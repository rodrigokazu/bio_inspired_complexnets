# -*- coding: utf-8 -*-

from igraph import *
import argparse
import random
import math
import os
import time
from multiprocessing import Pool, cpu_count

# main procedure
def main():
    global neurons_per_module
    global synapses_per_neuron
    global number_of_modules
    global meta
    global death_iterations
    global pruning_iterations
    global death_method
    global pruning_method
    global c_R
    global c_A
    global c_K
    global feed_forward
    global synaptic_reach
    global cross_modules
    global total_neurons
    global total_synapses
    global meta_network
    global net

    global mean_indegree_sq
    global mean_indegree
    global mean_degree
    global outdegrees
    global indegrees
    global degrees

    parser = argparse.ArgumentParser(description="Parameters for the network")
    parser.add_argument('-nn', type=int, default=10000)  # neurons_per_module
    parser.add_argument('-syn', type=int, default=100)  # synapses_per_neuron
    parser.add_argument('-mn', type=int, default=1)  # number_of_modules
    parser.add_argument('-meta', choices=['random', 'offdiagonal', 'full', 'smallworld', 'lattice', 'file'],
                        default='full')  # meta_network
    parser.add_argument('-metaargs', type=float,
                        default=0)  # meta_network argument: for small world, it's the percentage of rewiring
    parser.add_argument('-dits', type=int, default=1)  # death_iterations
    parser.add_argument('-pits', type=int, default=0)  # pruning_iterations
    parser.add_argument('-dmet', choices=['in-degree', 'out-degree', 'degree', 'random'],
                        default='in-degree')  # death_method
    parser.add_argument('-pmet', choices=['hebbian-approx', 'inv-hebbian-approx', 'random'],
                        default='hebbian-approx')  # pruning_method
    parser.add_argument('-r', type=float, default=1.0 / 3.0)  # c_R
    parser.add_argument('-a', type=float, default=0.01)  # c_A
    parser.add_argument('-k', type=float, default=0.2)  # c_K
    parser.add_argument('-ff', type=float, default=1)  # feed_forward
    parser.add_argument('-sr', type=int, default=10000)  # synaptic_reach
    parser.add_argument('--cm', dest='cm', action='store_true')
    parser.add_argument('--no-cm', dest='cm', action='store_false')

    parser.add_argument('--save-freq', dest="save_freq", type=int, default=50)  # save_frequency
    parser.add_argument('-save-to', dest="save_to", type=str, default='.')  # output_folder
    parser.add_argument('--save-fitness', dest='save_fitness', action='store_true')
    parser.add_argument('--no-save-fitness', dest='save_fitness', action='store_false')
    parser.add_argument('--save-net', dest='save_net', action='store_true')
    parser.add_argument('--no-save-net', action='store_false')

    args = parser.parse_args()

    print(args)

    neurons_per_module = args.nn
    synapses_per_neuron = args.syn
    number_of_modules = args.mn
    meta = args.meta
    metaargs = args.metaargs
    death_iterations = args.dits
    pruning_iterations = args.pits
    death_method = args.dmet
    pruning_method = args.pmet
    c_R = args.r
    c_A = args.a
    c_K = args.k
    feed_forward = args.ff
    synaptic_reach = args.sr
    cross_modules = args.cm
    total_neurons = args.nn * args.mn
    total_synapses = total_neurons * args.syn

    save_freq = args.save_freq
    output_folder = args.save_to
    save_fitness = args.save_fitness
    save_net = args.save_net

    save_parameters(vars(args), output_folder)

    print("Creating meta-network ...")

    if meta == 'random':
        meta_network = Graph.Erdos_Renyi(number_of_modules, m=number_of_modules / 2, directed=True)
        for v in meta_network.vs():
            if len(v.successors()) == 0:
                to_vs = list(range(0, number_of_modules))
                to_vs.remove(v.index)
                meta_network.add_edge(v.index, random.choice(to_vs))
    elif meta == 'full':
        if number_of_modules == 1:
            meta_network = Graph.Full(number_of_modules, loops=True, directed=True)
        else:
            meta_network = Graph.Full(number_of_modules, loops=False, directed=True)
    elif meta == 'smallworld':
        meta_network = Graph.Lattice([number_of_modules], nei=2, directed=True, mutual=False, circular=True)
        to_rewire_es = random.sample(meta_network.es, int(round(metaargs * len(meta_network.es))))
        to_rewire = [[e.source, e.target] for e in to_rewire_es]
        for o_edge in to_rewire:
            o_source = o_edge[0]
            o_target = o_edge[1]
            meta_network.delete_edges(o_source, o_target)
            n_potential = [v for v in range(0, number_of_modules) if v != o_target]
            n_target = random.choice(n_potential)
            meta_network.add_edge(o_source, n_target)
    elif meta == 'lattice':
        meta_network = Graph.Lattice([number_of_modules], nei=2, directed=True, mutual=False, circular=True)
    elif meta == 'offdiagonal':
        meta_network = Graph(directed=True)
        for i in range(0, number_of_modules):
            meta_network.add_vertex(id=i)
        for i in range(0, number_of_modules):
            meta_network.add_edge(i, (i + 1) % number_of_modules)
        print(meta_network)
    elif meta == 'file':
        i = 0
    else:
        print(f"{meta} is not a valid option.")

    for i in range(0, number_of_modules):
        meta_network.vs.select(i)['id'] = i

    print("Creating whole network ...")

    net = Graph(directed=True)
    for i in range(0, total_neurons):
        net.add_vertex(id=i, module=int(math.floor(i / neurons_per_module)))

    new_edges = []
    for i in range(0, total_synapses):
        if i % 1000 == 0:
            print(f"{i} synapses added ...")
        new_edges.append(get_new_random_edge())

    net.add_edges(new_edges)

    print("Death iterations ...")

    mean_indegree = mean(net.vs.indegree())
    mean_degree = mean(net.vs.degree())
    outdegrees = net.outdegree()
    indegrees = net.indegree()
    degrees = net.degree()

    with Pool(processes=cpu_count()) as pool:
        for it in range(0, death_iterations):
            to_remove = pool.map(death_worker, range(len(net.vs)))

            to_remove = [v for v in to_remove if v is not None]

            edges_to_remove = []
            for v in to_remove:
                for v2 in net.vs[v].successors():
                    edges_to_remove.append((v, v2.index))
                for v1 in net.vs[v].predecessors():
                    edges_to_remove.append((v1.index, v))

            net.delete_edges(edges_to_remove)

            gap = total_synapses - len(net.es)
            new_edges = pool.map(get_new_random_edge, range(gap))
            net.add_edges(new_edges)

            print(f"Death {it}: {len(to_remove)}")

            if it % save_freq == 0:
                if save_net:
                    save_network_to_file("death", it, where=output_folder)

    print("Pruning iterations ...")

    mean_indegree_sq = mean(net.vs.indegree()) ** 2
    outdegrees = net.outdegree()
    indegrees = net.indegree()

    with Pool(processes=cpu_count()) as pool:
        for it in range(0, pruning_iterations):
            to_remove = pool.map(pruning_worker, range(len(net.es)))

            to_remove = [e for e in to_remove if e is not None]

            net.delete_edges(to_remove)

            print(f"Pruning {it}: {len(to_remove)}")

            if it % save_freq == 0:
                if save_net:
                    save_network_to_file("pruning", it, where=output_folder)


def death_worker(v_index):
    fitness = death_probability(v_index)
    if random.random() < fitness:
        return v_index
    return None


def pruning_worker(e_index):
    e = net.es[e_index]
    fitness = pruning_probability((e.source, e.target))
    if random.random() < fitness:
        return (e.source, e.target)
    return None


def get_new_random_edge(dummy_arg=None):
    if feed_forward > 0 and random.random() < feed_forward:
        forward_edge = True
    else:
        forward_edge = False

    if not cross_modules:
        while True:
            v1 = net.vs[random.randint(0, total_neurons - 1)]
            if forward_edge:
                if v1.index == (v1['module'] + 1) * neurons_per_module - 1:
                    continue  # v1 is the last neuron in its module
                v2 = net.vs[random.randint(v1.index + 1, (v1['module'] + 1) * neurons_per_module - 1)]
            else:
                if v1.index == v1['module'] * neurons_per_module:
                    continue  # v1 is the first neuron in its module
                v2 = net.vs[random.randint(v1['module'] * neurons_per_module, v1.index - 1)]
            if v2.index != v1.index:
                break
    else:
        if forward_edge:
            v1 = net.vs[random.randint(0, total_neurons - 2)]
        else:
            v1 = net.vs[random.randint(1, total_neurons - 1)]

        module_head = v1['module'] * neurons_per_module
        module_tail = (v1['module'] + 1) * neurons_per_module

        edge_reach = random.randint(1, synaptic_reach)

        if forward_edge:
            target_vertex_id = v1.index + edge_reach
            crossed = target_vertex_id >= module_tail
            remainder = target_vertex_id - module_tail
        else:
            target_vertex_id = v1.index - edge_reach
            crossed = target_vertex_id < module_head
            remainder = module_head - target_vertex_id

        if crossed:
            this_module = meta_network.vs.find(id_eq=v1['module'])
            try:
                target_module_id = random.choice(this_module.neighbors())['id']
            except IndexError:
                print(f"Meta network has isolated vertex: {this_module['id']}")
                raise

            if forward_edge:
                v2 = net.vs[target_module_id * neurons_per_module + remainder]
            else:
                v2 = net.vs[(target_module_id + 1) * neurons_per_module - remainder]
        else:
            v2 = net.vs[target_vertex_id]

    return (v1.index, v2.index)


def death_probability(v_index):
    if death_method == 'degree':
        num = degrees[v_index]
        den = mean_degree
    elif death_method == 'in-degree':
        num = indegrees[v_index]
        den = mean_indegree
    elif death_method == 'out-degree':
        num = outdegrees[v_index]
        den = mean_indegree
    elif death_method == 'random':
        num = 1
        den = 1

    return c_A * math.exp(-c_K * (num / den))


def pruning_probability(e):
    i, j = e

    if pruning_method == 'hebbian-approx':
        num = indegrees[j] * outdegrees[i]
        den = mean_indegree_sq
    elif pruning_method == 'inv-hebbian-approx':
        num = indegrees[i] * outdegrees[j]
        den = mean_indegree_sq
    elif pruning_method == 'random':
        num = 1
        den = 1

    return c_A * math.exp(-c_K * (num / den))


def save_network_to_file(suffix="", it=0, where="."):
    if not os.path.exists(os.path.join(where, "Edges")):
        os.makedirs(os.path.join(where, "Edges"))
    fn = os.path.join(where, f"Edges/mota_net_{suffix}{it}.edges")
    net.write_edgelist(fn)


def save_parameters(args, where="."):
    if not os.path.exists(where):
        os.makedirs(where)
    fn = os.path.join(where, "parameters.txt")
    with open(fn, 'w') as f:
        for a in args:
            f.write(f"{a} = {args[a]}\n")


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time()
    print(f"Execution time: {e - s} seconds")

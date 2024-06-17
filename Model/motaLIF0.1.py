# -*- coding: utf-8 -*-
import brian2 as b2
import numpy as np
import matplotlib.pyplot as plt
from igraph import *
import argparse
import random
import math
import os
import time
from multiprocessing import Pool, cpu_count

# Function Definitions

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

def death_probability(v_index, mean_indegree, mean_degree, outdegrees, indegrees, degrees):
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

def pruning_probability(e, mean_indegree_sq, outdegrees, indegrees):
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

def simulate_neuronal_activity(iteration, output_folder):

    print("Simulating neuronal activity ...")

    duration = 10 * b2.second

    # Parameters for LIF neurons
    tau = 10 * b2.ms
    vr = -70 * b2.mV
    vt = -50 * b2.mV
    El = -65 * b2.mV
    Rm = 10 * b2.Mohm
    v_reset = -65 * b2.mV
    v_threshold = -50 * b2.mV

    eqs = '''
    dv/dt = (El - v + Rm * (I0 + I_noise)) / tau : volt
    dI_noise/dt = -I_noise/tau_noise + sigma*xi*tau_noise**-0.5 : amp
    I0 : amp
    sigma : amp
    tau_noise : second
    '''

    start_time = time.time()
    print("Creating neuron group...")
    G = b2.NeuronGroup(total_neurons, model=eqs, threshold='v>v_threshold', reset='v=v_reset', method='linear')
    G.v = vr
    G.I0 = 0.2 * b2.nA  # Reduced baseline input current
    G.sigma = 0.1 * b2.nA  # Noise amplitude
    G.tau_noise = 5 * b2.ms  # Noise correlation time
    end_time = time.time()
    print(f"Neuron group creation took {end_time - start_time:.2f} seconds")

    start_time = time.time()
    # Create synapses with STDP
    print("Creating synapses...")
    S = b2.Synapses(G, G,
                    '''w : 1
                       dpre/dt = -pre/tau_pre : 1 (event-driven)
                       dpost/dt = -post/tau_post : 1 (event-driven)''',
                    on_pre='''v_post += w*mV
                              pre = 1
                              w = clip(w + post, 0, w_max)''',
                    on_post='''post = 1
                               w = clip(w + pre, 0, w_max)''')

    sources = [e.source for e in net.es]
    targets = [e.target for e in net.es]
    S.connect(i=sources, j=targets)
    end_time = time.time()
    print(f"Synapse creation took {end_time - start_time:.2f} seconds")

    # Set the STDP parameters
    tau_pre = 20 * b2.ms
    tau_post = 20 * b2.ms
    A_pre = 0.01
    A_post = -A_pre
    w_max = 1.0

    S.w = 'rand() * w_max'

    start_time = time.time()
    print("Running simulation...")
    M = b2.SpikeMonitor(G)
    b2.run(duration)
    end_time = time.time()
    print(f"Simulation run took {end_time - start_time:.2f} seconds")
    print("Simulation complete.")

    start_time = time.time()
    # Get spike times and neuron indices
    spike_times = M.t / b2.ms
    neuron_indices = M.i

    # Identify the 10% most active neurons
    spike_counts = np.bincount(neuron_indices)
    most_active_neurons = np.argsort(spike_counts)[-int(0.1 * total_neurons):]

    # Generate and save raster plot
    plt.figure(figsize=(10, 6))
    plt.plot(spike_times, neuron_indices, '.k')
    plt.xlabel('Time (ms)')
    plt.ylabel('Neuron index')
    plt.title('Raster plot of neuronal activity')
    plt.savefig(os.path.join(output_folder, f'raster_plot_{iteration}.png'))
    plt.close()
    end_time = time.time()
    print(f"Raster plot generation took {end_time - start_time:.2f} seconds")

    start_time = time.time()
    # Update network topology based on STDP
    new_edges = []
    edges_to_remove = []

    for i, j, w in zip(S.i, S.j, S.w):
        if w < 0.01:  # Threshold for removing a synapse
            edges_to_remove.append((i, j))

    # Remove weak synapses
    for i, j in edges_to_remove:
        eid = net.get_eid(i, j)
        if eid is not None:
            net.delete_edges(eid)

    # Optionally, add new random edges to maintain connectivity
    num_new_edges = len(edges_to_remove)
    for _ in range(num_new_edges):
        new_edges.append(get_new_random_edge())

    net.add_edges(new_edges)
    end_time = time.time()
    print(f"Network topology update based on activity took {end_time - start_time:.2f} seconds")


def perform_death_iteration(it, save_freq, save_net, output_folder, mean_indegree, mean_degree, outdegrees, indegrees, degrees):
    print("Death iterations ...")

    with Pool(processes=cpu_count()) as pool:
        to_remove = pool.starmap(death_worker, [(v, mean_indegree, mean_degree, outdegrees, indegrees, degrees) for v in range(len(net.vs))])

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

def perform_pruning_iteration(it, save_freq, save_net, output_folder, mean_indegree_sq, outdegrees, indegrees):
    print("Pruning iterations ...")

    with Pool(processes=cpu_count()) as pool:
        to_remove = pool.starmap(pruning_worker, [(e, mean_indegree_sq, outdegrees, indegrees) for e in range(len(net.es))])

        to_remove = [e for e in to_remove if e is not None]

        net.delete_edges(to_remove)

        print(f"Pruning {it}: {len(to_remove)}")

        if it % save_freq == 0:
            if save_net:
                save_network_to_file("pruning", it, where=output_folder)

def death_worker(v_index, mean_indegree, mean_degree, outdegrees, indegrees, degrees):
    fitness = death_probability(v_index, mean_indegree, mean_degree, outdegrees, indegrees, degrees)
    if random.random() < fitness:
        return v_index
    return None

def pruning_worker(e_index, mean_indegree_sq, outdegrees, indegrees):
    e = net.es[e_index]
    fitness = pruning_probability((e.source, e.target), mean_indegree_sq, outdegrees, indegrees)
    if random.random() < fitness:
        return (e.source, e.target)
    return None

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

    # Death Iteration Block
    for it in range(death_iterations):
        print(f"Death iteration {it} ...")
        mean_indegree = mean(net.vs.indegree())
        mean_degree = mean(net.vs.degree())
        outdegrees = net.outdegree()
        indegrees = net.indegree()
        degrees = net.degree()

        perform_death_iteration(it, save_freq, save_net, output_folder, mean_indegree, mean_degree, outdegrees, indegrees, degrees)

        start_time = time.time()
        simulate_neuronal_activity(it, output_folder)
        end_time = time.time()
        print(f"Neuronal activity simulation took {end_time - start_time:.2f} seconds")

    # Pruning Iteration Block
    for it in range(pruning_iterations):
        print(f"Pruning iteration {it} ...")
        mean_indegree_sq = mean(net.vs.indegree()) ** 2
        outdegrees = net.outdegree()
        indegrees = net.indegree()

        perform_pruning_iteration(it, save_freq, save_net, output_folder, mean_indegree_sq, outdegrees, indegrees)

        start_time = time.time()
        simulate_neuronal_activity(it, output_folder)
        end_time = time.time()
        print(f"Neuronal activity simulation took {end_time - start_time:.2f} seconds")

    save_network_to_file("final", it, where=output_folder)
    print("Final network saved")

if __name__ == "__main__":
    s = time.time()
    main()
    e = time.time()
    print(f"Execution time: {e - s} seconds")

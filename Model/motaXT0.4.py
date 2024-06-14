 # -*- coding: utf-8 -*-

from igraph import *
import argparse
import random
import math
import os
import time
#import re

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

    # Gets network and simulation parameters from call

    parser = argparse.ArgumentParser(description="Parameters for the network")
    parser.add_argument('-nn',type=int,default=10000) #neurons_per_module
    parser.add_argument('-syn',type=int,default=100) #synapses_per_neuron
    parser.add_argument('-mn',type=int,default=1) #number_of_modules
    parser.add_argument('-meta',choices=['random','offdiagonal','full','smallworld','lattice','file'],default='full') #meta_network
    parser.add_argument('-metaargs',type=float,default=0) #meta_network argument: for small world, it's the percentage of rewiring
    parser.add_argument('-dits',type=int,default=1) #death_iterations
    parser.add_argument('-pits',type=int,default=0) #pruning_iterations
    parser.add_argument('-dmet',choices=['in-degree','out-degree','degree','random'],default='in-degree') #death_method
    parser.add_argument('-pmet',choices=['hebbian-approx','inv-hebbian-approx','random'],default='hebbian-approx') #pruning_method
    parser.add_argument('-r',type=float,default=1.0/3.0) #c_R
    parser.add_argument('-a',type=float,default=0.01) #c_A
    parser.add_argument('-k',type=float,default=0.2) #c_K
    parser.add_argument('-ff',type=float,default=1) #feed_forward
    parser.add_argument('-sr',type=int,default=10000) #synaptic_reach
    # cross_modules
    parser.add_argument('--cm', dest='cm', action='store_true')
    parser.add_argument('--no-cm', dest='cm', action='store_false')

    # Gets output options
    parser.add_argument('--save-freq', dest="save_freq", type=int,default=50) #save_frequency
    parser.add_argument('-save-to', dest="save_to", type=str,default='.') #output_folder

    # save_fitness
    parser.add_argument('--save-fitness', dest='save_fitness', action='store_true')
    parser.add_argument('--no-save-fitness', dest='save_fitness', action='store_false')

    # save_net
    parser.add_argument('--save-net', dest='save_net', action='store_true')
    parser.add_argument('--no-save-net', dest='save_net', action='store_false')


    ### Parses arguments into parameters

    args = vars(parser.parse_args())

    print (args)

    neurons_per_module = args['nn']
    synapses_per_neuron = args['syn']
    number_of_modules = args['mn']
    meta = args['meta']
    metaargs = args['metaargs']
    death_iterations = args['dits']
    pruning_iterations = args['pits']
    death_method = args['dmet']
    pruning_method = args['pmet']
    c_R = args['r']
    c_A = args['a']
    c_K = args['k']
    feed_forward = args['ff']
    synaptic_reach = args['sr']
    cross_modules = args['cm']
    total_neurons = args['nn'] * args['mn']
    total_synapses = total_neurons * args['syn']

    save_freq = args['save_freq']
    output_folder = args['save_to']
    save_fitness = args['save_fitness']
    save_net = args['save_net']

    save_parameters(args, output_folder)

    print ("Creating meta-network ...")

    # Creates the meta-network
    if meta == 'random':
        meta_network = Graph.Erdos_Renyi(number_of_modules,m=number_of_modules/2,directed=True)
        for v in meta_network.vs():
            if len(v.successors()) == 0:
                to_vs = (range(0,number_of_modules))
                to_vs.remove(v.index)
                meta_network.add_edge(v.index,random.choice(to_vs))
    elif meta == 'full':
        if number_of_modules == 1:
            meta_network = Graph.Full(number_of_modules,loops=True,directed=True)
        else:
            meta_network = Graph.Full(number_of_modules,loops=False,directed=True)
    elif meta == 'smallworld':
        meta_network = Graph.Lattice([number_of_modules], nei=2, directed=True, mutual=False, circular=True)
        to_rewire_es = random.sample(meta_network.es, int(round(metaargs * len(meta_network.es))))
        to_rewire = [[e.source,e.target] for e in to_rewire_es]
        for o_edge in to_rewire:
            o_source = o_edge[0]
            o_target = o_edge[1]
            meta_network.delete_edges(o_source,o_target)
            n_potential = [v for v in range(0,number_of_modules) if v != o_target]
            n_target = random.choice(n_potential)
            meta_network.add_edge(o_source,n_target)
    elif meta == 'lattice':
        meta_network = Graph.Lattice([number_of_modules], nei=2, directed=True, mutual=False, circular=True)
    elif meta == 'offdiagonal':
        meta_network = Graph(directed=True)
        for i in range(0,number_of_modules):
            meta_network.add_vertex(id=i)
        for i in range(0,number_of_modules):
            meta_network.add_edge(i,(i+1) % number_of_modules)
        print (meta_network)
    elif meta == 'file':
        i = 0
        # Load an arbitrary meta-network from a file
        # named metanet.txt which must be in the same
        # folder as the program and contain a list of
        # edges between modules
    else:
        print "{0} is not a valid option.".format(meta)

    # number the modules
    for i in range(0,number_of_modules):
        meta_network.vs.select(i)['id'] = i
    
    print ("Creating whole network ...")

    # Creates the whole network, nodes have IDs set by me (nid) and
    # are allocated to their modules, using a vertex attribute (module)
    net = Graph(directed=True)
    for i in range(0, total_neurons):
        net.add_vertex(id=i,module=int(math.floor(i/neurons_per_module)))

    #for v in net.vs:
    #    print str(v['id']) + " " + str(v['module'])

    # Adds edges
    new_edges = []
    for i in range(0, total_synapses):
        if i % 1000 == 0:
            print (str(i) + " synapses added ...")
        new_edges.append(get_new_random_edge())

    net.add_edges(new_edges)


    print ("Death iterations ...")

    ### Death iterations

    mean_indegree = mean(net.vs.indegree())
    mean_degree = mean(net.vs.degree())
    outdegrees = net.outdegree()
    indegrees = net.indegree()
    degrees = net.degree()

    for it in range(0,death_iterations):
        # Adds neurons to a list to be killed according to each neuron's fitness
        to_remove = []
        fitness_list = []
        for v in net.vs:
            fitness = death_probability(v.index)
            fitness_list.append(fitness)
            if random.random() < fitness:
                to_remove.append(v)

        # Kills the neurons in the list
        edges_to_remove = []
        for v in to_remove:
            for v2 in v.successors():
                edges_to_remove.append(net.get_eid(v,v2))
            for v1 in v.predecessors():
                edges_to_remove.append(net.get_eid(v1,v))
        
        net.delete_edges(edges_to_remove)
        
        # Calculates the missing synapses and adds them back
        gap = total_synapses - len(net.es)
        new_edges = []
        for i in range(0,gap):
            new_edges.append(get_new_random_edge())
        
        net.add_edges(new_edges)

        print ("Death " + str(it) + ": " + str(len(to_remove)))

        # Saves the network
        if it % save_freq == 0:
            if save_net:
                save_network_to_file("death", it, where=output_folder)
            #if save_fitness:
            #    save_node_fitness_to_file(fitness_list, where=output_folder)

    print ("Pruning iterations ...")

    ### Pruning iterations

    mean_indegree_sq = mean(net.vs.indegree()) ** 2
    outdegrees = net.outdegree()
    indegrees = net.indegree()

    for it in range(0,pruning_iterations):    
        # Adds synapses to a list to be removed according to each synapse's fitness
        to_remove = []
        fitness_list = []
        for e in net.es:
            fitness = pruning_probability(e)
            fitness_list.append(fitness)
            if random.random() < fitness:
                to_remove.append(e)

        # Remove synapses in the list
        net.delete_edges(to_remove)

        print ("Pruning " + str(it) + ": " + str(len(to_remove)))

        # Saves the network
        if it % save_freq == 0:
            if save_net:
                save_network_to_file("pruning", it, where=output_folder)
#            if save_fitness:
#                save_edge_fitness_to_file(fitness_list, where=output_folder)
        

def get_new_random_edge():

    # Decides if the edge is forward or backward
    forward_edge = random.random() <= feed_forward

    # Selects a random first node
    if cross_modules:
        v1 = net.vs[random.randint(0,total_neurons-1)]
    else:
        if forward_edge:
            v1 = net.vs[random.randint(0,total_neurons-2)]
        else:
            v1 = net.vs[random.randint(1,total_neurons-1)]


    v2 = -1

    module_head = v1['module'] * neurons_per_module
    module_tail = (v1['module'] + 1) * neurons_per_module

    # Selects reach for this edge
    if cross_modules:
        edge_reach = random.randint(1, synaptic_reach)
    else:
        if forward_edge:
            edge_reach = random.randint(1, neurons_per_module - v1['id'] - 1)
        else:
            edge_reach = random.randint(1, v1['id'])

    #print "v1: " + str(v1['id']) + "/" + str(v1['module']) + (" + " if forward_edge else " - ") + str(edge_reach)

    if forward_edge:
        target_vertex_id = v1['id'] + edge_reach
        crossed = target_vertex_id >= module_tail
        remainder = target_vertex_id - module_tail
    else:
        target_vertex_id = v1['id'] - edge_reach
        crossed = target_vertex_id < module_head
        remainder = module_head - target_vertex_id

    if crossed:
        this_module = meta_network.vs.find(id_eq = v1['module'])
        # Não aceita valores diferentes de 1 ou 0 na matriz da meta-rede, depois tem que mudar isso pra aceitar conexões fracionadas
        try:
            target_module_id = random.choice(this_module.neighbors())['id']
        except:
            print ("Meta network has isolated vertex:" + str(this_module['id']))
            raise
        
        if forward_edge:
            v2 = net.vs[target_module_id * neurons_per_module + remainder]
        else:
            v2 = net.vs[(target_module_id + 1) * neurons_per_module - remainder]
    else:
        v2 = net.vs[target_vertex_id]

    return (v1,v2)


def death_probability(v):

    if death_method == 'degree':
        num = degrees[v]
        den = mean_degree 
    elif death_method == 'in-degree':
        num = indegrees[v]
        den = mean_indegree
    elif death_method == 'out-degree':
        num = outdegrees[v]
        den = mean_indegree
    elif death_method == 'random':
        num = 1
        den = 1

    return c_A * math.exp( -c_K * (num / den))

def pruning_probability(e):
    
    i = e.source
    j = e.target
    
    if pruning_method == 'hebbian-approx':
        num = indegrees[j] * outdegrees[i]
        den = mean_indegree_sq
    elif pruning_method == 'inv-hebbian-approx':
        num = indegrees[i] * outdegrees[j]
        den = mean_indegree_sq
    elif pruning_method == 'random':
        num = 1
        den = 1

    return c_A * math.exp( -c_K * (num / den))

def save_network_to_file(suffix="", it=0, where="."):
    if not os.path.exists(where+"/Edges"):
        os.makedirs(where+"/Edges")
    fn = where + "/Edges/mota_net_" + suffix + str(it) + ".edges"
    net.write_edgelist(fn)

#def save_node_fitness_to_file(fitness_list, where="."):
#    if not os.path.exists(where+"/Fitness"):
#        os.makedirs(where+"/Fitness")
#    fn = where + "/Fitness/mota_node_fitness_net_" + suffix + str(it) + ".txt"
#    f = open(fn,'w')
#    
#    for fit in fitness_list:
#        f.write(fit)
#
#    f.close()
#
#def save_edge_fitness_to_file(fitness_list, where="."):
#    if not os.path.exists(where+"/Fitness"):
#        os.makedirs(where+"/Fitness")
#    fn = where + "/Fitness/mota_edge_fitness_net_" + suffix + str(it) + ".txt"
#    f = open(fn,'w')
#    
#    for fit in fitness_list:
#        f.write(fit)
#
#    f.close()

def save_parameters(args,where="."):
    if not os.path.exists(where):
        os.makedirs(where)
    fn = where+"/parameters.txt"
    f = open(fn,'w')
    
    for a in args:
        f.write(a + " = " + str(args[a]) + "\n")

    f.close()
    
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


s = time.time()

# Run!
main()

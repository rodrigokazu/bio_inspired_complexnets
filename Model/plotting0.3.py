 # -*- coding: utf-8 -*-

from igraph import *
import argparse
import os, gc
import re

import numpy as np
import matplotlib.pyplot as plt

# main procedure

def main():

	global dir_name
	global total_neurons

	parser = argparse.ArgumentParser(description="Plotting arguments ...")
	parser.add_argument('-dir',type=str)

	args = vars(parser.parse_args())

	calc_metrics = True
	plot_distributions = True

	print "Getting all files ..."
	dir_name = args['dir']

	# list gml files
	files_list = get_files_list(dir_name+"/GML",r'mota_net',r'(death)|(pruning)')
	
	neurons_per_it = {}
	neurons_over_1_per_it = {}
	synapses_per_it = {}
	clustering_per_it = {}
	average_shortest_path_per_it = {}
	giant_component_size_per_it = {}

	neurons_per_it["death"] = {}
	neurons_over_1_per_it["death"] = {}
	synapses_per_it["death"] = {}
	clustering_per_it["death"] = {}
	average_shortest_path_per_it["death"] = {}
	giant_component_size_per_it["death"] = {}

	neurons_per_it["pruning"] = {}
	neurons_over_1_per_it["pruning"] = {}
	synapses_per_it["pruning"] = {}
	clustering_per_it["pruning"] = {}
	average_shortest_path_per_it["pruning"] = {}
	giant_component_size_per_it["pruning"] = {}

	print "Loading networks ..."
	if plot_distributions:
		print "Plotting distributions ..."
	if calc_metrics:
		print "Computing metrics ..."

	if not os.path.exists(dir_name+"/Graphs"):
		os.makedirs(dir_name+"/Graphs")

	# for each gml file
	for fn in files_list:
		print "File: " + fn
		stage = re.search(r'(death|pruning)',fn).group(0)
		iteration = int(re.search(r'[0-9]+',fn).group(0))

		net = Graph.Read_GML(dir_name+"/GML/"+fn)
		total_neurons = len(net.vs)

		# plot the distribution
		if plot_distributions:
			plot_degree_distribution(net.degree(),dir_name+"/Graphs/Degree Dist " + stage + " " + str(iteration), yrange = total_neurons)

		# calcular e store clustering, shortest path, giant component size
		if calc_metrics:	

			# giant component size
			_gc = net.as_undirected().decompose(mode=WEAK, maxcompno=1, minelements=2)[0]
			_gcs = len(_gc.vs)

			giant_component_size_per_it[stage][iteration] = _gcs
		
			# clustering
			_clust = _gc.transitivity_undirected(mode="zero")

			clustering_per_it[stage][iteration] = _clust

			# average shortes path length
			_aspl = _gc.average_path_length(directed=False, unconn=False)

			average_shortest_path_per_it[stage][iteration] = _aspl
		
		gc.collect()

		# store number of neurons, synapses
		neurons_per_it[stage][iteration] = len(net.vs.select(_degree_gt = 0))
		neurons_over_1_per_it[stage][iteration] = len(net.vs.select(_degree_gt = 1))
		synapses_per_it[stage][iteration] = len(net.es)

	
	# list fitness lists
	files_list = get_files_list(dir_name,r'mota_fitness',r'(Death)|(Pruning)')

	# for each fitness file, plot the distribution
	#####

	if calc_metrics:

		print "Plotting metrics ..."

		# plot clustering, shortest path, giant component size, number of neurons, synapses por iteração
		plot_per_it(dir_name+"/Graphs/Neurons X Iteration (death)",neurons_per_it["death"],label="Neurons")
		plot_per_it(dir_name+"/Graphs/Neurons X Iteration (pruning)",neurons_per_it["pruning"],label="Neurons")
		plot_per_it(dir_name+"/Graphs/Neurons X Iteration",join_dicts(neurons_per_it["death"], neurons_per_it["pruning"]),label="Neurons")
		
		plot_per_it(dir_name+"/Graphs/Neurons (over 1) X Iteration (death)",neurons_over_1_per_it["death"],label="Neurons")
		plot_per_it(dir_name+"/Graphs/Neurons (over 1) X Iteration (pruning)",neurons_over_1_per_it["pruning"],label="Neurons")
		plot_per_it(dir_name+"/Graphs/Neurons (over 1) X Iteration",join_dicts(neurons_over_1_per_it["death"], neurons_over_1_per_it["pruning"]),label="Neurons")

		plot_per_it(dir_name+"/Graphs/Synapses X Iteration (death)",synapses_per_it["death"],label="Synapses")
		plot_per_it(dir_name+"/Graphs/Synapses X Iteration (pruning)",synapses_per_it["pruning"],label="Synapses")
		plot_per_it(dir_name+"/Graphs/Synapses X Iteration",join_dicts(synapses_per_it["death"], synapses_per_it["pruning"]),label="Synapses")
		
		plot_per_it(dir_name+"/Graphs/ASPL X Iteration (death)",average_shortest_path_per_it["death"],label="Average Shortest Path")
		plot_per_it(dir_name+"/Graphs/ASPL X Iteration (pruning)",average_shortest_path_per_it["pruning"],label="Average Shortest Path")
		plot_per_it(dir_name+"/Graphs/ASPL X Iteration",join_dicts(average_shortest_path_per_it["death"], average_shortest_path_per_it["pruning"]),label="Average Shortest Path")

		plot_per_it(dir_name+"/Graphs/Clustering X Iteration (death)",clustering_per_it["death"],label="Clustering")
		plot_per_it(dir_name+"/Graphs/Clustering X Iteration (pruning)",clustering_per_it["pruning"],label="Clustering")
		plot_per_it(dir_name+"/Graphs/Clustering X Iteration",join_dicts(clustering_per_it["death"], clustering_per_it["pruning"]),label="Clustering")

		plot_per_it(dir_name+"/Graphs/Giant Component X Iteration (death)",giant_component_size_per_it["death"],label="Giant Component")
		plot_per_it(dir_name+"/Graphs/Giant Component X Iteration (pruning)",giant_component_size_per_it["pruning"],label="Giant Component")
		plot_per_it(dir_name+"/Graphs/Giant Component X Iteration",join_dicts(giant_component_size_per_it["death"], giant_component_size_per_it["pruning"]),label="Giant Component")
		
		# save csv file with clustering, shortest path, giant component size, number of neurons, synapses por iteração
		for k in neurons_per_it.keys():
			write_to_csv("NeuronsOver1PerIteration.csv", neurons_over_1_per_it["death"], neurons_over_1_per_it["pruning"])
			write_to_csv("NeuronsPerIteration.csv", neurons_per_it["death"], neurons_per_it["pruning"])
			write_to_csv("SynapsesPerIteration.csv", synapses_per_it["death"], synapses_per_it["pruning"])
			write_to_csv("ClusteringPerIteration.csv", clustering_per_it["death"], clustering_per_it["pruning"])
			write_to_csv("AverageShortestPathPerIteration.csv", average_shortest_path_per_it["death"], average_shortest_path_per_it["pruning"])
			write_to_csv("GiantComponentPerIteration.csv", giant_component_size_per_it["death"], giant_component_size_per_it["pruning"])

def write_to_csv(fn, death_dict, pruning_dict):

	if not os.path.exists(dir_name+"/Data by Iteration"):
		os.makedirs(dir_name+"/Data by Iteration")

	f = open(dir_name+"/Data by Iteration/" + fn,'w')
	
	f.write("Stage,Iteration,Value\n")
	
	for it,v in death_dict.iteritems():
		f.write("Death," + str(it) + "," + str(v) + "\n")

	for it,v in pruning_dict.iteritems():
		f.write("Pruning," + str(it) + "," + str(v) + "\n")

	f.close()

def join_dicts(a,b):
	c = {}
	transition = max(a.keys())
	for k in a.keys():
		c[k] = a[k]
	for k in b.keys():
		c[k+transition] = b[k]
	return c

def get_files_list(d,preffix,regexp):
	print "Getting filenames ..."
	res = []
	for f in os.listdir(d):
		if re.search(preffix,f) and re.search(regexp,f):
			res.append(f)
	
	return sorted(res)

def plot_degree_distribution(dd, name, yrange):
	# get title
	t = name.split("/")[1]

	fig = plt.figure()
	ax = fig.add_subplot(111)

	# plots data
	ax.loglog(np.bincount(dd),'bo')

	# sets labels
	ax.set_title(t)
	ax.set_ylabel("Frequency")
	ax.set_xlabel("Degree")

	# save to file
	plt.savefig(name+'.png', bbox_inches='tight')
	plt.close(fig)

def plot_per_it(name,data,label,xl="Iteration",legend=[]):
	
	fig = plt.figure()
	ax = fig.add_subplot(111)

	# plots data
	if data != None:
		ax.plot(data.keys(),data.values(),'bo')

	# axes
	ax.set_xlim([0.0,total_neurons])
	ax.set_ylim([0.0,total_neurons])

	# sets labels
	ax.set_title(label)
	ax.set_ylabel(label)
	ax.set_xlabel(xl)

	# saves to file
	plt.savefig(name+'.png', bbox_inches='tight')
	plt.close(fig)

# Run!
main()
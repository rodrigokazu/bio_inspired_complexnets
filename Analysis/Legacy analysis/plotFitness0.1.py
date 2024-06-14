 # -*- coding: utf-8 -*-

from igraph import *
import argparse
import random
import math
import os, gc
import re

import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# main procedure

def main():

	global dir_name
	global total_neurons
	global net
	global mean_indegree_sq
	global mean_indegree
	global mean_degree
	global outdegrees
	global indegrees
	global degrees
	global c_R
	global c_A
	global c_K

	c_R = 1.0/3.0
	c_A = 0.01
	c_K = 0.2

	parser = argparse.ArgumentParser(description="Plotting arguments ...")
	parser.add_argument('-dir',type=str)

	args = vars(parser.parse_args())

	print "Getting all files ..."
	dir_name = args['dir']

	# list gml files
	files_list = get_files_list(dir_name+"/GML",r'mota_net',r'(death)|(pruning)')
	
	print "Plotting ..."

	if not os.path.exists(dir_name+"/GraphsFitness"):
		os.makedirs(dir_name+"/GraphsFitness")

	if not os.path.exists(dir_name+"/../Distributions"):
		os.makedirs(dir_name+"/../Distributions")

	# for each gml file
	for fn in files_list:
		print "File: " + fn
		stage = re.search(r'(death|pruning)',fn).group(0)
		iteration = int(re.search(r'[0-9]+',fn).group(0))

		net = Graph.Read_GML(dir_name+"/GML/"+fn)
		
		total_neurons = len(net.vs)
		degrees = net.degree()
		outdegrees = net.outdegree()
		indegrees = net.indegree()
		mean_degree = mean(net.vs.degree())
		mean_indegree = mean(net.vs.indegree())
		mean_indegree_sq = mean_indegree ** 2

		fitness_list = []
		#print stage
		if stage == "death":
			fitness_list = []
			for v in net.vs:
				fitness = int(death_probability(v.index) * 10 ** 7)
				if fitness > 0:
					fitness_list.append(fitness)

		elif stage == "pruning":
			fitness_list = []
			for e in net.es:
				fitness = int(pruning_probability(e) * 10 ** 7)
				if fitness > 0:
					fitness_list.append(fitness)

		# plot the distribution
		if len(fitness_list) > 0:
			plot_fitness_distribution(fitness_list,dir_name+"/GraphsFitness/Fitness Dist " + stage + " " + str(iteration), yrange = total_neurons)
			save_distribution_txt(dd = fitness_list, fn = dir_name+"/../Distributions/" + dir_name + " - Fitness Dist " + stage + " " + str(iteration))
			save_distribution_txt(dd = net.degree(), fn = dir_name+"/../Distributions/" + dir_name + " - Degree Dist " + stage + " " + str(iteration))
		
		gc.collect()

def get_files_list(d,preffix,regexp):
	print "Getting filenames ..."
	res = []
	for f in os.listdir(d):
		if re.search(preffix,f) and re.search(regexp,f):
			res.append(f)
	
	return sorted(res)

def plot_fitness_distribution(dd, name, yrange):
	# get title
	t = name.split("/")[1]

	fig = plt.figure()
	ax = fig.add_subplot(111)

	# plots data
	ax.loglog(np.histogram(dd, bins = 5),'bo')

	# sets labels
	ax.set_title(t)
	ax.set_ylabel("Frequency")
	ax.set_xlabel("Fitness (x10^7)")

	# save to file
	plt.savefig(name+'.png', bbox_inches='tight')
	plt.close(fig)

def death_probability(v, death_method = 'in-degree'):

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

def pruning_probability(e, pruning_method = 'hebbian-approx'):
	
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

def save_distribution_txt(fn, dd):
	
	f = open(fn + ".txt", 'w')
	for neu in dd:
		f.write(str(neu) + "\n")
	f.close()

# Run!
main()
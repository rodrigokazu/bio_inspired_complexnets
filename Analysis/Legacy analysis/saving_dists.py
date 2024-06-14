 # -*- coding: utf-8 -*-

from igraph import *
import numpy as np
import os

# main procedure

def main():

	# list gml files
	files_list = get_files_list()
	
	
	print "Loading networks to plot distribution ..."

	# for each gml file
	for fn in files_list:
		print "File: " + fn

		net = Graph.Read_GML(fn)
		
		save_degree_distribution(fn, net.degree())

def get_files_list():
	print "Getting filenames ..."
	
	f = open("distlist.txt","r")
	files_list = f.readlines()
	f.close()

	files_list = [fn.strip() for fn in files_list]

	return files_list

def save_degree_distribution(fn, dd):
	
	bins = np.bincount(dd)
	sp = os.path.split(fn)
	if not os.path.exists(sp[0] + "/Dist"):
		os.makedirs(sp[0] + "/Dist")
	nfn = sp[0] + "/Dist/" + sp[1][:-3] + "txt"
	#print nfn
	f = open(nfn, 'w')
	for bin in bins:
		#print bin
		f.write(str(bin) + "\n")
	f.close()

# Run!
main()
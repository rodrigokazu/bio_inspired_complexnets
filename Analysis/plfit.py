#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 09:40:02 2019

@author: kleber
"""
import os
import igraph
import powerlaw
import csv
import matplotlib.pyplot as plt
import re
from glob import glob
import pandas as pd

def read_parameters(folder):
    with open(folder + "../parameters.txt", "r") as f:
        pars = [x.strip().split(" = ")[1] for x in f.readlines()]
    return pars

def fit_net(fn, save_graphs = False, output_folder = None):
  
    stage = re.search(r'(pruning|death)', os.path.basename(fn)).group(0)
    it = re.search(r'[0-9]+', os.path.basename(fn)).group(0)
    
    net = igraph.Graph.Read_Edgelist(fn)

    rem_nodes = len(net.vs.select(_degree_gt = 0)) # net.vcount()
    rem_edges = net.ecount()
    
    if rem_edges < 100 or rem_nodes < 100:
        return "NULL"

    x = [t[2] for t in list(net.degree_distribution().bins())]

#    fit = powerlaw.Fit(x, xmin = 1, xmax = max(x)/10)
    fitfull = powerlaw.Fit(x, xmin = 1, xmax = max(x))
    fit = fitfull
    
    if save_graphs != False:
        fig = plt.figure()
        fig = fit.plot_pdf(color = 'b', linewidth = 2)
#        fig2 = fitfull.plot_pdf(color = 'b', linewidth = 2)
#        fit.power_law.plot_pdf(color = 'b', linestyle = '--', ax = fig2)
        fit.power_law.plot_pdf(color = 'b', linestyle = '--', ax = fig)
        
        plt.suptitle(stage.capitalize() + ", iteration #" + it, fontsize = 18, y = 1.02)
        plt.title("N = " + str(rem_nodes) + "; S = " + str(rem_edges) + "; alpha = " + str(round(fit.power_law.alpha,3)) + "; D = " + str(round(fit.power_law.D,3)), fontsize = 14)
#        plt.axvline(x = max(x)/10, color = '0.6', linestyle = ':')
        
        if output_folder is None:
            plt.savefig(os.path.splitext(fn)[0] + '.png', bbox_inches = 'tight')
        else:
            plt.savefig(output_folder + os.path.splitext(os.path.basename(fn))[0] + '.png', bbox_inches = 'tight')
            
#        plt.close(fig)

    rlist = [fn, stage, it, rem_nodes, rem_edges, round(fit.power_law.alpha, 4), round(fit.power_law.D, 4)]
    
    R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio = True)
    rlist.extend([round(R,4), round(p,4)])
    
    R, p = fit.distribution_compare('power_law', 'lognormal', normalized_ratio = True)
    rlist.extend([round(R,4), round(p,4)])
    
    R, p = fit.distribution_compare('power_law', 'truncated_power_law', normalized_ratio = True)
    rlist.extend([round(R,4), round(p,4)])
    
    R, p = fit.distribution_compare('truncated_power_law', 'lognormal', normalized_ratio = True)
    rlist.extend([round(R,4), round(p,4)])
    
    return rlist

def fit_nets(folder, save_graphs = False, output_folder = None):
    if output_folder is None:
        output_folder = folder + "../Results/"
        
    if not os.path.exists(output_folder):
		os.makedirs(output_folder)
        
    fs = []
    for (dirpath, dirnames, filenames) in os.walk(folder):
        fs.extend(os.path.join(dirpath, filename) for filename in filenames)
        break
    
    pars = read_parameters(folder)
    
    mdata = []
    for f in fs:
        ks = fit_net(f, save_graphs = save_graphs, output_folder = output_folder)
        if ks != "NULL":
            m = pars[:]
            m.extend(ks)
            mdata.append(m)

    with open(output_folder + "output.csv", "wb") as f:
        writer = csv.writer(f, delimiter = ";")
        writer.writerow(["a", "save_freq", "dmet", "save_net", "nn", "dits", "sr", "pits", "mn", "metaargs", "syn", "cm", "meta", "ff", "k", "save_fitness",
                         "r", "pmet", "save_to", "filename","stage","iteration","nodes","edges","alpha","D","R_exp","p_exp","R_lognormal","p_lognormal","R_truncPL","p_truncPL", "R_trunc_vs_LN","p_trunc_vs_LN"])
        writer.writerows(mdata)
    
    if not os.path.exists(output_folder + "/Summary/"):
		os.makedirs(output_folder + "/Summary/")
    
    df = pd.read_csv(output_folder + "output.csv", sep=";")
#    print(df['iteration'])
#    print(df['dits'])
    df['giteration'] = df.apply (lambda row: (row['iteration'] + row['dits'] if row['stage'] == "pruning" else row['iteration']), axis=1)
        
    plot_summary(df, 'nodes', output_folder, 'Neurons')
    plot_summary(df, 'edges', output_folder, "Synapses")
    plot_summary(df, 'alpha', output_folder, "Exponent")
    plot_summary(df, 'D', output_folder, "KS Distance")
    plot_summary(df, 'R_exp', output_folder, "LogLik_PL_vs_Exp")
    plot_summary(df, 'R_lognormal', output_folder, "LogLik_PL_vs_LN")
    plot_summary(df, 'R_truncPL', output_folder, "LogLik_PL_vs_TruncPL")
    plot_summary(df, 'R_trunc_vs_LN', output_folder, "LogLik_TruncPL_vs_LN")
    
    return mdata

def plot_summary(df, yvar, output_folder, fname):
    color_map = {'pruning':'blue', 'death':'seagreen'}
    df.plot.scatter(x='giteration', y=yvar, c=df['stage'].map(color_map), style='o')
    plt.savefig(output_folder + "/Summary/" + fname + ".png")
    

#####################
    
# Specify the folders where the network files are, it will save all summary graphs for each one in the corresponding folder
    
base_folder = "/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Storage/Large Nets/100k/"

folders = glob(base_folder + "/*/Edges/")
folders2 = folders[:]
#folders = folders2[0:10]
folders = [
        "/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Storage/Large Nets/100k/Sim 1/Edges/",
"/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Storage/Large Nets/100k/Sim 5/Edges/",
"/home/kleber/Dropbox/Scientific Research/Projects/Networks of Neurons - Death and Pruning/Complex Networks 2010 - Storage/Large Nets/100k/Sim 19/Edges/"
]
    
for folder in folders:
    fit_nets(folder, save_graphs = True)
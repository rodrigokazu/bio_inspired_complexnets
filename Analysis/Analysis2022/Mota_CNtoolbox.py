# Neural Pathways Laboratory #
# University of Sheffield - University of Brazil (Federal University of Rio de Janeiro) #

# Toolbox for relevant metric-extraction from biologically inspired complex networks #

# ----------------------------------------------------------------------------------------------------------------- #

# Written by Dr Rodrigo Kazu #
# Any enquiries to r.siqueiradesouza@sheffield.ac.uk #

# ----------------------------------------------------------------------------------------------------------------- #

import numpy as np
import time
import threading
from igraph import *


def analyse_50nets(fiftynets):

    """ Runs the analysis for the networks modelled at 50k neurons density and export results;
        This function initiates all the threads and run the analysis in parallel for the same network;
        The .join() function guarantees that all threads will finish at the same time

             Arguments:

                 fiftynets(list): Path for the networks to be analysed generated with the network_acquisition() function
                  of this toolbox.

           Returns:

              Exported complex network statistics.

|   """

    t1 = threading.Thread(target=parallel_cluster_50k, args=(fiftynets,))
    t2 = threading.Thread(target=parallel_averagepath_50k, args=(fiftynets,))
    #t3 = threading.Thread(target=parallel_shortestpath_50k, args=(fiftynets,))

    t1.start()
    #t2.start()
    #t3.start()

    t1.join()
    t2.join()
    #t3.join()


def network_density_paths(main_path):

    """ Acquires the paths to the biologically-inspired networks of 100k and 50k densities for further analysis

             Arguments:

                 main_path(str): Paths to the directory where the networks are stored

           Returns:

              Networks paths for 50k and 100k density simulations
             """

    fifty = main_path + "\\50k\\"
    hundred = main_path + "\\100k\\"

    fiftysims = os.listdir(fifty)
    hundredsims = os.listdir(hundred)

    fiftysims_paths = list()
    hundredsims_paths = list() # To export a list with the Sim folders "Sim 1", "Sim 2", etc.

    for sim in fiftysims:

        path = fifty + sim
        fiftysims_paths.append(path)

    for sim in hundredsims:

        path = hundred + sim
        hundredsims_paths.append(path)

    return fiftysims_paths, hundredsims_paths


def network_acquisition(density_path):

    """ Acquires the paths to the biologically-inspired networks for further analysis

          Arguments:

              density_path(str): Paths to the directory where the networks of correct density are stored

        Returns:

           Networks path and list containing all the network files

        """

    paths = density_path  # A list with the Sim folders "Sim 1", "Sim 2", etc.


    all_sims = dict()

    for path in paths:

        edges_path = path + "\\Edges\\"  # This is the folder structure chosen

        nets = os.listdir(edges_path)  # Obtains all the files in the folder.
        net_paths = list()

        for net in nets:

            network_file = edges_path + net
            net_paths.append(network_file)

        if path[-5] == "S":

            all_sims[path[-5:]] = net_paths

        else:

            all_sims[path[-6:]] = net_paths

    return all_sims


def parallel_averagepath_50k(fiftynets):

    """ Computes the average path length for a list of networks generated with network_acquisition()

              Arguments:

                  fiftynets(list): List of networks generated with network_acquisition()

            Returns:

               Average path length

            """
    for Sim in fiftynets:  # Fifty nets is a dict with Sims as keys

        for nets in fiftynets[Sim]:

            print("Average path calculations for ", nets)

            net = Graph.Read(nets)

            net_vcount = net.vcount()
            net_ecount = net.ecount()

            print("Nodes:", net_vcount)
            print("Edges:", net_ecount)

            start = time.perf_counter()
            print(f"[Path calculation started]")
            print(f"[Calculating average path length on thread number ] {threading.current_thread()}")
            path = net.average_path_length()  # Target is what's running on the new thread

            finish = time.perf_counter()
            print(f'Finished in {round(finish - start, 2)} seconds (s) and the average path length is {path}')

    return path


def parallel_cluster_50k(fiftynets):

    """ Computes the clustering coefficient for a list of networks generated with network_acquisition()

                 Arguments:

                     fiftynets(list): List of networks generated with network_acquisition()

               Returns:

                Clustering coefficient

   """
    for Sim in fiftynets:  # Fifty nets is a dict with Sims as keys

        for nets in fiftynets[Sim]:

            print("Clustering calculations for ", nets)
            net = Graph.Read(nets)

            net_vcount = net.vcount()
            net_ecount = net.ecount()

            print("Nodes:", net_vcount)
            print("Edges:", net_ecount)

            start = time.perf_counter()
            print(f"[Cluster calculation started]")
            print(f"[Calculating transitivity on thread number ] {threading.current_thread()}")
            clustering = net.transitivity_undirected()  # Target is what's running on the new thread
            finish = time.perf_counter()
            print(f'Finished in {round(finish - start, 2)} seconds (s) and the clustering coefficient is {clustering}')

    return clustering


def parallel_shortestpath_50k(fiftynets):

    """ Computes the shortest path length for a list of networks generated with network_acquisition()

                 Arguments:

                     fiftynets(list): List of networks generated with network_acquisition()

               Returns:

                  Shortest path length

   """

    for Sim in fiftynets:  # Fifty nets is a dict with Sims as keys

        for nets in fiftynets[Sim]:

            print("Shortest path calculations for ", nets)

            net = Graph.Read(nets)

            net_vcount = net.vcount()
            net_ecount = net.ecount()

            print("Nodes:", net_vcount)
            print("Edges:", net_ecount)

            start = time.perf_counter()
            print(f"[Path calculation started]")
            print(f"[Calculating average path length on thread number ] {threading.current_thread()}")
            path = np.mean(net.shortest_paths())  # Target is what's running on the new thread

            finish = time.perf_counter()
            print(f'Finished in {round(finish - start, 2)} seconds (s) and the shortest path length is {path}')

    return path


def write_metrics(shortestpath, averagepath, clustering):



    return 0
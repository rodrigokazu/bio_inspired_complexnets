# Neural Pathways Laboratory #
# University of Sheffield - University of Brazil (Federal University of Rio de Janeiro) #

# Toolbox for relevant metric-extraction from biologically inspired complex networks #

# ----------------------------------------------------------------------------------------------------------------- #

# Written by Dr Rodrigo Kazu #
# Any enquiries to r.siqueiradesouza@sheffield.ac.uk #

# ----------------------------------------------------------------------------------------------------------------- #

import time
import threading
from igraph import *


def network_density_paths(main_path):

    """ Acquires the paths to the biologically-inspired networks of 100k and 50k densitiesfor further analysis

             Arguments:
                 main_path(str): Paths to the directory where the recordings are stored in folders with the MEA
                 number.

           Returns:

              Networks paths for 50k and 100k density simulations
             """

    fifty = main_path + "\\50k\\"
    hundred = main_path + "\\100k\\"

    fiftysims = os.listdir(fifty)
    hundredsims = os.listdir(hundred)

    fiftysims_paths = list()
    hundredsims_paths = list()

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
              main_path(str): Paths to the directory where the recordings are stored in folders with the MEA
              number.

        Returns:

           Networks path and list containing all the network files
          """
    paths = density_path

    net_paths = list()

    for path in paths:

            edges_path = path + "\\Edges\\"

            nets = os.listdir(edges_path)

    for net in nets:

        network_file = edges_path + net
        net_paths.append(network_file)

    return net_paths


def parallel_path_50k(fiftynets):

    for nets in fiftynets:

        print("Path calculations for ", nets)

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
        print(f'Finished in {round(finish - start, 2)} seconds (s). and the path length is {path}')

    return 0


def parallel_cluster_50k(fiftynets):

    for nets in fiftynets:

        print("Cluster calculations for ", nets)
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
        print(f'Finished in {round(finish - start, 2)} seconds (s). and the clustering coefficient is {clustering}')

    return 0


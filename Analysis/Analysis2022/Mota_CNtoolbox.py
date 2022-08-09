# Neural Pathways Laboratory #
# University of Sheffield - University of Brazil (Federal University of Rio de Janeiro) #

# Toolbox for relevant metric-extraction from biologically inspired complex networks #

# ----------------------------------------------------------------------------------------------------------------- #

# Written by Dr Rodrigo Kazu #
# Any enquiries to r.siqueiradesouza@sheffield.ac.uk #

# ----------------------------------------------------------------------------------------------------------------- #

from igraph import *
from pathlib import Path
from os import listdir


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

        path = fifty + sim + "\\"
        fiftysims_paths.append(path)

    for sim in hundredsims:

        path = hundred + sim + "\\"
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


# Edit root folder accordingly #

main_path = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Projects\\complexnets\\complexnets_storage\\Large Nets"

paths = network_density_paths(main_path)

fiftynets = network_acquisition(paths[0])

hundrednets = network_acquisition(paths[1])


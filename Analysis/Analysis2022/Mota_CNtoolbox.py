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

              Networks path
             """

    fifty = main_path + "\\50k\\"
    hundred = main_path + "\\100k\\"

    return fifty, hundred

def network_acquisition(density_path):

    """ Acquires the paths to the biologically-inspired networks for further analysis

          Arguments:
              main_path(str): Paths to the directory where the recordings are stored in folders with the MEA
              number.

        Returns:

           Networks path and list containing all the network files
          """

    path = Path(main_path)

    net_paths = {}

    for path in path.iterdir():

        if path.is_dir():

            path_to_string = str(path)

            path_to_string = path_to_string + "\\Edges\\"

            nets = os.listdir(path_to_string)

    return path_to_string, nets


# Edit root folder accordingly #

main_path = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Projects\\complexnets\\complexnets_storage\\Large Nets"

paths = network_density_paths(main_path)

fiftynets = network_acquisition(paths[0])

hundrednets = network_acquisition(paths[1])

print(main_path)

from Mota_CNtoolbox import *


main_path = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Projects\\complexnets\\complexnets_storage\\Large Nets"

paths = network_density_paths(main_path)

fiftynets = network_acquisition(paths[0])
hundrednets = network_acquisition(paths[1])  # For reference

# Analysing the 50k networks for all simulations #

analyse_50nets(fiftynets)

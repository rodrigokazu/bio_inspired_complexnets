from Mota_CNtoolbox import *


main_path = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Projects\\complexnets\\complexnets_storage\\Large Nets"
exportpath50 = "C:\\Users\\me1rss\\Desktop\\50k_test\\"
exportpath100 = "C:\\Users\\me1rss\\Desktop\\100k_test\\"

paths = network_density_paths(main_path)

fiftynets = network_acquisition(paths[0])
hundrednets = network_acquisition(paths[1])  # For reference

# Analysing the networks for all simulations in different threads #

#analyse_allnets(allnets=fiftynets, exportpath=exportpath50)
analyse_allnets(allnets=hundrednets, exportpath=exportpath100)

#plot_degree_distribution(allnets=fiftynets, exportpath=exportpath50)


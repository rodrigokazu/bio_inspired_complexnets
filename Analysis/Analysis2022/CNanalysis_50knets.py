import threading
import igraph
from Mota_CNtoolbox import *


main_path = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Projects\\complexnets\\complexnets_storage\\Large Nets"

paths = network_density_paths(main_path)

fiftynets = network_acquisition(paths[0])

# Analysing the 50k networks for all simulations #

t1 = threading.Thread(target=parallel_cluster_50k, args=(fiftynets,))
t2 = threading.Thread(target=parallel_path_50k, args=(fiftynets,))

t1.start()
t2.start()
t1.join()
t2.join()

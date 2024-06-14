# Neural Pathways Laboratory #
# University of Sheffield - University of Brazil (Federal University of Rio de Janeiro) #

# Toolbox for relevant metric-extraction from biologically inspired complex networks #

# ----------------------------------------------------------------------------------------------------------------- #

# Written by Dr Rodrigo Kazu #
# Any enquiries to r.siqueiradesouza@sheffield.ac.uk #

# ----------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------------------------------------------- #
# In order to utilise this toolbox you will need the path of the folder where you want to export the results #

# AND #

# The path for the folder called 50k or 100k which contains the folders Sim 1 to Sim X with your simulations #

# ----------------------------------------------------------------------------------------------------------------- #

import Mota_CNtoolbox

"""
# Linux Paths #

main_path = "/home/rsiqueiradesouza/complexnets/complexnets_storage/Large Nets"
exportpath50 = "/home/rsiqueiradesouza/complexnets/repo/bio_inspired_complexnets/Analysis/Analysis2022/Results/50k/"
exportpath100 = "/home/rsiqueiradesouza/complexnets/repo/bio_inspired_complexnets/Analysis/Analysis2022/Results/100k/"
exportkeynets = "/home/rsiqueiradesouza/complexnets/repo/bio_inspired_complexnets/Analysis/Analysis2022/Results/keynets/"

"""
# Windows paths #

main_path = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Current projects\\complexnets\\dataset\\Large Nets"
exportpath50 = "C:\\Users\\me1rss\\Desktop\\50k_test\\"
exportpath100 = "C:\\Users\\me1rss\\Desktop\\100k_test\\"
pathdata = "C:\\Users\\me1rss\\Desktop\\50k_test\\AveragePath.csv"
dbexport = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Current projects\\complexnets\\Analysis_2023\\50k_nets\\"
datapath = ("C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Current projects\\complexnets\\Analysis_2023\\50k_nets"
            "\\GC.pkl")
exportkeynets = "C:\\Users\\me1rss\\Desktop\\keynets\\"
analysis2024 = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Current projects\\complexnets\\Analysis_2024\\"

# Key arguments for plotting and analysis #

to_overlay = ['Sim 1x', 'Sim 2x', "Sim 6x"]
legend = ["Our model", "Random Death", "Random Pruning"]
color = {"Sim 6x": "r", "Sim 2x": [1.0000, 0.4980, 0.], "Sim 1x": "b"}

# to_overlay = ['Sim 8x', 'Sim 7x', 'Sim 1x']  # FF
# legend = ["Feed-forwardness 50%", "Feed-forwardness 80%", "Feed-forwardness 100%"]  # FF
# sns.set_palette("Blues_r")  # FF


paths =Mota_CNtoolbox.network_density_paths(main_path)

fiftynets = Mota_CNtoolbox.network_acquisition(paths[0])
hundrednets = Mota_CNtoolbox.network_acquisition(paths[1])
keynets = Mota_CNtoolbox.network_acquisition(paths[2])  # For reference

#Mota_CNtoolbox.analyse_all(allnets=keynets, exportpath=exportkeynets)

Mota_CNtoolbox.plot_degree_distribution_ECDF(allnets=keynets, exportpath=analysis2024)



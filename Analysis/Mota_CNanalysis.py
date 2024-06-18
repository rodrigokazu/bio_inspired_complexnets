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
import time

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
datapath = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Current projects\\complexnets\\Analysis_2023\\50k_nets\\"
exportkeynets = "C:\\Users\\me1rss\\Desktop\\keynets\\"
analysis2024 = "C:\\Users\\me1rss\\Dropbox\\NeuralPathways\\Current projects\\complexnets\\Analysis_2024\\NN50000_syn100_pits5000\\"


paths =Mota_CNtoolbox.network_density_paths(main_path)

fiftynets = Mota_CNtoolbox.network_acquisition(paths[0])
#hundrednets = Mota_CNtoolbox.network_acquisition(paths[1])
keynets = Mota_CNtoolbox.network_acquisition(paths[1])  # For reference


# Key arguments for plotting and analysis #

"""
to_overlay = ['Sim 1y', 'Sim 2y', 'Sim 6y']
legend = ["Our model", "Random Death", "Random Pruning"]

"""
# FF arguments #

to_overlay = ['Sim 8y', 'Sim 7y', 'Sim 1y']  # FF
legend = ["Feed-forwardness 50%", "Feed-forwardness 80%", "Feed-forwardness 100%"]  # FF


color = {"Sim 8y": "#a5c2cf", "Sim 7y": "#4f81bd",  "Sim 1y": "#08306b",  "Sim 6y": "#993333", "Sim 2y": "#ff9966"}


# Actual analysis #

if __name__ == '__main__':

    start_time = time.time()
    Mota_CNtoolbox.plot_ALL_analysis(to_overlay=to_overlay, legend=legend, color=color, allnets=keynets,
                                     datapath=analysis2024, exportpath=analysis2024)
    end_time = time.time()

    print(f"Multiprocessing time taken: {end_time - start_time} seconds")



# Neural Pathways Laboratory #
# University of Sheffield - University of Brazil (Federal University of Rio de Janeiro) #

# Toolbox for relevant metric-extraction from biologically inspired complex networks #

# ----------------------------------------------------------------------------------------------------------------- #

# Written by Dr Rodrigo Kazu #
# Any enquiries to r.siqueiradesouza@sheffield.ac.uk #

# ----------------------------------------------------------------------------------------------------------------- #


import gc
import igraph
import logging
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import os
import pandas as pd
import pickle
import powerlaw
import random
import re
import seaborn as sns
import threading
import time

from scipy.sparse import csgraph, diags, csr_matrix
from scipy.sparse.linalg import eigsh
from joblib import Parallel, delayed


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


# ----------------------------------------------------------------------------------------------------------------- #
# In order to utilise this toolbox you will need the path of the folder where you want to export the results #

# AND #

# The path for the folder called 50k or 100k which contains the folders Sim 1 to Sim X with your simulations #

# For Linux replace all "//" with "\"

# ----------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------------------------------------------- #
# Data analysis #
# ----------------------------------------------------------------------------------------------------------------- #


def analyse_all(allnets, exportpath, **datapath):

    """ Runs the analysis for the networks modeled at 50k neurons density and export results;
        This function initiates all the processes and runs the analysis in parallel for the same network;
        The .join() function guarantees that all processes will finish at the same time

        Arguments:

            allnets(list): Path for the networks to be analyzed generated with the network_acquisition() function
            of this toolbox.

        Returns:

        Exported complex network statistics.
    """

    processes = [
        multiprocessing.Process(target=parallel_neun_syn_counts, args=(allnets, exportpath)),
        multiprocessing.Process(target=parallel_averagepaths, args=(allnets, exportpath)),
        multiprocessing.Process(target=parallel_clusters, args=(allnets, exportpath)),
        multiprocessing.Process(target=parallel_fitnet, args=(allnets, exportpath))]

    for process in processes:
        process.start()

    for process in processes:
        process.join()


def compute_fiedler(network_path):
    """ Computes the Fiedler value of a network

        Arguments:
            network_path (str): Path to the network file

        Returns:
            dict: A dictionary containing the Fiedler value and other relevant information
    """
    try:
        logging.info(f"Processing network: {network_path}")

        # Read the network
        net = igraph.Graph.Read_Edgelist(network_path)

        if net.vcount() < 2:  # Fiedler value is not defined for networks with less than 2 nodes
            logging.warning(f"Network {network_path} has less than 2 nodes.")
            return None

        # Get the adjacency matrix in sparse format
        adj_matrix = csr_matrix(net.get_adjacency().data)

        # Compute the Laplacian matrix
        laplacian = csgraph.laplacian(adj_matrix, normed=True)

        # Compute the second smallest eigenvalue (Fiedler value)
        eigenvalues, _ = eigsh(laplacian, k=2, which='SM')
        fiedler_value = eigenvalues[1]  # Second smallest eigenvalue

        # Extract labels
        label = network_labelling(network_path)

        return {
            "Simulation": label[0],
            "Network": network_path,
            "Iteration": int(label[1]),
            "FiedlerValue": fiedler_value
        }
    except Exception as e:
        logging.error(f"Error computing Fiedler value for {network_path}: {e}")
        return None


def fit_net(label, nets, Sim, exportpath, save_graphs=False):

    """
    Function that runs the Kolmogorov-Smirnov test

            Arguments:

                nets(str): Path of the network to be analysed
                Sim (str): Simulation number
                exportpath (str): Path where the plots and analysed data will be exported
                label(str): Output of the network_labelling() function

             Returns:

             Exported complex network statistics.

   """

    stage = re.search(r'(pruning|death)', label[0])[1]
    it = label[1]

    net = igraph.Graph.Read_Edgelist(nets)

    rem_nodes = len(net.vs.select(_degree_gt=0))  # net.vcount()
    rem_edges = net.ecount()

    if rem_edges < 100 or rem_nodes < 100:
        return "NULL"

    x = [t[2] for t in list(net.degree_distribution().bins())]

    del net
    gc.collect()

    #    fit = powerlaw.Fit(x, xmin = 1, xmax = max(x)/10)
    fitfull = powerlaw.Fit(x, xmin=1, xmax=max(x))
    fit = fitfull

    if save_graphs != False:

        fig = plt.figure()
        fig = fit.plot_pdf(color='b', linewidth=2)
        #        fig2 = fitfull.plot_pdf(color = 'b', linewidth = 2)
        #        fit.power_law.plot_pdf(color = 'b', linestyle = '--', ax = fig2)
        fit.power_law.plot_pdf(color='b', linestyle='--', ax=fig)

        plt.suptitle(stage.capitalize() + ", iteration #" + it, fontsize=18, y=1.02)
        plt.title("N = " + str(rem_nodes) + "; S = " + str(rem_edges) + "; alpha = " + str(
            round(fit.power_law.alpha, 3)) + "; D = " + str(round(fit.power_law.D, 3)), fontsize=14)
        #        plt.axvline(x = max(x)/10, color = '0.6', linestyle = ':')

        plt.savefig(exportpath+"Degree_Dist/"+"FIT"+str(Sim)+"_"+str(stage.capitalize()) + ", iteration #" + str(it)+'.png', bbox_inches='tight')
        plt.close(fig)

    rlist = [round(fit.power_law.alpha, 4), round(fit.power_law.D, 4)]

    R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    rlist.extend([round(R, 4), round(p, 4)])

    R, p = fit.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    rlist.extend([round(R, 4), round(p, 4)])

    R, p = fit.distribution_compare('power_law', 'truncated_power_law', normalized_ratio=True)
    rlist.extend([round(R, 4), round(p, 4)])

    R, p = fit.distribution_compare('truncated_power_law', 'lognormal', normalized_ratio=True)
    rlist.extend([round(R, 4), round(p, 4)])

    return stage, int(it), fit.power_law.alpha, fit.power_law.D


def inspect_data_structure(data, name):

    print(f"Inspecting data structure for {name}:")

    if isinstance(data, dict):

        for key, value in data.items():
            print(f"Key: {key}, Type: {type(value)}")
            if isinstance(value, list):
                print(f"First element type: {type(value[0])} if the list is not empty.")
            elif isinstance(value, dict):
                for k, v in value.items():
                    print(f"  Subkey: {k}, Type: {type(v)}")
            break

    elif isinstance(data, list):

        print(f"First element type: {type(data[0])} if the list is not empty.")
    else:

        print(f"Type: {type(data)}")


def load_and_concatenate_data(datapath, data_type):
    """
    Load the pickled file and structure the data into a dictionary with simulation names as keys,
    each containing two lists: iterations and syn values (for 'neun_syn') or appropriate fields for
    'clustering' and 'averagepaths'.

    Arguments:
        datapath (str): Path to the directory containing the pickled files.
        data_type (str): Type of data to load ('averagepaths', 'clustering', or 'neun_syn').

    Returns:
        dict: A dictionary with simulation names as keys and a dictionary containing two lists
              ('iterations', 'syn_values') as values for 'neun_syn' or appropriate fields for other types.
    """

    data_files = {
        'averagepaths': 'averagepaths.pkl',
        'clustering': 'clustering.pkl',
        'neun_syn': 'NeuN_Syn.pkl'
    }

    # Define the key to extract values based on data type
    value_key_map = {
        'averagepaths': 'AveragePathLength',
        'clustering': 'Clustering',
        'neun_syn': 'Syn'  # Assuming we are interested in Syn values
    }

    value_key = value_key_map[data_type]  # Get the key to extract the values

    if data_type not in data_files:

        raise ValueError("Invalid data_type. Choose from 'averagepaths', 'clustering', or 'neun_syn'.")

    file_path = os.path.join(datapath, data_files[data_type])

    with open(file_path, 'rb') as file:
        data = pickle.load(file)

    result = {}

    if data_type == 'neun_syn':
        for sim_name, sim_data in data.items():
            # Initialize lists for iterations and syn values
            iterations = []
            syn_values = []

            # Extract and process the fields as specified
            it_d = sim_data.get('it_d', [])
            syn_d = sim_data.get('syn_d', [])
            it_p = sim_data.get('it_p', [])
            syn_p = sim_data.get('syn_p', [])

            # Directly add 'it_d' and 'syn_d' values to the lists
            iterations.extend(it_d)
            syn_values.extend(syn_d)

            # Add 550 to 'it_p' values and then add to the iterations list
            altered_it_p = [x + 550 for x in it_p]
            iterations.extend(altered_it_p)

            # Add 'syn_p' values to the syn values list
            syn_values.extend(syn_p)

            # Store the extracted and processed data in the result dictionary
            result[sim_name] = {
                'iterations': iterations,
                'syn_values': syn_values
            }

    elif data_type == 'clustering' or data_type == 'averagepaths': # For averagepaths and clustering data, iterate over list elements

        concatenated_data = dict()

        for sim_data in data:
            Sim = sim_data.get("Simulation")
            iterations = np.array(sim_data["Iteration"])
            values = np.array(sim_data.get(value_key, []))
            label = sim_data.get("Label", "")

            # Ensure both arrays are at least 1-dimensional
            if iterations.ndim == 0:
                iterations = np.expand_dims(iterations, axis=0)
            if values.ndim == 0:
                values = np.expand_dims(values, axis=0)

            if Sim not in concatenated_data:
                concatenated_data[Sim] = ([], [])

            # Adjust iterations if the label indicates pruning
            adjusted_iterations = iterations + 550 if 'pruning' in label.lower() else iterations

            # Extend the lists with the new data
            concatenated_data[Sim][0].extend(adjusted_iterations.tolist())
            concatenated_data[Sim][1].extend(values.tolist())

        # Store the extracted and processed data in the result dictionary
        result = concatenated_data

    return result


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

        edges_path = path + "/Edges/"  # This is the folder structure chosen

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


def network_density_paths(main_path):

    """ Acquires the paths to the biologically-inspired networks of 100k and 50k densities for further analysis
    You will need to comment \ uncomment or remove the lines referring to keynets depending on your needs

             Arguments:

                 main_path(str): Paths to the directory where the networks are stored

           Returns:

              Networks paths for 50k and 100k density simulations
             """

    fifty = main_path + "/50k/"
    #hundred = main_path + "/100k/"
    keynets = main_path + "/keynets/"

    print(keynets)

    fiftysims = os.listdir(fifty)
    #hundredsims = os.listdir(hundred)
    keynetssims = os.listdir(keynets)


    keynetssims_paths = list()
    fiftysims_paths = list()
    #hundredsims_paths = list()  # To export a list with the Sim folders "Sim 1", "Sim 2", etc.

    for sim in fiftysims:

        if sim != "Degree_Dist":

            path = fifty + sim
            fiftysims_paths.append(path)

    #for sim in hundredsims:

        #path = hundred + sim
        #hundredsims_paths.append(path)

    for sim in keynetssims:

        path = keynets + sim
        keynetssims_paths.append(path)

    return fiftysims_paths, keynetssims_paths #, hundredsims_paths


def parallel_averagepaths(allnets, exportpath):

    """ Computes the average path length for a list of networks generated with network_acquisition()

        Arguments:
            allnets (list): List of networks generated with network_acquisition()
            exportpath (str): Path to export the dataset as a csv

        Returns:
            Average path exported as csv
    """

    averagepaths = []

    for Sim in allnets:

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)
                path = net.average_path_length()

                print(f'The ASPL for simulation {Sim} network {nets} is {path}')

                label = network_labelling(nets)

                record = {
                    "Simulation": Sim,
                    "Network": nets,
                    "Label": label[0],
                    "Iteration": int(label[1]),
                    "AveragePathLength": path
                }

                if re.search(r'(pruning|death)', label[0]):

                    if 'death' in label[0]:
                        record["Type"] = "death"
                    else:
                        record["Type"] = "pruning"

                averagepaths.append(record)

                del net
                gc.collect()

    df = pd.DataFrame(averagepaths)
    df.to_csv(os.path.join(exportpath, 'AveragePath.csv'), index=False)

    with open(os.path.join(exportpath, 'averagepaths.pkl'), 'wb') as fp:
        pickle.dump(averagepaths, fp)

    print('Average paths saved successfully to file')

    return averagepaths


def parallel_clusters(allnets, exportpath):

    """ Computes the clustering coefficient for a list of networks generated with network_acquisition()

        Arguments:
            allnets (list): List of networks generated with network_acquisition()
            exportpath (str): Path to export the dataset as a csv

        Returns:
            Clustering coefficients exported as csv
    """
    averagecluster = []

    for Sim in allnets:

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)
                clustering = net.transitivity_undirected()
                print(f'The clustering coefficient for simulation {Sim} network {nets} is {clustering}')

                label = network_labelling(netpath=nets)

                record = {
                    "Simulation": Sim,
                    "Network": nets,
                    "Label": label[0],
                    "Iteration": int(label[1]),
                    "Clustering": clustering
                }

                if re.search(r'(pruning|death)', label[0]):

                    if 'death' in label[0]:
                        record["Type"] = "death"
                    else:
                        record["Type"] = "pruning"

                averagecluster.append(record)

                del net
                gc.collect()

    df = pd.DataFrame(averagecluster)
    df.to_csv(os.path.join(exportpath, 'AverageClustering.csv'), index=False)

    with open(os.path.join(exportpath, 'clustering.pkl'), 'wb') as fp:
        pickle.dump(averagecluster, fp)

    print('Clustering coefficients saved successfully to file')
    return averagecluster


def parallel_density(allnets, exportpath):

    """ Computes the density for a list of networks generated with network_acquisition()
    The density of a igraph.Graph is simply the ratio of the actual number of its edges and the largest possible number of
    edges it could have. The maximum number of edges depends on interpretation: are vertices allowed to be connected to
     themselves? This is controlled by the loops parameter.

                 Arguments:

                     allnets(list): List of networks generated with network_acquisition()

               Returns:

                  CSV of densities for all networks and simulations

   """
    alldensities = dict()

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        alldensities[Sim] = dict()

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)

                print(f'Computing density for {nets}')
                print(f"[Calculating density on thread number ] {threading.current_thread()}")
                density = net.density(loops=False)

                print(f'The density is {density}')

                label = network_labelling(netpath=nets)
                name = "Density.csv"

                alldensities[Sim][label[0]] = density

                del net
                gc.collect()

        print(f'Writing to *.csv')
        write_metrics(metric=alldensities, exportpath=exportpath, name=name, label=label)

    return density


def parallel_fiedler_value(allnets, exportpath):
    """ Computes the Fiedler value (algebraic connectivity) for a list of networks generated with network_acquisition()

        Arguments:
            allnets (list): List of networks generated with network_acquisition()
            exportpath (str): Path to export the dataset as a csv

        Returns:
            CSV of Fiedler values for all networks and simulations
    """

    all_net_paths = [(Sim, net) for Sim in allnets for net in allnets[Sim] if os.path.getsize(net) > 0]
    logging.info(f"Total networks to process: {len(all_net_paths)}")

    fiedler_values = Parallel(n_jobs=-1)(delayed(compute_fiedler)(net) for Sim, net in all_net_paths)

    # Filter out None values
    fiedler_values = [fv for fv in fiedler_values if fv is not None]

    if not fiedler_values:
        logging.error("No valid Fiedler values were computed.")
        return None

    df = pd.DataFrame(fiedler_values)
    df.to_csv(os.path.join(exportpath, 'FiedlerValues.csv'), index=False)

    with open(os.path.join(exportpath, 'fiedler_values.pkl'), 'wb') as fp:
        pickle.dump(fiedler_values, fp)

    logging.info('Fiedler values saved successfully to file')

    return fiedler_values


def parallel_fitnet(allnets, exportpath):

    """ Fits the power law for a list of networks generated with network_acquisition()

      Arguments:

          allnets(list): List of networks generated with network_acquisition()
          exportpath(str): Path to export the dataset as a csv

           Returns:

            Fits

        """

    fits = dict()

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        fits[Sim] = dict()
        alpha_D_list = list()

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                label = network_labelling(nets)

                print(f'Computing fits for {nets}')

                alpha_D = fit_net(label=label, nets=nets, exportpath=exportpath, Sim=Sim, save_graphs=False)

                name = "Fits.csv"

                fits[Sim][label[0]] = alpha_D
                alpha_D_list.append(alpha_D)

                gc.collect()

        export = exportpath + 'Alpha_D.pkl'

        with open(export, 'wb') as fp:

            pickle.dump(fits, fp)

            print('Measure Alpha_D saved successfully to file')  # saving it because of time required to run

        print(f'Writing to *.csv')
        write_metrics(metric=fits, exportpath=exportpath, name=name, label=label)

    return 0


def parallel_giantcomponents(allnets, exportpath):

    """ Computes the giant compnent for a list of networks generated with network_acquisition()

                 Arguments:

                     allnets(list): List of networks generated with network_acquisition()

               Returns:

                  CSV of giant components for all networks and simulations

   """
    gcs = dict()

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        gcs[Sim] = dict()
        gcs[Sim + " iterations"] = list()
        gcs[Sim]["it_d"] = list()
        gcs[Sim]["it_p"] = list()
        gcs[Sim]["gc_d"] = list()
        gcs[Sim]["gc_p"] = list()

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)

                print(f'Computing giant component for {nets}')
                print(f"[Calculating GC on thread number ] {threading.current_thread()}")

                # giant component size
                _gc = net.as_undirected().decompose(mode=igraph.WEAK, maxcompno=1, minelements=2)[0]
                _gcs = len(_gc.vs)

                print(f'The GC is {_gcs}')

                label = network_labelling(netpath=nets)
                name = "GC.csv"

                gcs[Sim][label[0]] = _gcs

                gcs[Sim][label[0]] = _gcs
                gcs[Sim + " iterations"].append(label[0])

                if re.search(r'(pruning|death)', label[0])[1] == 'death':

                    gcs[Sim]["it_d"].append(int(label[1]))
                    gcs[Sim]["gc_d"].append(_gcs)

                else:

                    gcs[Sim]["it_p"].append(int(label[1]))
                    gcs[Sim]["gc_p"].append(_gcs)

                del net
                gc.collect()

        print(f'Writing to *.csv')
        print(f'Done for {Sim}')

        with open('GC.pkl', 'wb') as fp:

            pickle.dump(gcs, fp)

            print('Giant component size saved successfully to file')  # saving it because of time required to run

        write_metrics(metric=gcs, exportpath=exportpath, name=name, label=label)

    return gcs


def parallel_neun_syn_counts(allnets, exportpath):

    """ Original function written by Dr Kleber Neves to compute numbers of neurons and synapses per simulation

        Arguments:

         allnets(list): List of networks generated with network_acquisition()

        Returns:

          CSV of giant components for all networks and simulations

    """
    labels = {}
    NeuN_Syn = {}
    neurons_per_it = {}
    neurons_over_1_per_it = {}
    synapses_per_it = {}

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        neurons_per_it[Sim] = list()
        neurons_over_1_per_it[Sim] = list()
        synapses_per_it[Sim] = list()
        labels[Sim] = list()
        NeuN_Syn[Sim] = list()
        it = list()
        it_d = list()
        it_p = list()
        neun_d = list()
        neun_p = list()
        syn_d = list()
        syn_p = list()
        stage = list()

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)

                label = network_labelling(netpath=nets)

                # store number of neurons, synapses
                neurons_per_it[Sim].append(len(net.vs.select(_degree_gt=0)))
                neurons_over_1_per_it[Sim].append((len(net.vs.select(_degree_gt=1))))
                synapses_per_it[Sim].append(net.ecount())
                stage.append(re.search(r'(pruning|death)', label[0])[1])
                it.append(int(label[1]))

                if re.search(r'(pruning|death)', label[0])[1] == 'death':

                    it_d.append(int(label[1]))
                    neun_d.append(len(net.vs.select(_degree_gt=0)))
                    syn_d.append(net.ecount())

                else:

                    it_p.append(int(label[1]))
                    neun_p.append(len(net.vs.select(_degree_gt=0)))
                    syn_p.append(net.ecount())

                labels[Sim].append(label[0])

                print(f'Acquiring counts for {Sim} "_" {nets}')

                del net
                gc.collect()

        NeuN_Syn[Sim] = {"Labels": labels, "Stage": stage, "Iteration": it, "NeuN": neurons_per_it[Sim], "Syn": synapses_per_it[Sim],
                         "Active_NeuN": neurons_over_1_per_it[Sim], "it_d": it_d, "it_p": it_p, "neun_d": neun_d, "neun_p": neun_p,
                         "syn_d": syn_d, "syn_p": syn_p}
        print(f'Simulation {Sim} network {nets}  has {NeuN_Syn[Sim]["NeuN"]} neurons and {NeuN_Syn[Sim]["Syn"]} synapses.')

    name = "NeuN_Syn_Meta.csv"
    write_metrics(metric=NeuN_Syn, exportpath=exportpath, name=name, label=label)

    pkl_file = exportpath + 'NeuN_Syn.pkl'

    with open(pkl_file, 'wb') as fp:

        pickle.dump(NeuN_Syn, fp)

        print('Measure NeuN_Syn saved successfully to file')  # saving it because of time required to run

    return NeuN_Syn


def parallel_robustness(allnets, exportpath):

    """ Computes the robustness (GC or the R metric) for a list of networks generated with network_acquisition()
        Please change the name of the output file

                 Arguments:

                     allnets(list): List of networks generated with network_acquisition()

               Returns:

                  CSV of the measure R for all networks and simulations

   """
    R = dict()
    GC = dict()
    to_overlay = ['Sim 1', 'Sim 2', 'Sim 6', 'Sim 8', 'Sim 7']
    name = "GC_R"
    option = "GC"  # can be R or GC

    for Sim in to_overlay:  # Fifty nets is a dict with Sims as keys

        sim_time = time.time()

        R[Sim] = dict()

        R[Sim + " iterations"] = list()
        R[Sim]["it_d"] = list()
        R[Sim]["it_p"] = list()
        R[Sim]["R_d"] = list()
        R[Sim]["R_p"] = list()

        GC[Sim] = dict()

        GC[Sim + " iterations"] = list()
        GC[Sim]["it_d"] = list()
        GC[Sim]["it_p"] = list()
        GC[Sim]["R_d"] = list()
        GC[Sim]["R_p"] = list()


        for nets in allnets[Sim]:

            net_time = time.time()

            # Initialising GC #

             # methods are FRD or RD or RB - Full random degree or recalculated degree or recalculated betweenness

            if os.path.getsize(nets) > 0:

                # Only resets the variables if the networks exists #

                sQsum = 0
                removed = 0
                sQcount = 0
                method = "FRD"

                net = igraph.Graph.Read(nets)
                OGnet = net.copy()

                print(f'Computing Robustness for {Sim} {nets}')
                print(f"[Calculating on thread number ] {threading.current_thread()}")

                label = network_labelling(netpath=nets)

                while net.vcount() != 1:

                    if method == "FRD":

                        degrees = net.degree()

                        net.delete_vertices(random.choice(range(len(degrees))))

                    if method == "RD":

                        degrees = net.degree()
                        sorted_neun = sorted(range(len(degrees)), key=lambda x: degrees[x], reverse=True)

                        net.delete_vertices(sorted_neun[0])

                    elif method == "RB":

                        bt = net.betweenness()
                        #sorted_bt = sorted(range(len(bt)), key=lambda x: bt[x], reverse=True)

                        # net.delete_vertices(sorted_bt[0])

                        net.delete_vertices(bt.index(max(bt)))

                    _decomposed = net.as_undirected().decompose(mode=igraph.WEAK, maxcompno=1, minelements=1)

                    if _decomposed:

                        _gc = _decomposed[0]
                        _gcs = len(_gc.vs)
                        GCv = _gcs

                    if option == "R":

                        sQ = _gcs/OGnet.vcount()

                        sQsum = sQsum + sQ
                        sQcount = sQcount + 1

                        removed = removed + 1

                        print('---------------------------------------------------------------------------------------')
                        print(f' GC: {_gcs} , sQsum: {sQsum}, sQcount: {sQcount} r (estimated): {sQsum/sQcount}')
                        print(f'Neuronal count is now {net.vcount()}. We removed {removed} nodes on net {Sim} {label[0]}. ')

                        instant_end_time = time.time()
                        elapsed_instant_time = instant_end_time - net_time

                        print(f'Net time: {elapsed_instant_time/60} minutes.')
                        print('---------------------------------------------------------------------------------------')

                        r = sQsum/sQcount

                        print(f'R for {Sim} {label[0]} is {r}')

                        R[Sim][label[0]] = r
                        R[Sim + " iterations"].append(label[0])

                        if re.search(r'(pruning|death)', label[0])[1] == 'death':

                            R[Sim]["it_d"].append(int(label[1]))
                            R[Sim]["R_d"].append(r)

                        else:

                            R[Sim]["it_p"].append(int(label[1]))
                            R[Sim]["R_p"].append(r)

                        net_end_time = time.time()
                        elapsed_net_time = net_end_time - net_time

                        print(f'Final net time: {elapsed_net_time/60} minutes.')

                        #del net
                        gc.collect()

                    elif option == "GC":

                        removed = removed + 1

                        print('---------------------------------------------------------------------------------------')
                        print(f' GC: {GCv} ')
                        print(f'Neuronal count is now {net.vcount()}. We removed {removed} nodes on net {Sim} {label[0]}.')

                        instant_end_time = time.time()
                        elapsed_instant_time = instant_end_time - net_time

                        print(f'Net time: {elapsed_instant_time / 60} minutes.')
                        print('---------------------------------------------------------------------------------------')

                        GC[Sim][label[0]] = GCv
                        GC[Sim + " iterations"].append(label[0])

                        if re.search(r'(pruning|death)', label[0])[1] == 'death':

                            GC[Sim]["it_d"].append(int(label[1]))
                            GC[Sim]["R_d"].append(GCv)

                        else:

                            GC[Sim]["it_p"].append(int(label[1]))
                            GC[Sim]["R_p"].append(GCv)

                        net_end_time = time.time()
                        elapsed_net_time = net_end_time - net_time

                        print(f'Final net time: {elapsed_net_time / 60} minutes.')

                        # del net
                        gc.collect()


        sim_end_time = time.time()
        elapsed_sim_time = sim_end_time - sim_time

        print(f'Simulation time: {elapsed_sim_time/60} minutes')

    with open('R_GC_FRD.pkl', 'wb') as fp:

        print(f'Writing to file')

        pickle.dump(GC, fp)

        print('Robustness (GC) saved successfully to file')  # saving it because of time required to run

    #write_metrics(metric=gcs, exportpath=exportpath, name=name, label=label)

    return GC


def write_metrics(metric, exportpath, name, label):

    """ Writes the results of the analysis for the networks modelled at 50k neurons density and export results;


         Arguments:

             averagepath(list): Dataset for the networks analysed

       Returns:

          Exported complex network statistics.

|   """

    df = pd.DataFrame(data=metric)
    file = exportpath + name
    df.to_csv(file, mode='a')

    return metric


# ----------------------------------------------------------------------------------------------------------------- #
# Data visualisation #
# ----------------------------------------------------------------------------------------------------------------- #

def plot_ALL_analysis(allnets, color, exportpath, legend, to_overlay, datapath):

    """
    Plots the analysis for the networks modelled at 50k neurons density and export results;
    This function initiates all the processes and runs the analysis in parallel for the same network;
    The .join() function guarantees that all processes will finish at the same time

    Arguments:
        allnets(list): Path for the networks generated with the network_acquisition() function of this toolbox for
        the overlayed scats function.
        datapath(str): Path for a folder where all the analyses generated with this toolbox are saved as *.pkl
        to_overlay(list): List of simulations to be plotted in the "Sim X" convention
        legend (list): List of words to compose the legend of the figures
        color (dict): Dict of colours for the plot with the "Sim X" convention as keys

    Returns:
        Overlayed plots.
    """

    #p1 = multiprocessing.Process(target=plot_degree_distribution_overlayedscats, args=(allnets, exportpath, to_overlay, legend, color))
    p2 = multiprocessing.Process(target=plot_pruningrate, args=(color, datapath, exportpath, legend, to_overlay))
    p3 = multiprocessing.Process(target=plot_clustering_lineplot, args=(color, datapath, exportpath, legend, to_overlay))
    p4 = multiprocessing.Process(target=plot_averagepath_lineplot, args=(color, datapath, exportpath, legend, to_overlay))
    p5 = multiprocessing.Process(target=plot_alpha_D, args=(datapath, exportpath))
    p6 = multiprocessing.Process(target=plot_synaptic_fraction_overlayed, args=(color, datapath, exportpath, legend, to_overlay))

    #p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    #p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()


def plot_alpha_D(datapath, exportpath):

    """ Original function written by Dr Kleber Neves to plot the degree distributions, customised for Alpha and D
    Alpha and D can be obtained using fit_net()

         Arguments:

            alpha_D (list): List of alphas and Ds
            exportpath(str): Path to export the dataset as a csv

       Returns:

          Plots of alphas vs Ds

   """

    data_path = datapath + "Alpha_D.pkl"

    with open(data_path, 'rb') as fp:  # The ** argument is imported as a dictionary

        fits = pickle.load(fp)


    for Sim in fits:

        # Creating relevant lists #

        overall_it = list()
        current_it = 0

        overall_alpha = list()
        overall_D = list()
        it_death = list()
        it_pruning = list()
        alpha_death = list()
        alpha_pruning = list()
        D_death = list()
        D_pruning = list()

        # Populate the lists with the content from alpha_D #

        alpha_D = fits[Sim]

        for label in alpha_D:

            if alpha_D[label][0] == "death":

                it_death.append(alpha_D[label][1])
                alpha_death.append(alpha_D[label][2])
                D_death.append(alpha_D[label][3])

                overall_it.append(current_it)
                overall_alpha.append(alpha_D[label][2])
                overall_D.append(alpha_D[label][3])

            else:

                it_pruning.append(alpha_D[label][1])
                alpha_pruning.append(alpha_D[label][2])
                D_pruning.append(alpha_D[label][3])

                overall_it.append(current_it)
                overall_alpha.append(alpha_D[label][2])
                overall_D.append(alpha_D[label][3])

            current_it = current_it + 1


        # Dealing with "L" and "U" outputs in a very inefficient way #

        delete_list_a_death = []
        delete_list_it_death = []
        delete_list_a_pruning = []
        delete_list_it_pruning = []

        for index in range(0, len(alpha_death)):

            if alpha_death[index] == "L":

                delete_list_a_death.append(index)

            if alpha_death[index] == "U":

                delete_list_a_death.append(index)

        for index in range(0, len(it_death)):

            if it_death[index] == "L":

                delete_list_it_death.append(index)

            if alpha_death[index] == "U":

                delete_list_it_death.append(index)

        for index in range(0, len(alpha_pruning)):

            if alpha_pruning[index] == "L":

                delete_list_a_pruning.append(index)

            if alpha_pruning[index] == "U":

                delete_list_a_pruning.append(index)

        for index in range(0, len(it_pruning)):

            if it_pruning[index] == "L":

                delete_list_it_pruning.append(index)

            if it_pruning[index] == "U":

                delete_list_it_pruning.append(index)

        for index in sorted(delete_list_a_death, reverse=True):

            del alpha_death[index]

        for index in sorted(delete_list_it_death, reverse=True):

            del it_death[index]

        for index in sorted(delete_list_a_pruning, reverse=True):

            del alpha_pruning[index]

        for index in sorted(delete_list_it_pruning, reverse=True):

            del it_pruning[index]

        if len(it_death) > 0:

            # Sorting the values of alpha to account for inconsistencies in the order of iterations
            sorted_alpha_d = [x for _, x in sorted(zip(it_death, alpha_death))]

        else:

            sorted_alpha_d = []

        sorted_alpha_p = [x for _, x in sorted(zip(it_pruning, alpha_pruning))]

        sorted_alpha = sorted_alpha_d + sorted_alpha_p

        # Sorting the values of D to account for inconsistencies in the order of iterations
        sorted_D_d = [x for _, x in sorted(zip(it_death, D_death))]
        sorted_D_p = [x for _, x in sorted(zip(it_pruning, D_pruning))]

        sorted_D = sorted_D_d + sorted_D_p

        # Dealing with the L and U outputs again

        delete_from_sorted = []

        it_pruning_copy = it_pruning

        for index in range(0, len(sorted_D)):

            if sorted_D[index] == "L":

                delete_from_sorted.append(index)

            if sorted_D[index] == "U":

                delete_from_sorted.append(index)

            # Dealing with "L" and "U" outputs

        if len(it_death) > 0:

            # concatenating death and pruning iterations
            it_pruning = np.array(it_pruning_copy)
            it_pruning = it_pruning + 500
            it_pruning = list(it_pruning)

        overall_it = it_death + it_pruning
        overall_it = sorted(overall_it)

        for index in sorted(delete_from_sorted, reverse=True):  # It doesn't seem to be getting in this loop half of the time

            del sorted_D[index]
            del sorted_alpha[index]
            del overall_it[index]


        # plots data

        fig = plt.figure(figsize=(5, 5), dpi=500)

        sns.set_style("ticks")
        sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 10, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=overall_it, y=sorted_alpha, markers=True, linewidth=4, color='r', label="Alpha")
        ax = sns.lineplot(x=overall_it, y=sorted_D, markers=True, linewidth=4, color='b', label="Distance")

        ax.set(ylim=[0, 3])
        ax.set_ylabel("Measure")
        ax.set_xlabel("Iteration")

        sns.despine()
        plt.legend()

        if Sim == "Sim 1":

            # sets labels
            ax.set_title("Mota's model")

        elif Sim == "Sim 2":

            ax.set_title("Random Death")

        elif Sim == "Sim 6":

            ax.set_title("Random Pruning")

        else:

            ax.set_title(str(Sim))

        # save to file
        if not os.path.exists(exportpath + "Alpha_D"):  # creates export directory

            os.makedirs(exportpath + "Alpha_D")

        plt.savefig(exportpath + "Alpha_D/" + str(Sim) + '.png', bbox_inches='tight')

        plt.close(fig)
        gc.collect()

    return 0


def plot_averagepath_lineplot(color, datapath, exportpath, legend, to_overlay):

    """
    Function to plot overlayed progression of average path length of three different conditions of the Mota's Model.

    Arguments:
        datapath (str): Path to the directory containing the pickled files.
        exportpath (str): Path to export the figures.
        color (dict): Dictionary mapping Sim values to colors.
        legend (list): List of legend labels.
        to_overlay (list): List of Sim values to overlay in the plot.

    Returns:
        int: 0 if successful.
    """
    concatenated_data = load_and_concatenate_data(datapath, 'averagepaths')

    fig = plt.figure(figsize=(5, 5), dpi=500)  # generating the figure

    for Sim in to_overlay:

        if Sim not in concatenated_data:
            continue

        overall_it, overall_syn = concatenated_data[Sim]

        # plots data
        print(f"----------------Plotting {Sim}---------------------")

        sns.set_style("ticks")

        sns.set_context(context="paper", rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=overall_it, y=overall_syn, markers=True, linewidth=2.5,
                          label=legend[to_overlay.index(Sim)], color=color[Sim])

        ax.axvline(x=500, ymin=0, ymax=7, linestyle="dashed", color="0.8")
        ax.axvspan(0, 500, alpha=0.05)
        sns.despine()

        plt.legend(loc=1)

    # sets labels
    ax.set_title("Average path length")
    ax.set_ylabel("Average path length")
    ax.set_xlabel("Iteration")
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 5500)

    # save to file
    if not os.path.exists(exportpath + "Average_paths"):  # creates export directory
        os.makedirs(exportpath + "Average_paths")

    plt.savefig(exportpath + "Average_paths/AP_FF" + "_".join(map(str, to_overlay)) + ".png", bbox_inches="tight")

    plt.close(fig)
    gc.collect()

    return 0


def plot_betweenness_centrality(allnets, exportpath):

    """ Original function written by Dr Kleber Neves to plot the degree distributions

       Arguments:

                 allnets(list): List of networks generated with network_acquisition()
                 exportpath(str): Path to export the figures

       Returns:

          Plots of degree distributions

   """

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)
                bc = net.betweenness()

                # get title
                t = network_labelling(netpath=nets)[0]

                print(f'---------------[[PLOTTING {t}]]---------------')

                fig = plt.figure(figsize=(5, 5), dpi=500)

                sns.set_style("ticks")

                sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                                        "lines.linewidth": 2, "xtick.labelsize": 8,
                                                        "ytick.labelsize": 8})

                # plots data
                ax = sns.scatterplot(data=bc)
                ax.set(yscale="log")
                #ax.set(yscale="log", xscale="log", ylim=[10 ** -0.2, 10 ** 4], xlim=[10 ** -0.2, 10 ** 4])

                # sets labels
                ax.set_title(str(Sim)+" "+t)
                ax.set_xlabel("Neuronal number")
                ax.set_ylabel("Betweenness Centrality")

                # save to file
                if not os.path.exists(exportpath + "Betweenness_centrality"):  # creates export directory

                    os.makedirs(exportpath + "Betweenness_centrality")

                plt.savefig(exportpath+"Betweenness_centrality/"+str(Sim)+"_"+t+'.png', bbox_inches='tight')
                plt.close(fig)

                del net
                gc.collect()


def plot_clustering_lineplot(color, datapath, exportpath, legend, to_overlay):

    """
    Function to plot overlayed progression of the clustering coefficient of three different conditions of the Mota's Model.

    Arguments:
        datapath (str): Path to the directory containing the pickled files.
        exportpath (str): Path to export the figures.
        color (dict): Dictionary mapping Sim values to colors.
        legend (list): List of legend labels.
        to_overlay (list): List of Sim values to overlay in the plot.

    Returns:
        int: 0 if successful.
    """
    concatenated_data = load_and_concatenate_data(datapath, 'clustering')

    fig = plt.figure(figsize=(5, 5), dpi=500)  # generating the figure

    for Sim in to_overlay:
        if Sim not in concatenated_data:
            continue

        overall_it, overall_syn = concatenated_data[Sim]

        # plots data
        print(f"----------------Plotting {Sim}---------------------")

        sns.set_style("ticks")

        sns.set_context(context="paper", rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=overall_it, y=overall_syn, markers=True, linewidth=2.5,
                          label=legend[to_overlay.index(Sim)], color=color[Sim])
        ax.set(yscale="log")
        ax.set_ylim(10**-5, 10**0)
        ax.axvline(x=500, ymin=0, ymax=1, linestyle="dashed", color="0.8")
        ax.axvspan(0, 500, alpha=0.05)
        sns.despine()

        plt.legend(loc='lower right')

    # sets labels
    ax.set_title("Average clustering coefficient")
    ax.set_ylabel("Clustering coefficient")
    ax.set_xlabel("Iteration")
    ax.set_xlim(0, 5500)

    # save to file
    if not os.path.exists(exportpath + "Clustering"):  # creates export directory
        os.makedirs(exportpath + "Clustering")

    plt.savefig(exportpath + "Clustering/CC_loglog" + "_".join(map(str, to_overlay)) + ".png", bbox_inches="tight")

    plt.close(fig)
    gc.collect()

    return 0


def plot_degree_distribution_line(allnets, exportpath):

    """ Original function written by Dr Kleber Neves to plot the degree distributions

        Arguments:

                 allnets(list): List of networks generated with network_acquisition()
                 exportpath(str): Path to export the dataset as a csv

       Returns:

          Plots of degree distributions

   """

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        fig = plt.figure(figsize=(5, 5), dpi=500)

        sns.set_style("ticks")

        sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        for nets in allnets[Sim]:

            net = igraph.Graph.Read(nets)
            dd = net.degree()

            # get title
            t = network_labelling(netpath=nets)[0]

            print(f'---------------[[PLOTTING {t}]]---------------')

            # plots data
            ax = sns.lineplot(data=np.bincount(dd))
            ax.set(yscale="log", xscale="log")
                   #ylim=[10 ** -0.2, 10 ** 4], xlim=[10 ** -0.2, 10 ** 4])

            del net
            gc.collect()

        # sets labels
        ax.set_title(str(Sim) + " " + t)
        ax.set_ylabel("Frequency")
        ax.set_xlabel("Degree")

        # save to file
        if not os.path.exists(exportpath + "Degree_Dist"):  # creates export directory

            os.makedirs(exportpath + "Degree_Dist")

        plt.savefig(exportpath+"Degree_Dist/"+str(Sim)+"_"+t+'.png', bbox_inches='tight')
        plt.close(fig)


def plot_degree_distribution_scatter(allnets, exportpath):

    """ Original function written by Dr Kleber Neves to plot the degree distributions

       Arguments:

                 allnets(list): List of networks generated with network_acquisition()
                 exportpath(str): Path to export the figures

       Returns:

          Plots of degree distributions

   """

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)
                dd = net.degree()

                # get title
                t = network_labelling(netpath=nets)[0]

                print(f'---------------[[PLOTTING {t}]]---------------')

                fig = plt.figure(figsize=(5, 5), dpi=500)

                sns.set_style("ticks")

                sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                                        "lines.linewidth": 2, "xtick.labelsize": 8,
                                                        "ytick.labelsize": 8})

                # plots data
                ax = sns.scatterplot(data=np.bincount(dd))
                ax.set(yscale="log", xscale="log", ylim=[10 ** -0.2, 10 ** 4], xlim=[10 ** -0.2, 10 ** 4])

                # sets labels
                ax.set_title(str(Sim)+" "+t)
                ax.set_ylabel("Frequency")
                ax.set_xlabel("Degree")

                # save to file
                if not os.path.exists(exportpath + "Degree_Dist"):  # creates export directory

                    os.makedirs(exportpath + "Degree_Dist")

                plt.savefig(exportpath+"Degree_Dist/"+str(Sim)+"_"+t+'.png', bbox_inches='tight')
                plt.close(fig)

                del net
                gc.collect()


def plot_degree_distribution_ECDF(allnets, exportpath):

    """ ECDF plots of the degree distributions

         Arguments:

                   allnets(list): List of networks generated with network_acquisition()
                   exportpath(str): Path to export the figures

         Returns:

            Plots of degree distributions

     """

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)
                dd = net.degree()

                # get title
                t = network_labelling(netpath=nets)[0]

                print(f'---------------[[PLOTTING {t}]]---------------')

                fig = plt.figure(figsize=(5, 5), dpi=500)

                sns.set_style("ticks")

                sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                                     "lines.linewidth": 2, "xtick.labelsize": 8,
                                                     "ytick.labelsize": 8})

                # plots data
                ax = sns.ecdfplot(data=np.bincount(dd))

                ax.set(yscale="log", xscale="log", ylim=[10 ** -0.5, 10 ** 0.5], xlim=[10 ** -0.2, 10 ** 4])

                # sets labels
                ax.set_title(str(Sim) + " " + t)
                ax.set_ylabel("Frequency")
                ax.set_xlabel("Degree")

                # save to file
                if not os.path.exists(exportpath + "Degree_Dist"):  # creates export directory

                    os.makedirs(exportpath + "Degree_Dist")

                plt.savefig(exportpath + "Degree_Dist/" + str(Sim) + "_" + t + 'ECDF.png', bbox_inches='tight')
                plt.close(fig)

                del net
                gc.collect()


def plot_degree_distribution_overlayedscats(allnets, exportpath, to_overlay, legend, color):

    """ Function to plot overlayed scatter plots of degree distribuitions of three different conditions of the
     Mota's Model

     Arguments:

             allnets(list): List of networks generated with network_acquisition()
             exportpath(str): Path to export the figures
             to_overlay(list): List of simulations to be plotted in the "Sim X" convention
             legend (list): List of words to compose the legend of the figures
             color (dict): Dict of colours for the plot with the "Sim X" convention as keys

       Returns:

          Plots of degree distributions

   """

    to_overlay = to_overlay
    legend = legend
    color = color

    Sim = 0

    for nets in range(0, len(allnets[to_overlay[Sim]])):

        fig = plt.figure(figsize=(5, 5), dpi=500)

        sns.set_style("ticks")

        sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8, "lines.markersize":9})

        if os.path.getsize(allnets[to_overlay[Sim]][nets]) > 0:

            net = igraph.Graph.Read(allnets[to_overlay[Sim]][nets])
            net2 = igraph.Graph.Read(allnets[to_overlay[Sim+1]][nets])
            net3 = igraph.Graph.Read(allnets[to_overlay[Sim + 2]][nets])

            dd_1 = net.degree()
            dd_2 = net2.degree()
            dd_3 = net3.degree()

            # get title
            t = network_labelling(netpath=allnets[to_overlay[Sim]][nets])[0]

            print(f'---------------[[PLOTTING {to_overlay[Sim]} {t}]]---------------')

            # get title
            t2 = network_labelling(netpath=allnets[to_overlay[Sim+1]][nets])[0]

            print(f'---------------[[PLOTTING {to_overlay[Sim + 1]} {t2}]]---------------')

            # get title
            t3 = network_labelling(netpath=allnets[to_overlay[Sim + 2]][nets])[0]

            print(f'---------------[[PLOTTING {to_overlay[Sim + 2]} {t3}]]---------------')

            # plots data
            ax = sns.scatterplot(data=np.bincount(dd_1), label=legend[Sim], color=color[to_overlay[Sim]])  # color="b"  label="Feed-forwardness 50%"
            ax = sns.scatterplot(data=np.bincount(dd_2), label=legend[Sim+1], color=color[to_overlay[Sim+1]])  # color=[1.0000, 0.4980, 0.]
            ax = sns.scatterplot(data=np.bincount(dd_3), label=legend[Sim+2], color=color[to_overlay[Sim+2]])  # color="r"
            sns.despine()
            ax.set(yscale="log", xscale="log", ylim=[10 ** -0.2, 10 ** 4.5], xlim=[10 ** -0.2, 10 ** 4])

            # sets labels
            ax.set_title("Degree distributions for iteration " + t)
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Degree")
            ax.legend()

        # save to file
        if not os.path.exists(exportpath + "Degree_Dist"):  # creates export directory

            os.makedirs(exportpath + "Degree_Dist")

        plt.savefig(exportpath + "Degree_Dist/" + str(to_overlay[Sim]) + "_" + str(to_overlay[Sim+1]) + "_" + str(to_overlay[Sim+2]) + "_" + t + '.png', bbox_inches='tight')

        plt.close(fig)

        del net
        gc.collect()


def plot_fiedler_values(datapath, exportpath):

    """ Plots the Fiedler values for different simulations

        Arguments:
            datapath (str): Path to the pickled file exported by parallel_fiedler_value
            exportpath (str): Path to export the figures

        Returns:
            Plots of Fiedler values
    """

    data_path = datapath + "fiedler_values.pkl"

    with open(data_path, 'rb') as fp:  # Load the Fiedler values
        fiedler_values = pickle.load(fp)

    for Sim in fiedler_values:
        iterations = []
        values = []

        for record in fiedler_values:
            if record['Simulation'] == Sim:
                iterations.append(record['Iteration'])
                values.append(record['FiedlerValue'])

        fig = plt.figure(figsize=(5, 5), dpi=500)
        sns.set_style("ticks")
        sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=iterations, y=values, markers=True, linewidth=2.5, label=Sim)
        ax.set_ylabel("Fiedler Value")
        ax.set_xlabel("Iteration")
        ax.set_title(f"Fiedler Values for {Sim}")
        sns.despine()
        plt.legend()

        if not os.path.exists(exportpath + "FiedlerValues"):
            os.makedirs(exportpath + "FiedlerValues")

        plt.savefig(exportpath + f"FiedlerValues/{Sim}.png", bbox_inches='tight')
        plt.close(fig)
        gc.collect()

    return 0


def plot_GC_overlayed(datapath, exportpath):

    """ Function to plot overlayed progression of the giant component size of three different conditions of the Mota's Model


        Arguments:

               datapath (dict): Path to the pickled file exported by parallel_giantcomponent(allnets, exportpath)
               exportpath(str): Path to export the figures

          Returns:

             Plots of degree distributions

      """

    to_overlay = ['Sim 1', 'Sim 2', 'Sim 6']  # Model conditions, 'Sim 6'
    legend = ["Mota's model", "Random Death", "Random Pruning"]  # Model conditions , "Random Pruning"
    color = {"Sim 6": "r", "Sim 2": [1.0000, 0.4980, 0.], "Sim 1": "b"}
    #to_overlay = ['Sim 8', 'Sim 7', 'Sim 1']  # FF
    #legend = ["Feed-forwardness 50%", "Feed-forwardness 80%", "Feed-forwardness 100%"]  # FF
    #sns.set_palette("Blues_r")  # FF

    with open(datapath, 'rb') as fp:  # The ** argument is imported as a dictionary

        gcs = pickle.load(fp)

    fig = plt.figure(figsize=(5, 5), dpi=500)  # generating the figure
    # sns.set_palette("Blues_r")

    for Sim in to_overlay:

        it_pruning = np.array(gcs[Sim]['it_p'])
        it_pruning = it_pruning + 500
        it_pruning = list(it_pruning)

        overall_it = gcs[Sim]['it_d'] + it_pruning
        overall_gc = gcs[Sim]['gc_d'] + gcs[Sim]['gc_p']

        overall_it_sorted, overall_gc_sorted = zip(*sorted(zip(overall_it, overall_gc)))

        # plots data

        print(f'----------------Plotting {Sim}---------------------')

        sns.set_style("ticks")

        sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=np.array(overall_it_sorted), y=np.array(overall_gc_sorted), markers=True, linewidth=2.5, color=color[Sim],
                          label=legend[to_overlay.index(Sim)])
        # color=color[Sim],
        ax.axvline(x=500,  ymin=0,  ymax=1, linestyle="dashed", color="0.8")
        ax.axvspan(0, 500, alpha=0.05)
        sns.despine()

        plt.legend(loc=1)

    Sim = 0

    # sets labels
    ax.set_title("Average GC size for different conditions")
    ax.set_ylabel("Giant component size")
    ax.set_xlabel("Iteration")
    ax.set_ylim(0, 51000)
    ax.set_xlim(0, 3000)


    # save to file
    if not os.path.exists(exportpath + "Giant Component"):  # creates export directory

        os.makedirs(exportpath + "Giant Component")

    plt.savefig(exportpath + "Giant Component/GC_" + str(to_overlay[Sim]) + "_" + str(to_overlay[Sim + 1]) + "_"
                + str(to_overlay[Sim + 2]) + '.png', bbox_inches='tight')

    plt.close(fig)
    gc.collect()

    return 0


def plot_pruningrate(color, datapath, exportpath, legend, to_overlay):

    to_overlay = to_overlay
    legend = legend
    color = color

    fig = plt.figure(figsize=(5, 5), dpi=500)

    sns.set_style("ticks")
    sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                         "lines.linewidth": 2, "xtick.labelsize": 8,
                                         "ytick.labelsize": 8})
    data_path = datapath + "NeuN_Syn.pkl"

    with open(data_path, 'rb') as fp:  # The ** argument is imported as a dictionary

        NeuN_Syn = pickle.load(fp)

    # Running through experimental conditions, i.e. Simulations #

    pruned_fraction = dict()

    for Sim in to_overlay:

        it_pruning = np.array(NeuN_Syn[Sim]['it_p'])
        pruned_fraction[Sim] = list()
        pruned_fraction[Sim].append(25)

        sorted_syn = [x for _, x in sorted(zip(it_pruning, NeuN_Syn[Sim]['syn_p']))]
        it_pruning = sorted(it_pruning)

        # Getting the percentages #

        for syn in range(1, len(NeuN_Syn[Sim]['syn_p'])):

            decimal = sorted_syn[syn]/sorted_syn[syn-1]
            pruned_fraction[Sim].append(100 - decimal*100)

        # plots data

        print(f'----------------Plotting {Sim}---------------------')

        ax = sns.lineplot(x=it_pruning, y=pruned_fraction[Sim], markers=True, linewidth=2.5,
                          label=legend[to_overlay.index(Sim)], color=color[Sim])
        ax.set_ylim(-0.005, 50)

        plt.legend(loc=1)
        sns.despine()

        # sets labels
        ax.set_title("Rate of synaptic pruning")
        ax.set_ylabel("Percentage of synapses removed")
        ax.set_xlabel("Iteration on the SP stage")

        # save to file
    if not os.path.exists(exportpath + "Pruning_Rate"):  # creates export directory

        os.makedirs(exportpath + "Pruning_Rate")

    plt.savefig(exportpath + "Pruning_Rate/Pruning_Rate_FF" + '.png', bbox_inches='tight')

    plt.close(fig)
    gc.collect()

    return 0


def plot_R_overlayed(exportpath, datapath):

    """ Function to plot overlayed progression of the R measure of three different conditions of the Mota's Model


        Arguments:

               datapath (dict): Path to the pickled file exported by parallel_averagepath(allnets, exportpath)
               exportpath(str): Path to export the figures

          Returns:

             Plots of degree distributions

      """

    #to_overlay = ['Sim 1', 'Sim 2', 'Sim 6'] # Model conditions
    #legend = ["Mota's model", "Random Death", "Random Pruning"] # Model conditions
    #color = {"Sim 6": "r", "Sim 2": [1.0000, 0.4980, 0.], "Sim 1": "b"}
    to_overlay = ['Sim 8', 'Sim 7', 'Sim 1']  # FF
    legend = ["Feed-forwardness 50%", "Feed-forwardness 80%", "Feed-forwardness 100%"]  # FF
    sns.set_palette("Blues_r")  # FF

    with open(datapath, 'rb') as fp:  # The ** argument is imported as a dictionary

        R = pickle.load(fp)

    fig = plt.figure(figsize=(5, 5), dpi=500)  # generating the figure


    for Sim in to_overlay:

        it_pruning = np.array(R[Sim]['it_p'])
        it_pruning = it_pruning + 500
        it_pruning = list(it_pruning)

        overall_it = R[Sim]['it_d'] + it_pruning
        overall_R = R[Sim]['R_d'] + R[Sim]['R_p']

        overall_it_sorted, overall_R_sorted = zip(*sorted(zip(overall_it, overall_R)))


        # plots data

        print(f'----------------Plotting {Sim}---------------------')

        sns.set_style("ticks")

        sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=np.array(overall_it_sorted), y=np.array(overall_R_sorted), markers=True, linewidth=2.5,
                          label=legend[to_overlay.index(Sim)])
        ax.axvline(x=500,  ymin=0,  ymax=1, linestyle="dashed", color="0.8")
        ax.axvspan(0, 500, alpha=0.05)

        plt.legend(loc=1)

    Sim = 0

    # sets labels
    ax.set_title("Robustness to targeted attacks")
    ax.set_ylabel("R")
    ax.set_xlabel("Iteration")
    ax.set_ylim(-0.005, 0.5)
    ax.set_xlim(-25, 3000)
    sns.despine()


    # save to file
    if not os.path.exists(exportpath + "R"):  # creates export directory

        os.makedirs(exportpath + "R")

    plt.savefig(exportpath + "R/R_FRD_FF" + str(to_overlay[Sim]) + "_" + str(to_overlay[Sim + 1]) + "_"
                + str(to_overlay[Sim + 2]) + '.png', bbox_inches='tight')

    plt.close(fig)
    gc.collect()

    return 0

    # Running through experimental conditions, i.e. Simulations #


def plot_synaptic_fraction(NeuN_Syn, exportpath):

    """ Function to plot synaptic preservation in each of the conditions of the Mota's model

         Arguments:

            NeuN_Syn (dict): Dictionary containing labels, stages, iterations, neurons per iteration and synapses per it
            exportpath(str): Path to export the dataset as a csv

       Returns:

          Plots of Synaptic Fraction

   """

    # Declaring variables #

    current_it = 0

    it_death = list()
    it_pruning = list()
    overall_it = list()
    sorted_syn = list()
    sorted_neun = list()

    # Running through experimental conditions, i.e. Simulations #

    for Sim in NeuN_Syn:

        it_pruning = np.array(NeuN_Syn[Sim]['it_p'])
        it_pruning = it_pruning + 500
        it_pruning = list(it_pruning)

        overall_it = NeuN_Syn[Sim]['it_d'] + it_pruning
        overall_syn = NeuN_Syn[Sim]['syn_d'] + NeuN_Syn[Sim]['syn_p']
        overall_neun = NeuN_Syn[Sim]['neun_d'] + NeuN_Syn[Sim]['neun_p']

        # plots data

        print(f'----------------Plotting {Sim}---------------------')

        fig = plt.figure(figsize=(5, 5), dpi=500)

        sns.set_style("ticks")
        sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=np.array(overall_it), y=np.array(overall_syn), markers=True, linewidth=2, color='r', label="Synaptic Fraction")
        #ax = sns.scatterplot(x=np.array(overall_it), y=np.array(overall_syn), markers=True, linewidth=2, color='k', label="Synaptic Fraction")
        ax = sns.lineplot(x=np.array(overall_it), y=np.array(overall_neun), markers=True, linewidth=2, color='b', label="Neurons")
        plt.legend(loc=1)

        # sets labels
        ax.set_title("Preservation of Synapses over time " + str(Sim))
        ax.set_ylabel("Count")
        ax.set_xlabel("Iteration")

        # save to file
        if not os.path.exists(exportpath + "Synaptic_Preservation"):  # creates export directory

            os.makedirs(exportpath + "Synaptic_Preservation")

        plt.savefig(exportpath + "Synaptic_Preservation/SP" + str(Sim) + '.png', bbox_inches='tight')

        plt.close(fig)
        gc.collect()

    return 0


def plot_synaptic_fraction_overlayed(color, datapath, exportpath, legend, to_overlay):
    """
    Function to plot overlayed curves of synaptic preservation of three different conditions of the Mota's Model.

    Arguments:
        datapath (str): Path to the directory containing the pickled files.
        exportpath (str): Path to export the figures.
        color (dict): Dictionary mapping Sim values to colors.
        legend (list): List of legend labels.
        to_overlay (list): List of Sim values to overlay in the plot.

    Returns:
        int: 0 if successful.
    """
    concatenated_data = load_and_concatenate_data(datapath, 'neun_syn')

    fig = plt.figure(figsize=(5, 5), dpi=500)  # generating the figure

    for Sim in to_overlay:

        if Sim not in concatenated_data:
            continue

        concatenated_Sim = concatenated_data[Sim]

        overall_it = concatenated_Sim['iterations']
        overall_syn = concatenated_Sim['syn_values']

        # plots data
        print(f"----------------Plotting {Sim}---------------------")

        sns.set_style("ticks")

        sns.set_context(context="paper", rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                             "lines.linewidth": 2, "xtick.labelsize": 8,
                                             "ytick.labelsize": 8})

        ax = sns.lineplot(x=overall_it, y=overall_syn, markers=True, linewidth=2.5, color=color[Sim],
                          label=legend[to_overlay.index(Sim)])

        ax.axvline(x=500, ymin=0, ymax=10, linestyle="dashed", color="0.8")
        ax.axvspan(0, 500, alpha=0.05)
        sns.despine()

        plt.legend(loc=1)

    # sets labels
    ax.set_title("Preservation of Synapses over time ")
    ax.set_ylabel("Synaptic count")
    ax.set_xlabel("Iteration")
    ax.set_ylim(0, 5000500)
    ax.set_xlim(0, 5500)

    # save to file
    if not os.path.exists(exportpath + "Synaptic_Preservation"):  # creates export directory
        os.makedirs(exportpath + "Synaptic_Preservation")

    plt.savefig(exportpath + "Synaptic_Preservation/SP" + "_".join(map(str, to_overlay)) + ".png", bbox_inches="tight")

    plt.close(fig)
    gc.collect()

    return 0


def network_labelling(netpath):

    """ Support function to properly label the networks in the dataframes and in the exports

             Arguments:

                 netpath(str):Path of the network

           Returns:

              Label (str)

           """

    char = -8
    counter = 1

    while netpath[char].isdigit() == True:

        char = char - 1
        counter = counter + 1

    if char == -8:

        if netpath[char] == "h":

            label = "death "+netpath[-7]

            return label, netpath[-7]

        else:

            label = "pruning "+netpath[-7]

            return label, netpath[-7]

    else:

        counter = counter * -1
        start = -6 + counter  # Playing with slicing

        if netpath[char] == "h":

            label = "death" + netpath[start:-6]

            return label, netpath[start:-6]

        else:

            label = "pruning" + netpath[start:-6]

            return label, netpath[start:-6]
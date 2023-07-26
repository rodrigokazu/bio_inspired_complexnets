# Neural Pathways Laboratory #
# University of Sheffield - University of Brazil (Federal University of Rio de Janeiro) #

# Toolbox for relevant metric-extraction from biologically inspired complex networks #

# ----------------------------------------------------------------------------------------------------------------- #

# Written by Dr Rodrigo Kazu #
# Any enquiries to r.siqueiradesouza@sheffield.ac.uk #

# ----------------------------------------------------------------------------------------------------------------- #


import gc
import igraph
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import powerlaw
import re
import seaborn as sns
import threading


# ----------------------------------------------------------------------------------------------------------------- #
# In order to utilise this toolbox you will need the path of the folder where you want to export the results #

# AND #

# The path for the folder called 50k or 100k which contains the folders Sim 1 to Sim X with your simulations #

# For Linux replace all "//" with "\"

# ----------------------------------------------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------------------------------------------- #
# Data analysis #
# ----------------------------------------------------------------------------------------------------------------- #


def analyse_allnets(allnets, exportpath):

    """ Runs the analysis for the networks modelled at 50k neurons density and export results;
        This function initiates all the threads and run the analysis in parallel for the same network;
        The .join() function guarantees that all threads will finish at the same time

         Arguments:

             allnets(list): Path for the networks to be analysed generated with the network_acquisition() function
              of this toolbox.

          Returns:

          Exported complex network statistics.

   """

    #t1 = threading.Thread(target=parallel_neun_syn_count, args=(allnets, exportpath))
    #t2 = threading.Thread(target=parallel_averagepath, args=(allnets, exportpath))
    #t3 = threading.Thread(target=parallel_density, args=(allnets, exportpath))
    #t4 = threading.Thread(target=parallel_cluster, args=(allnets, exportpath))
    #t5 = threading.Thread(target=parallel_giantcomponent, args=(allnets, exportpath))
    t6 = threading.Thread(target=parallel_fitnet, args=(allnets, exportpath))

    #t1.start()
    #t2.start()
    #t3.start()
    #t4.start()
    #t5.start()
    t6.start()

    #t1.join()
    #t2.join()
    #t3.join()
    #t4.join()
    #t5.join()
    t6.join()


def fit_net(label, nets, Sim, exportpath, save_graphs=False):

    """
    Need to speak to Dr Kleber Neves

            Arguments:

                allnets(list): Path for the networks to be analysed generated with the network_acquisition() function
                 of this toolbox.

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

    return stage, int(it), fit.power_law.alpha, fit.power_law.D,


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

             Arguments:

                 main_path(str): Paths to the directory where the networks are stored

           Returns:

              Networks paths for 50k and 100k density simulations
             """

    fifty = main_path + "/50k/"
    hundred = main_path + "/100k/"

    fiftysims = os.listdir(fifty)
    hundredsims = os.listdir(hundred)

    fiftysims_paths = list()
    hundredsims_paths = list()  # To export a list with the Sim folders "Sim 1", "Sim 2", etc.

    for sim in fiftysims:

        if sim != "Degree_Dist":

            path = fifty + sim
            fiftysims_paths.append(path)

    for sim in hundredsims:

        path = hundred + sim
        hundredsims_paths.append(path)

    return fiftysims_paths, hundredsims_paths


def parallel_averagepath(allnets, exportpath):

    """ Computes the average path length for a list of networks generated with network_acquisition()

      Arguments:

          allnets(list): List of networks generated with network_acquisition()
          exportpath(str): Path to export the dataset as a csv

           Returns:

            Average path exported as csv

        """

    averagepaths = dict()

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        averagepaths[Sim] = dict()
        averagepaths[Sim+" iterations"] = dict()

        print(f'Computing path lenght for {Sim}')
        print(f"[Calculating average path length on thread number ] {threading.current_thread()}")

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)

                path = net.average_path_length()

                label = network_labelling(nets)
                name = "AveragePath.csv"

                averagepaths[Sim][label[0]] = path
                averagepaths[Sim + " iterations"][label[0]] = label[1]

                del net
                gc.collect()

        write_metrics(metric=averagepaths, exportpath=exportpath, name=name, label=label)
        print(f'Done for {Sim}')

    return averagepaths


def parallel_centrality(allnets, exportpath):

    return 0


def parallel_cluster(allnets, exportpath):

    """ Computes the clustering coefficient for a list of networks generated with network_acquisition()

                 Arguments:

                     allnets(list): List of networks generated with network_acquisition()
                     exportpath(str): Path to export the dataset as a csv

               Returns:

                Clustering coefficients exported as csv

   """

    averagecluster = dict()

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        averagecluster[Sim] = dict()

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)

                print(f'Computing clustering for {nets}')
                print(f"[Calculating transitivity on thread number ] {threading.current_thread()}")
                clustering = net.transitivity_undirected()  # Target is what's running on the new thread
                print(f'The clustering coefficient is {clustering}')

                label = network_labelling(netpath=nets)
                name = "AverageClustering.csv"

                averagecluster[Sim][label[0]] = clustering

                del net
                gc.collect()

        print(f'Writing to *.csv')
        write_metrics(metric=averagecluster, exportpath=exportpath, name=name, label=label)

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


def parallel_fitnet(allnets, exportpath):

    """ Fits the power law for a list of networks generated with network_acquisition()

      Arguments:

          allnets(list): List of networks generated with network_acquisition()
          exportpath(str): Path to export the dataset as a csv

           Returns:

            Fits

        """

    fits = dict()
    netnumbers = list()

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        fits[Sim] = dict()
        alpha_D_list = list()

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)
                label = network_labelling(nets)

                print(f'Computing fits for {nets}')
                print(f"[Calculating fits on thread number ] {threading.current_thread()}")

                alpha_D = fit_net(label=label, nets=nets, exportpath=exportpath, Sim=Sim, save_graphs=False)

                name = "Fits.csv"

                fits[Sim][label[0]] = alpha_D
                alpha_D_list.append(alpha_D)

                del net
                gc.collect()

        plot_alpha_D(alpha_D=alpha_D_list, Sim=Sim, exportpath=exportpath)

        print(f'Writing to *.csv')
        write_metrics(metric=fits, exportpath=exportpath, name=name, label=label)

    return 0


def parallel_giantcomponent(allnets, exportpath):

    """ Computes the giant compnent for a list of networks generated with network_acquisition()

                 Arguments:

                     allnets(list): List of networks generated with network_acquisition()

               Returns:

                  CSV of giant components for all networks and simulations

   """
    gcs = dict()

    for Sim in allnets:  # Fifty nets is a dict with Sims as keys

        gcs[Sim] = dict()

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

                del net
                gc.collect()

        print(f'Writing to *.csv')
        write_metrics(metric=gcs, exportpath=exportpath, name=name, label=label)

    return gcs


def parallel_neun_syn_count(allnets, exportpath):

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
        stage = list()

        for nets in allnets[Sim]:

            if os.path.getsize(nets) > 0:

                net = igraph.Graph.Read(nets)

                print(f'Evaluating neurons and synapses for {nets}')
                print(f"[Calculating NeuN_Syn on thread number ] {threading.current_thread()}")

                label = network_labelling(netpath=nets)
                name = "NeuN_Syn_Meta.csv"

                # store number of neurons, synapses
                neurons_per_it[Sim].append(len(net.vs.select(_degree_gt=0)))
                neurons_over_1_per_it[Sim].append((len(net.vs.select(_degree_gt=1))))
                synapses_per_it[Sim].append((len(net.es)))
                stage.append(re.search(r'(pruning|death)', label[0])[1])
                it.append(label[1])
                labels[Sim].append(label[0])

                print(f'Network has {len(net.vs.select(_degree_gt=1))} active neurons.')

                del net
                gc.collect()

        NeuN_Syn[Sim] = {"Labels": labels, "Stage": stage, "Iteration": it, "NeuN": neurons_per_it[Sim], "Syn": synapses_per_it[Sim],
                         "Active_NeuN": neurons_over_1_per_it[Sim]}

    print(f'Writing to *.csv')
    write_metrics(metric=NeuN_Syn, exportpath=exportpath, name=name, label=label)

    return 0


def write_metrics(metric, exportpath, name, label):

    """ Writes the results of the analysis for the networks modelled at 50k neurons density and export results;


         Arguments:

             averagepath(list): Dataset containing the average path length for the networks analysed

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


def plot_alpha_D(alpha_D, exportpath, Sim):

    """ Original function written by Dr Kleber Neves to plot the degree distributions, customised for Alpha and D
    Alpha and D can be obtained using fit_net()

         Arguments:

            dd (list): Degree Distribution of an iigraph.Graph object

       Returns:

          Plots of degree distributions

   """

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

    for label in alpha_D:

        if label[0] == "death":

            it_death.append(label[1])
            alpha_death.append(label[2])
            D_death.append(label[3])

            overall_it.append(current_it)
            overall_alpha.append(label[2])
            overall_D.append(label[3])

        else:

            it_pruning.append(label[1])
            alpha_pruning.append(label[2])
            D_pruning.append(label[3])

            overall_it.append(current_it)
            overall_alpha.append(label[2])
            overall_D.append(label[3])

        current_it = current_it + 1

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

    # Dealing with "L" and "U" outputs

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

    for index in range(0, len(sorted_D)):

        if sorted_D[index] == "L":

            delete_from_sorted.append(index)

        if sorted_D[index] == "U":

            delete_from_sorted.append(index)

        # Dealing with "L" and "U" outputs

    for index in sorted(delete_from_sorted, reverse=True):

        del sorted_D[index]
        del it_pruning[index] # Plotted lists should be of the same size

    if len(it_death) > 0:

        # concatenating death and pruning iterations
        it_pruning = np.array(it_pruning)
        it_pruning = it_pruning + 500
        it_pruning = list(it_pruning)

    overall_it = it_death + it_pruning
    overall_it = sorted(overall_it)

    fig = plt.figure(figsize=(5, 5), dpi=500)

    sns.set_style("ticks")

    sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                         "lines.linewidth": 2, "xtick.labelsize": 8,
                                         "ytick.labelsize": 8})

    # plots data
    ax = sns.lineplot(x=overall_it, y=sorted_alpha, markers=True, linewidth=2, color='r', label="Alpha")
    ax = sns.lineplot(x=overall_it, y=sorted_D, markers=True, linewidth=2, color='b', label="Distance")
    ax.set(ylim=[0, 2])
    plt.legend()

    gc.collect()

    # sets labels
    ax.set_title("Evolution of Alpha and D")
    ax.set_title(str(Sim))
    ax.set_ylabel("Measure")
    ax.set_xlabel("Iteration")

    # save to file
    if not os.path.exists(exportpath + "Alpha_D"):  # creates export directory

        os.makedirs(exportpath + "Alpha_D")

    plt.savefig(exportpath + "Alpha_D/" + str(Sim) + '.png', bbox_inches='tight')
    plt.close(fig)

    return 0


def plot_degree_distribution_line(allnets, exportpath):

    """ Original function written by Dr Kleber Neves to plot the degree distributions

         Arguments:

            dd (list): Degree Distribution of an iigraph.Graph object

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

            dd (list): Degree Distribution of an iigraph.Graph object

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


def plot_average_path(exportpath, pathdata):

    """ Plots the path lenghts for a given network

             Arguments:

                pathdata (str): Path for a *.csv spreadsheet

           Returns:

              Plots of path lengths

       """

    path = pd.read_csv(pathdata)

    Sim1 = path['Sim 1']
    Iteration = path['Iteration']

    fig = plt.figure(figsize=(5, 5), dpi=500)

    sns.set_style("ticks")

    sns.set_context(context='paper', rc={"font.size": 10, "axes.titlesize": 12, "axes.labelsize": 9,
                                         "lines.linewidth": 2, "xtick.labelsize": 8,
                                         "ytick.labelsize": 8})

    # plots data
    ax = sns.scatterplot(x=Iteration, y=Sim1)

    #ax.set(yscale="log", xscale="log", ylim=[10 ** -0.2, 10 ** 4], xlim=[10 ** -0.2, 10 ** 4])

    # sets labels
    ax.set_title("Sim 1")
    ax.set_ylabel("Path length")
    ax.set_xlabel("Iteration")

    # save to file

    plt.savefig(exportpath + 'Sim1.png', bbox_inches='tight')
    plt.close(fig)

    return 0

# ----------------------------------------------------------------------------------------------------------------- #
# Support functions #
# ----------------------------------------------------------------------------------------------------------------- #


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

            label = "death"+netpath[-7]

            return label, netpath[-7]

        else:

            label = "pruning"+netpath[-7]

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


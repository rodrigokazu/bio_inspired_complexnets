# bio_inspired_complexnets
”Sculpting is easy.  You just chip away everything that does not look like David.” Michelangelo  (attributed),  about  the  making  of  his  masterpiece David

Reference for what was simulated in each Sim is in the file simulation_reference.xls

Code repository for the paper: "Selective pruning and neuronal death generate heavy-tail network connectivity" by Kazu et al. If you have any questions please contact:  r.siqueiradesouza@sheffield.ac.uk

# Usage: 

To use this toolbox, you will need the path of the folder where you want to export the results and the path for the folder called 50k or 100k (neuronal densities of your network) which contains the folders Sim 1 to Sim X with your simulations, each of which will have an "Edges" folder inside containing *.edges files.

# Documentation version 1.0:


Neural Pathways Laboratory
University of Sheffield - University of Brazil (Federal University of Rio de Janeiro)
Toolbox for relevant metric-extraction from biologically inspired complex networks

# Modules and Functions

****1. analyse_all(allnets, exportpath, **datapath)****

def analyse_all(allnets, exportpath, **datapath):
    """ 
    Runs the analysis for the networks modeled at 50k neurons density and exports results.
    This function initiates all the threads and runs the analysis in parallel for the same network.
    The .join() function guarantees that all threads will finish at the same time.

    Arguments:
        allnets (list): Path for the networks to be analysed generated with the network_acquisition() function.
        exportpath (str): Path where the results will be exported.

    Returns:
        None
    """
**2. fit_net(label, nets, Sim, exportpath, save_graphs=False)**

def fit_net(label, nets, Sim, exportpath, save_graphs=False):
    """
    Function that runs the Kolmogorov-Smirnov test.

    Arguments:
        label (str): Output of the network_labelling() function.
        nets (str): Path of the network to be analysed.
        Sim (str): Simulation number.
        exportpath (str): Path where the plots and analysed data will be exported.
        save_graphs (bool): Whether to save the generated graphs.

    Returns:
        tuple: Contains stage, iteration, alpha, and D values.
    """
**3. network_acquisition(density_path)**

def network_acquisition(density_path):
    """ 
    Acquires the paths to the biologically-inspired networks for further analysis.

    Arguments:
        density_path (str): Paths to the directory where the networks of correct density are stored.

    Returns:
        dict: Networks path and list containing all the network files.
    """
**4. network_density_paths(main_path)**

def network_density_paths(main_path):
    """ 
    Acquires the paths to the biologically-inspired networks of 100k and 50k densities for further analysis.

    Arguments:
        main_path (str): Paths to the directory where the networks are stored.

    Returns:
        tuple: Networks paths for 50k and 100k density simulations.
    """
**5. parallel_averagepaths(allnets, exportpath)**

def parallel_averagepaths(allnets, exportpath):
    """ 
    Computes the average path length for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Average paths.
    """
**6. parallel_clusters(allnets, exportpath)**

def parallel_clusters(allnets, exportpath):
    """ 
    Computes the clustering coefficient for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Clustering coefficients.
    """
**7. parallel_density(allnets, exportpath)**

def parallel_density(allnets, exportpath):
    """ 
    Computes the density for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        float: Density of the networks.
    """
**8. parallel_fitnet(allnets, exportpath)**

def parallel_fitnet(allnets, exportpath):
    """ 
    Fits the power law for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Fits of the networks.
    """
**9. parallel_giantcomponent(allnets, exportpath)**

def parallel_giantcomponent(allnets, exportpath):
    """ 
    Computes the giant component for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Giant components of the networks.
    """
**10. parallel_neun_syn_counts(allnets, exportpath)**

def parallel_neun_syn_counts(allnets, exportpath):
    """ 
    Computes the number of neurons and synapses per simulation.

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Neuron and synapse counts.
    """

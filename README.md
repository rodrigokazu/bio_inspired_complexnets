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

Modules and Functions
1. analyse_all(allnets, exportpath, **datapath)
python
Copy code
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
2. fit_net(label, nets, Sim, exportpath, save_graphs=False)
python
Copy code
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
3. network_acquisition(density_path)
python
Copy code
def network_acquisition(density_path):
    """ 
    Acquires the paths to the biologically-inspired networks for further analysis.

    Arguments:
        density_path (str): Paths to the directory where the networks of correct density are stored.

    Returns:
        dict: Networks path and list containing all the network files.
    """
4. network_density_paths(main_path)
python
Copy code
def network_density_paths(main_path):
    """ 
    Acquires the paths to the biologically-inspired networks of 100k and 50k densities for further analysis.

    Arguments:
        main_path (str): Paths to the directory where the networks are stored.

    Returns:
        tuple: Networks paths for 50k and 100k density simulations.
    """
5. parallel_averagepaths(allnets, exportpath)
python
Copy code
def parallel_averagepaths(allnets, exportpath):
    """ 
    Computes the average path length for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Average paths.
    """
6. parallel_clusters(allnets, exportpath)
python
Copy code
def parallel_clusters(allnets, exportpath):
    """ 
    Computes the clustering coefficient for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Clustering coefficients.
    """
7. parallel_density(allnets, exportpath)
python
Copy code
def parallel_density(allnets, exportpath):
    """ 
    Computes the density for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        float: Density of the networks.
    """
8. parallel_fitnet(allnets, exportpath)
python
Copy code
def parallel_fitnet(allnets, exportpath):
    """ 
    Fits the power law for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Fits of the networks.
    """
9. parallel_giantcomponent(allnets, exportpath)
python
Copy code
def parallel_giantcomponent(allnets, exportpath):
    """ 
    Computes the giant component for a list of networks generated with network_acquisition().

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Giant components of the networks.
    """
10. parallel_neun_syn_counts(allnets, exportpath)
python
Copy code
def parallel_neun_syn_counts(allnets, exportpath):
    """ 
    Computes the number of neurons and synapses per simulation.

    Arguments:
        allnets (list): List of networks generated with network_acquisition().
        exportpath (str): Path to export the dataset as a CSV.

    Returns:
        dict: Neuron and synapse counts.
    """
11. calc_average_path(G, verbose=False)
python
Copy code
def calc_average_path(G, verbose=False):
    """
    Computes the average path length of the graph.

    Arguments:
        G (networkx.Graph): The graph to compute the average path length for.
        verbose (bool): Whether to print detailed output.

    Returns:
        float: The average path length of the graph.
    """
12. calc_clustering_coefficient(G, verbose=False)
python
Copy code
def calc_clustering_coefficient(G, verbose=False):
    """
    Computes the clustering coefficient of the graph.

    Arguments:
        G (networkx.Graph): The graph to compute the clustering coefficient for.
        verbose (bool): Whether to print detailed output.

    Returns:
        float: The clustering coefficient of the graph.
    """
13. calc_density(G, verbose=False)
python
Copy code
def calc_density(G, verbose=False):
    """
    Computes the density of the graph.

    Arguments:
        G (networkx.Graph): The graph to compute the density for.
        verbose (bool): Whether to print detailed output.

    Returns:
        float: The density of the graph.
    """
14. calc_giant_component(G, verbose=False)
python
Copy code
def calc_giant_component(G, verbose=False):
    """
    Computes the size of the giant component of the graph.

    Arguments:
        G (networkx.Graph): The graph to compute the giant component for.
        verbose (bool): Whether to print detailed output.

    Returns:
        int: The size of the giant component.
    """
15. count_neurons_synapses(G, verbose=False)
python
Copy code
def count_neurons_synapses(G, verbose=False):
    """
    Computes the number of neurons and synapses in the graph.

    Arguments:
        G (networkx.Graph): The graph to count neurons and synapses for.
        verbose (bool): Whether to print detailed output.

    Returns:
        tuple: Number of neurons and synapses.
    """
16. fit_powerlaw(G, verbose=False)
python
Copy code
def fit_powerlaw(G, verbose=False):
    """
    Fits a power-law distribution to the degree distribution of the graph.

    Arguments:
        G (networkx.Graph): The graph to fit the power-law distribution to.
        verbose (bool): Whether to print detailed output.

    Returns:
        tuple: Alpha and D values from the Kolmogorov-Smirnov test.
    """
17. load_graph(filename, verbose=False)
python
Copy code
def load_graph(filename, verbose=False):
    """
    Loads a graph from a file.

    Arguments:
        filename (str): Path to the file containing the graph data.
        verbose (bool): Whether to print detailed output.

    Returns:
        networkx.Graph: The loaded graph.
    """
18. save_graph(G, filename, verbose=False)
python
Copy code
def save_graph(G, filename, verbose=False):
    """
    Saves a graph to a file.

    Arguments:
        G (networkx.Graph): The graph to save.
        filename (str): Path to the file to save the graph to.
        verbose (bool): Whether to print detailed output.

    Returns:
        None
    """
19. plot_degree_distribution(G, filename, verbose=False)
python
Copy code
def plot_degree_distribution(G, filename, verbose=False):
    """
    Plots the degree distribution of the graph.

    Arguments:
        G (networkx.Graph): The graph to plot the degree distribution for.
        filename (str): Path to the file to save the plot to.
        verbose (bool): Whether to print detailed output.

    Returns:
        None
    """

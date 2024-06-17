#  Neural Pathways & metaBIO Labs
(http://neuralpathways.uk & https://metabio.netlify.app/)

# Wellcome Sanger Institute & Cambridge Neuroscience in collaboration with the Federal University of Rio de Janeiro

”Sculpting is easy.  You just chip away everything that does not look like David.” Michelangelo  (attributed),  about  the  making  of  his  masterpiece David

Reference for what was simulated in each Sim is in the file simulation_reference.xls

Code repository for the paper: "Selective pruning and neuronal death generate heavy-tail network connectivity" by Kazu et al. If you have any questions please contact:  r.siqueiradesouza@sheffield.ac.uk

# Documentation version 1.1:

# The model

You can use the *.sh files from the CMD folder to run the model. Place it inside the folder that has the model you want to run (ie. motaXT0.65.py).

The computational model described in your script has several parameters that are set up using the `argparse` library for command-line arguments.

The parameters in the model are listed in each bash file and are customisable as follows: 


1. **Neurons per Module** (`neurons_per_module`): This is the number of neurons in each module of the network.
   - Argument: `-nn`
   - Type: `int`
   - Default: `10000`

2. **Synapses per Neuron** (`synapses_per_neuron`): This is the number of synapses each neuron has.
   - Argument: `-syn`
   - Type: `int`
   - Default: `100`

3. **Number of Modules** (`number_of_modules`): This is the number of modules in the network.
   - Argument: `-mn`
   - Type: `int`
   - Default: `1`

4. **Meta Network** (`meta_network`): This parameter determines the type of meta network used.
   - Argument: `-meta`
   - Choices: `['random', 'offdiagonal', 'full', 'smallworld', 'lattice', 'file']`
   - Default: `full`

5. **Meta Network Argument** (`metaargs`): This is an additional argument for the meta network, such as the percentage of rewiring for a small-world network.
   - Argument: `-metaargs`
   - Type: `float`
   - Default: `0`

6. **Death Iterations** (`death_iterations`): This is the number of iterations for neuron death.
   - Argument: `-dits`
   - Type: `int`
   - Default: `1`

7. **Pruning Iterations** (`pruning_iterations`): This is the number of iterations for synapse pruning.
   - Argument: `-pits`
   - Type: `int`
   - Default: `0`

8. **Death Method** (`death_method`): This is the method used for neuron death.
   - Argument: `-dmet`
   - Choices: `['in-degree', 'out-degree', 'degree', 'random']`
   - Default: `in-degree`

9. **Pruning Method** (`pruning_method`): This is the method used for synapse pruning.
   - Argument: `-pmet`
   - Choices: `['hebbian-approx', 'inv-hebbian-approx', 'random']`
   - Default: `hebbian-approx`

10. **C_R** (`c_R`): This is a parameter for the computational model, often related to synaptic strength or connectivity.
    - Argument: `-r`
    - Type: `float`
    - Default: `1.0 / 3.0`

11. **C_A** (`c_A`): This is another parameter for the computational model, possibly related to activity or adaptation.
    - Argument: `-a`
    - Type: `float`
    - Default: `0.01`

12. **C_K** (`c_K`): This is another parameter, possibly related to a constant in the model.
    - Argument: `-k`
    - Type: `float`
    - Default: `0.2`

13. **Feed Forward** (`feed_forward`): This parameter may influence the feedforward connections in the network.
    - Argument: `-ff`
    - Type: `float`
    - Default: `1`

14. **Synaptic Reach** (`synaptic_reach`): This is the reach or range of synapses.
    - Argument: `-sr`
    - Type: `int`
    - Default: `10000`

These parameters define the configuration of the network and the rules for neuron death and synapse pruning within the computational model.

# Usage of the analysis toolbox: 

To use this the analysis toolbox (Mota_CNtoolbox.py), you will need the path of the folder where you want to export the results and the path for the folder called 50k or 100k (neuronal densities of your network) which contains the folders Sim 1 to Sim X with your simulations, each of which will have an "Edges" folder inside containing *.edges files.

# Toolbox for relevant metric-extraction from biologically inspired complex networks

# Modules and Functions

****1. analyse_all(allnets, exportpath, **datapath)****

def analyse_all(allnets, exportpath, **datapath):
    """ 
    Runs the analysis for the networks modelled at 50k neuron density and exports results.
    This function initiates all the threads and runs the analysis in parallel for the same network.
    The .join() function guarantees that all threads will finish at the same time.

    Arguments:
        allnets (list): Path for the networks to be analysed generated with the network_acquisition() function.
        exportpath (str): Path where the results will be exported.

    Returns:
        None
    """
****1.1 plot_ALL_analysis(allnets, color, exportpath, legend, to_overlay, **datapath)****

def plot_ALL_analysis(allnets, color, exportpath, legend, to_overlay, **datapath):

    """ Plots the analysis for the networks modelled at 50k neurons density and export results;
        This function initiates all the threads and run the analysis in parallel for the same network;
        The .join() function guarantees that all threads will finish at the same time

         Arguments:

            allnets(list): Path for the networks  generated with the network_acquisition() function of this toolbox for
            the overlayed scats functiom.
             datapath(str): Path for a folder where all the analyses generated with this toolbox are saved as *.pkl
             to_overlay(list): List of simulations to be plotted in the "Sim X" convention
             legend (list): List of words to compose the legend of the figures
             color (dict): Dict of colours for the plot with the "Sim X" convention as keys

          Returns:

          Overlayed plots.

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

# The data exported from the analysis should be in the following format: 

Clustering Data (clustering.pkl):

Type: List of dictionaries
Keys: ['Simulation', 'Network', 'Label', 'Iteration', 'Clustering', 'Type']

Average Path Length Data (averagepaths.pkl):

Type: List of dictionaries
Keys: ['Simulation', 'Network', 'Label', 'Iteration', 'AveragePathLength', 'Type']

Note: The correct key for path length is 'AveragePathLength', not 'PathLength'
NeuN and Synapse Data (NeuN_Syn.pkl):

Type: Dictionary
Keys within each simulation: ['Labels', 'Stage', 'Iteration', 'NeuN', 'Syn', 'Active_NeuN', 'it_d', 'it_p', 'neun_d', 'neun_p', 'syn_d', 'syn_p']

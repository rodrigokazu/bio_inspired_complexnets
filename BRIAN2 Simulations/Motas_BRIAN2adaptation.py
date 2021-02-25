from brian2 import *
import igraph as ig
import seaborn as sns
import time

# Function definitions #


set_device('cpp_standalone')


@implementation('cpp','''
// Note that functions always need a return value at the moment
double store_spike(int i, double t) {
    static std::ofstream spike_file("C:/Users/pc1rss/Desktop/spikes.txt");
    spike_file << i << " " << t << std::endl;
    return 0.;  // unused
}
''')


@check_units(i=1, t=second, result=1)
def store_spike(i, t):

    raise NotImplementedError('Use standalone mode')


def motas_raster_and_hist(t):

    # Visualising the Spikes over 100 ms #

    fig = plt.figure(figsize=(175, 20), dpi=100)

    sns.set(style='whitegrid', font_scale=2)

    sns.set_context(context='notebook', rc={"font.size": 10, "axes.titlesize": 20, "axes.labelsize": 15,
                                            "lines.linewidth": 1, "xtick.labelsize": 12, "ytick.labelsize": 12,
                                            "lines.markersize": 2})
    subplot(211)

    plot(spikemon.t / ms, spikemon.i, '.k')
    xlabel('Time (ms)')
    ylabel('Neuron index')

    # Histogram of instantaneous FRs #

    subplot(212)

    _ = hist(spikemon.t / ms, 100, histtype='stepfilled', facecolor='k',
             weights=list(ones(len(spikemon)) / (Neuronumber * defaultclock.dt)))

    xlabel('Time (ms)')
    ylabel('Instantaneous firing rate (sp/s)')

    plt.savefig(desktop + "Motas_scatter_plus_instantFR.png")


def visualise_connectivity(filename, path, S):

    sns.set(context='notebook', style='whitegrid', font_scale=4)

    sns.set_context("talk", rc={"font.size": 60, "axes.titlesize": 60, "axes.labelsize": 70, "lines.linewidth": 4,
                                "xtick.labelsize": 50, "ytick.labelsize": 50, "lines.markersize": 30})

    Ns = len(S.source)
    Nt = len(S.target)

    fig = figure(figsize=(80, 32))

    subplot(121)

    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10, color='grey')

    for i, j in zip(S.i, S.j):

        plot([0, 1], [i, j], '-k')

    xticks([0, 1], ['Source', 'Target'])

    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))

    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')

    plt.savefig(path + filename + "Graph.png")

    return fig


# CHANGE PATHS ACCORDINGLY #

# Reading Mota's Network that will be analysed #

mota_path = "C:\\Users\\pc1rss\\Dropbox\\NeuralCGI\\Brian2\\Comples Networks test\\Sample Networks" \
            "\\mota_net_pruning400.edges"

desktop = "C:\\Users\\pc1rss\\Desktop\\"

mota = ig.Graph.Read_Edgelist(mota_path, directed=True)  # Creating a graph

syn = 0

for e in mota.es:

    syn = syn + 1

print("Mota's Model Network description:\n Number of nodes: ", len(mota.vs.indices), "\nNumber of edges: ", syn)

# Starting BRIAN2 #

start_scope()

N = len(mota.vs.indices)

# Parameters of the simulation of multiple neuronal types #

tau = 10*ms
v0_max = 3.
duration = 2000*ms
sigma = 0.2

area = 20000*umetre**2
Cm = 1*ufarad*cm**-2 * area
gl = 5e-5*siemens*cm**-2 * area
El = -65*mV
EK = -90*mV
ENa = 50*mV
g_na = 100*msiemens*cm**-2 * area
g_kd = 30*msiemens*cm**-2 * area
VT = -63*mV

# Differential equation of the simulated neuron #

eqs = Equations('''
dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I)/Cm : volt
dm/dt = 0.32*(mV**-1)*4*mV/exprel((13.*mV-v+VT)/(4*mV))/ms*(1-m)-0.28*(mV**-1)*5*mV/exprel((v-VT-40.*mV)/(5*mV))/ms*m : 1
dn/dt = 0.032*(mV**-1)*5*mV/exprel((15.*mV-v+VT)/(5*mV))/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
I : amp
''')


# Creates as many leaky integrator neurons as the original network had and the Synapses object for those neurons #

G = NeuronGroup(N, eqs, threshold='v > -40*mV', refractory='v > -40*mV', method='exponential_euler')

G.v = El
G.I = '0.7*nA * i / N'  # Initial voltage

M = SpikeMonitor(G)  # Recording events

S = Synapses(G, G)

# Connecting accordingly to the edges in the Mota's Network #

start = time.asctime(time.localtime(time.time()))

print("Connecting synapses to Mota's...")

for e in mota.es:

    S.connect(i=e.tuple[0], j=e.tuple[1])

print("Started to connect synapses to Mota's at: ", start)
print("Finished the full adjacency matrix at: ", time.asctime(time.localtime(time.time())))

# visualise_connectivity(filename="Mota_Graph_10k", path=desktop, S=S)  # Generating figures

print("Simulating the spiking activity now...")
run(duration)  # Let the games begin!

print("Finished the spiking simulation at: ", time.asctime(time.localtime(time.time())))

motas_raster_and_hist(spikemon=M, Neuronumber=N)

print("Mota's simulation in done saving the data.")


"""
This @network_operation does not work. 

@network_operation(clock=Clock(dt=10*ms))
def draw_gfx():  # This returns two lists i, t of the neuron indices and spike times for # all the recorded spikes

    rasterline, = plot([], [], '.')  # plot points, hence the '.'
    axis([0, 1, 0, N])
    subplot(212)
    traceline, = plot([], [])  # plot lines, hence no '.'
    axis([0, 1, -0.06, -0.05])

    i, t = zip(M.spikes)
    rasterline.set_xdata(M.t / ms)
    rasterline.set_ydata(M.i)

    traceline.set_xdata(trace.t)

    traceline.set_ydata(trace[0]) # and finally tell pylab to redraw it
    plt.savefig("C:\\Users\\pc1rss\\Desktop\\Graph.png")
    draw()
"""
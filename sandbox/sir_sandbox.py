import matplotlib.pyplot as plt
import numpy as np
from scipy import io
import math

import networkx as nx
from networkx import algorithms as alg

import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mconf

# Network selection in which to simulate the infection/spreading process
G = nx.read_gml("data/dolphins.gml", label="id")
# G = nx.erdos_renyi_graph(1000, 0.1)
# G = nx.watts_strogatz_graph(1000, 5, 0.1)
# G = nx.barabasi_albert_graph(n=100, m=2)

# SIR infection model parameters.
#     infected nodes will infect other nodes with probability beta, and recover
#     (become non-susceptible to reinfection) after one timestep
BETA = 0.08  # P(infectious node infecting a susceptible neighbour)
GAMMA = 1.0  # P(infectious node becoming recovered after one timestep)
NUM_ITERATIONS = 200  # Number of iterations for which to perform simulation
NUM_REPETITION_EACH_NODE = 100  # Number of realisations for each starting node

OUTPUT = "output/"
DEBUGGING = "debugging/"


def configure_sir_model(
        starting_node, network=G, beta=BETA, gamma=GAMMA):
    """Configures the SIR infection model"""
    model = ep.SIRModel(network)
    config = mconf.Configuration()

    config.add_model_parameter('beta', beta)  # P(infecting)
    config.add_model_parameter('gamma', gamma)  # P(recovery) after 1 timestep
    config.add_model_initial_configuration(
        'Infected', [starting_node])
    model.set_initial_status(config)
    return model


# Vector to store the Mis
M = [0]*len(G.nodes)

# Loop to start successively at each node in the network
# Set the initial configuration, and the starting node
for i, starting_node in enumerate(list(G.nodes)):

    # Loop for the number of realisations to consider for each starting case
    m = []  # store total number of infected nodes after each realisation
    for _ in range(NUM_REPETITION_EACH_NODE):
        # Need to reinitialise model parameters at each realisation
        model = configure_sir_model(starting_node)
        # Iterate the spreading process for NUM_ITERATIONS
        iterations = model.iteration_bunch(NUM_ITERATIONS)
        trends = model.build_trends(iterations)

        # Size of the population infected, for this realisation
        # In SIR infection model: number of "removed" nodes in last iteration
        m.append(trends[0]["trends"]["node_count"][2][-1])

    # Average size of population M[i] infected, w/ epidemic starting at node i
    M[i] = np.mean(m)


# Analysis of the actual spreading /-------------------------------------------

# 1) Characterise the (k_s, k) (coreness, degree) of the starting node
"""Attribute to each node in the network its k_s (coreness) value"""
corenesses = []
shell_layer = 0
current_shell = nx.core.k_shell(G, k=shell_layer)
while (len(current_shell.nodes) != 0 or shell_layer == 0):
    for node in list(current_shell.nodes):
        G.nodes[node]["layer"] = shell_layer
        corenesses.append(shell_layer)
    shell_layer += 1
    current_shell = nx.core.k_shell(G, k=shell_layer)
final_layer = shell_layer - 1

"""Attribute to each node in the network its k (degree) value"""
degrees = [tup[1] for tup in list(G.degree())]
for i, node in enumerate(G.nodes):
    G.nodes[node]["degree"] = degrees[i]

"""Attribute to each node in the network its C_B (betweenness centrality)"""
centralities = alg.betweenness_centrality(G)
for node in G.nodes:
    G.nodes[node]["centrality"] = centralities[node]

# +-------------------------------------------------------------------------+
# FROM HERE ON IS JUST ANALYSIS; SO LET'S SAVE TO .mat FILE
# +-------------------------------------------------------------------------+
mdic = {"degrees": degrees,
        "centralities": centralities,
        "corenesses": corenesses,
        "M": M,
        "G": G}
io.savemat(DEBUGGING + "sir_simulation_results.mat", mdic)


# Compute M(k_s, k): the average size of the population Mi infected in
# an epidemic originating at node i with a given (k_s, k), averaged over all
# origins with the same (k_s, k) values

unique_degrees = np.unique(degrees)
unique_centralities = np.unique([v for _, v in centralities.items()])
unique_coreness = np.unique(corenesses)

# +-------------------------------------------------------------------------+
# |   k-shell index vs degree k outcome of spreading prediction             |
# +-------------------------------------------------------------------------+

# create object where to store the data for each of the plots, with the right
# dimensions. Each entry will correspond to a unique (k_s, k), and thus
# store the corresonding M(k_s, k)
ks_vs_degree = np.zeros((len(unique_coreness), len(unique_degrees)))
square_aspect_ratio_ks_k = len(unique_coreness) / len(unique_degrees)

# row index: coreness ks
# column index: degree k
for row_index, ks in zip(
        range(0, len(ks_vs_degree)), unique_coreness):
    for column_index, k in zip(
            range(0, len(ks_vs_degree[row_index])), unique_degrees):
        count = 0
        sum = 0
        for i, node in enumerate(G.nodes):
            if G.nodes[node]["layer"] == ks and G.nodes[node]["degree"] == k:
                count += 1
                sum += M[i]
        if count != 0:
            ks_vs_degree[row_index][column_index] = sum / count

# Convert data from absolute M(k_s, k) to percentual M(k_s, k)
for i in range(0, len(ks_vs_degree)):
    for j in range(0, len(ks_vs_degree[i])):
        ks_vs_degree[i][j] = ks_vs_degree[i][j] / len(G.nodes) * 100

# Visualize in the colormap grid format:
fig, ax = plt.subplots(1, 1)
im0 = ax.imshow(np.transpose(ks_vs_degree), cmap='jet',
                aspect=square_aspect_ratio_ks_k,
                extent=(0, np.max(unique_coreness),
                        0, np.max(unique_degrees)),
                origin="lower")
xlim = (np.min(unique_coreness), np.max(unique_coreness))
ylim = (np.min(unique_degrees), np.max(unique_degrees))
ax.set_xlabel(xlim)
ax.set_ylabel(ylim)
ax.set_xticks(unique_coreness)
ax.set_yticks(unique_degrees)
ax.set_xticklabels(unique_coreness)
ax.set_yticklabels(unique_degrees)
ax.set_xlabel("Coreness $k_S$")
ax.set_ylabel("Degree $k$")
plt.colorbar(im0, ax=ax, label='$M$(%)')
plt.savefig(
    OUTPUT + 'ks_vs_k_spreading_prediction.png')


# +-------------------------------------------------------------------------+
# |k-shell index vs betweenness centrality C_B spreading outcome prediction |
# +-------------------------------------------------------------------------+

# create object where to store the data for each of the plots, with the right
# dimensions. Each entry will correspond to a unique (k_s, k), and thus
# store the corresonding M(k_s, k)
ks_vs_cb = np.zeros((len(unique_coreness), len(unique_centralities)))
square_aspect_ratio_ks_cb = len(unique_coreness) / np.max(unique_centralities)

# row index: coreness ks
# column index: betweennes centrality cb
for row_index, ks in zip(
        range(0, len(ks_vs_cb)), unique_coreness):
    for column_index, cb in zip(
            range(0, len(ks_vs_cb[row_index])), unique_centralities):
        count = 0
        sum = 0
        for i, node in enumerate(G.nodes):
            if G.nodes[node]["layer"] == ks and G.nodes[
                    node]["centrality"] == cb:
                count += 1
                sum += M[i]
        if count != 0:
            ks_vs_cb[row_index][column_index] = sum / count

# Convert data from absolute M(k_s, k) to percentual M(k_s, k)
for i in range(0, len(ks_vs_cb)):
    for j in range(0, len(ks_vs_cb[i])):
        ks_vs_cb[i][j] = ks_vs_cb[i][j] / len(G.nodes) * 100

# Visualize in the colormap grid format:
fig, ax = plt.subplots(1, 1)
im0 = ax.imshow(np.transpose(ks_vs_cb), cmap='jet',
                aspect=square_aspect_ratio_ks_cb,
                extent=(0, len(unique_coreness),
                        0, np.max(unique_centralities)),
                origin="lower")
xlim = (np.min(unique_coreness), np.max(unique_coreness))
ylim = (np.min(unique_centralities), np.max(unique_centralities))
y_labels = np.linspace(
    np.min(unique_centralities),
    math.floor(np.max(unique_centralities)*100)/100, 5)
ax.set_xticks(unique_coreness)
ax.set_yticks(y_labels)
ax.set_xticklabels(unique_coreness)
ax.set_yticklabels(y_labels)
ax.set_xlabel("Coreness $k_S$")
ax.set_ylabel("Betweenness Centrality $C_B$")
plt.colorbar(im0, ax=ax, label='$M$(%)')
plt.savefig(
    OUTPUT + 'ks_vs_cb_spreading_prediction.png')

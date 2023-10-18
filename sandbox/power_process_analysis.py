import matplotlib.pyplot as plt
import numpy as np
from scipy import io
import math

import networkx as nx
from networkx import algorithms as alg


def resize_image(im, nR, nC):
    # simple image scaling to (n × C) size def scale(im, nR, nC):
    nR0 = len(im)
    nC0 = len(im[0])  # source number of columns
    return [[im[int(nR0 * r / nR)][int(nC0 * c / nC)]
             for c in range(nC)] for r in range(nR)]


OUTPUT = "output/"
DEBUGGING = "debugging/"

# ----------------------------------------------------------------------- #
# get logged variable for plot debugging
mdic = io.loadmat(DEBUGGING + "/sir_simulation_email_beta8.mat")
NETWORK_NAME = mdic["NETWORK_NAME"][0]
M = mdic["M"][0]

# Read the nework
# G = nx.read_gml(f"data/{NETWORK_NAME}.gml", label="id")
G = nx.read_edgelist(
    f"data/{NETWORK_NAME}.txt", create_using=nx.Graph(), nodetype=int)
# Input graph has self loops which is not permitted
G.remove_edges_from(nx.selfloop_edges(G))
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

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
ks_vs_degree = np.zeros((len(unique_degrees), len(unique_coreness)))
square_aspect_ratio_ks_k = (unique_coreness[-1] - unique_coreness[0]
                            ) / (unique_degrees[-1] - unique_degrees[0])

# row index: coreness ks
# column index: degree k
for row_index, k in zip(
        range(0, len(ks_vs_degree)), unique_degrees):
    for column_index, ks in zip(
            range(0, len(ks_vs_degree[row_index])), unique_coreness):
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
im0 = ax.imshow(resize_image(ks_vs_degree, len(ks_vs_degree[:, 0]) // 5,
                             len(ks_vs_degree[0, :])), cmap='jet',
                aspect=square_aspect_ratio_ks_k,
                extent=(0, np.max(unique_coreness),
                        0, np.max(unique_degrees)),
                origin="lower", interpolation="none")
xlim = (np.min(unique_coreness), np.max(unique_coreness))
ylim = (np.min(unique_degrees), np.max(unique_degrees))
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xlabel("Coreness $k_S$")
ax.set_ylabel("Degree $k$")
plt.colorbar(im0, ax=ax, label='$M$(%)')
plt.savefig(
    OUTPUT + f'ks_vs_k_spreading_prediction_{NETWORK_NAME}.png')


# +-------------------------------------------------------------------------+
# |k-shell index vs betweenness centrality C_B spreading outcome prediction |
# +-------------------------------------------------------------------------+

# create object where to store the data for each of the plots, with the right
# dimensions. Each entry will correspond to a unique (k_s, k), and thus
# store the corresonding M(k_s, k)
ks_vs_cb = np.zeros((len(unique_centralities), len(unique_coreness), ))
square_aspect_ratio_ks_cb = (unique_coreness[-1] - unique_coreness[0]
                             ) / (unique_centralities[-1]
                                  - unique_centralities[0])

# row index: coreness ks
# column index: betweennes centrality cb
for row_index, cb in zip(
        range(0, len(ks_vs_cb)), unique_centralities):
    for column_index, ks in zip(
            range(0, len(ks_vs_cb[row_index])), unique_coreness):
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
donwsizing_ratio = 5
im0 = ax.imshow(resize_image(ks_vs_cb, len(ks_vs_cb[:, 0]) // 15,
                             len(ks_vs_cb[0, :])), cmap='jet',
                aspect=square_aspect_ratio_ks_cb,
                extent=(0, len(unique_coreness),
                        0, np.max(unique_centralities)),
                origin="lower", interpolation="none")
xlim = (np.min(unique_coreness), np.max(unique_coreness))
ylim = (np.min(unique_centralities), np.max(unique_centralities))
y_labels = np.linspace(
    np.min(unique_centralities),
    math.floor(np.max(unique_centralities)*100)/100, 5)
ax.set_xlim(xlim)
ax.set_ylim(ylim)
ax.set_xlabel("Coreness $k_S$")
ax.set_ylabel("Betweenness Centrality $C_B$")
plt.colorbar(im0, ax=ax, label='$M$(%)')
plt.savefig(
    OUTPUT + f'ks_vs_cb_spreading_prediction_{NETWORK_NAME}.png')

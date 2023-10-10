import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp

import matplotlib as mpl

from networkx import algorithms as alg

OUTPUT_PATH = "./output/"
CMAP_STYLE = "winter"


G = nx.read_gml("./data/karate.gml", label="id")

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure("Degree analysis of the network", figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(5, 4)

ax0 = fig.add_subplot(axgrid[0:3, :])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(Gcc, seed=10396953)
nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
ax0.set_title("Connected components of G")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

ax2 = fig.add_subplot(axgrid[3:, 2:])
ax2.bar(*np.unique(degree_sequence, return_counts=True))
ax2.set_title("Degree histogram")
ax2.set_xlabel("Degree")
ax2.set_ylabel("# of Nodes")

fig.tight_layout()
plt.savefig(OUTPUT_PATH + "network_characterisation.png")

"""Attribute to each node in the network its k_s (shell layer) value"""
shell_layer = 0
current_shell = nx.core.k_shell(G, k=shell_layer)
while (len(current_shell.nodes) != 0 or shell_layer == 0):
    for node in list(current_shell.nodes):
        G.nodes[node]["layer"] = shell_layer
    shell_layer += 1
    current_shell = nx.core.k_shell(G, k=shell_layer)

final_layer = shell_layer - 1


fig = plt.figure("Network and outer shell", figsize=(12, 6))

"""Plot a specific shell layer for the given network (final layer)"""
desired_layer = final_layer
shell = nx.core.k_shell(G, k=desired_layer)

# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(6, 6)

nodes_color = [
    'red' if G.nodes[n]["layer"] == desired_layer else 'blue' for n in G.nodes]

ax0 = fig.add_subplot(axgrid[:, 0:3])
Gcc = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])
pos = nx.spring_layout(Gcc, seed=10396953)
nx.draw(G, node_color=nodes_color, node_size=20, pos=pos)
ax0.set_title("Karate dataset - outer shell in red")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[:, 3:])
Gcc = shell.subgraph(sorted(
    nx.connected_components(shell), key=len, reverse=True)[0])
nx.draw_networkx_nodes(Gcc, pos, ax=ax1, node_size=20, node_color="red")
nx.draw_networkx_edges(Gcc, pos, ax=ax1, alpha=0.4)
ax1.set_title("Outer shell of karate dataset")
ax1.set_axis_off()

fig.tight_layout()
plt.savefig(OUTPUT_PATH + "network_and_outer_shell.png")


"""Characterise shell layer that each node belongs to"""
# This loop was just for debug purposes
# categorized_nodes = []
# for layer in range(0, final_layer + 1):
#     categorized_nodes.append(
#         [G.nodes[n]["layer"] == layer for n in G.nodes])
# categorized_nodes = np.array(categorized_nodes)

fig, ax = plt.subplots()
colors = [G.nodes[i]["layer"] for i in range(1, len(G.nodes)+1)]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Shell layer')
"""for layer in range(0, final_layer + 1):
    special_nodes = [n for n in G.nodes if G.nodes[n]["layer"] == layer]
    subgraph = nx.subgraph(G, special_nodes)
    nx.draw_networkx_nodes(
        subgraph, pos, node_size=40, node_color=COLORS[layer],
        label=f"layer {layer}")"""
nx.draw_networkx_nodes(
    G, pos, node_size=20,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax)
plt.title("Characterisation of shell layer each node belongs to")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "node_shell_characterisation.png")


"""Characterise degree of each node"""
fig, ax = plt.subplots()
"""for degree in range(degree_sequence[0], 0, -1):
    special_nodes = [n for n in G.nodes if G.degree[n] == degree]
    subgraph = nx.subgraph(G, special_nodes)
    nx.draw_networkx_nodes(
        subgraph, pos, node_size=20, node_color=COLORS[degree-1],
        label=f"degree {degree}")"""
colors = [tup[1] for tup in list(G.degree())]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Degree')
nx.draw_networkx_nodes(
    G, pos, node_size=20,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax)
plt.title("Characterisation of degree of each node")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "node_degree_characterisation.png")


"""Characterise betweenness centrality of each node"""
centrality = alg.betweenness_centrality(G)

fig, ax = plt.subplots()
"""for i, cent in enumerate(np.unique(list(centrality.values()))):
    special_nodes = [n for n in G.nodes if centrality[n] == cent]
    subgraph = nx.subgraph(G, special_nodes)
    nx.draw_networkx_nodes(
        subgraph, pos, node_size=20, node_color=COLORS[i],
        label=f"$C_B$ {cent:.3f}")"""
colors = list(centrality.values())
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Betweenness centrality')
nx.draw_networkx_nodes(
    G, pos, node_size=20,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax)
plt.title("Characterisation of betweenness centrality of each node")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + "node_centrality_characterisation.png")

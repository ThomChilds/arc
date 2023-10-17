import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl

from networkx import algorithms as alg

OUTPUT_PATH = "./output/"
CMAP_STYLE = "winter"
NETWORK_NAME = "karate"

"""FROM GML FORMAT"""
G = nx.read_gml(f"./data/{NETWORK_NAME}.gml", label="id")

"""# FROM .TXT FILE"""
# G = nx.read_edgelist(
#     f"data/{NETWORK_NAME}.txt", create_using=nx.Graph(), nodetype=int)

"""From network model"""
# G = nx.barabasi_albert_graph(n=100, m=2)
# G = nx.watts_strogatz_graph(1000, 5, 0.1)

"""Remove self loops and disconnected components"""
G.remove_edges_from(nx.selfloop_edges(G))
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure(f"Degree analysis of the {NETWORK_NAME} network",
                 figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(5, 4)

ax0 = fig.add_subplot(axgrid[0:3, :])
pos = nx.spring_layout(G, seed=10396953)
nx.draw_networkx_nodes(G, pos, ax=ax0, node_size=10)
nx.draw_networkx_edges(G, pos, ax=ax0, alpha=0.4, width=0.1)
ax0.set_title(f"Connected components of the {NETWORK_NAME} network")
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
plt.savefig(OUTPUT_PATH + f"network_characterisation_{NETWORK_NAME}.png")


"""Attribute to each node in the network its k_s (shell layer) value"""
shell_layer = 0
current_shell = nx.core.k_shell(G, k=shell_layer)
while (len(current_shell.nodes) != 0 or shell_layer == 0):
    for node in list(current_shell.nodes):
        G.nodes[node]["layer"] = shell_layer
    shell_layer += 1
    current_shell = nx.core.k_shell(G, k=shell_layer)

final_layer = shell_layer - 1


fig = plt.figure(f"{NETWORK_NAME} network and outer shell", figsize=(12, 6))

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
ax0.set_title(f"{NETWORK_NAME} network - outer shell in red")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[:, 3:])
Gcc = shell.subgraph(sorted(
    nx.connected_components(shell), key=len, reverse=True)[0])
nx.draw_networkx_nodes(Gcc, pos, ax=ax1, node_size=20, node_color="red")
nx.draw_networkx_edges(Gcc, pos, ax=ax1, alpha=0.4)
ax1.set_title(f"Outer shell of the {NETWORK_NAME} network")
ax1.set_axis_off()

fig.tight_layout()
plt.savefig(OUTPUT_PATH + f"network_and_outer_shell_{NETWORK_NAME}.png")


"""Characterise shell layer that each node belongs to"""
fig, ax = plt.subplots()
colors = [G.nodes[i]["layer"] for i in list(G.nodes)]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Shell layer')
nx.draw_networkx_nodes(
    G, pos, node_size=20,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax)
plt.title("Characterisation of shell layer each node belongs to")
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_PATH + f"node_shell_characterisation_{NETWORK_NAME}.png")


"""Characterise degree of each node"""
fig, ax = plt.subplots()
colors = [tup[1] for tup in list(G.degree())]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Degree')
nx.draw_networkx_nodes(
    G, pos, node_size=20,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax)
plt.title("Characterisation of the degree of each node")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + f"node_degree_characterisation_{NETWORK_NAME}.png")


"""Characterise betweenness centrality of each node"""
centrality = alg.betweenness_centrality(G)

fig, ax = plt.subplots()
colors = list(centrality.values())
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Betweenness centrality')
nx.draw_networkx_nodes(
    G, pos, node_size=20,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax)
plt.title("Characterisation of the betweenness centrality of each node")
plt.tight_layout()
plt.savefig(
    OUTPUT_PATH + f"node_centrality_characterisation_{NETWORK_NAME}.png")

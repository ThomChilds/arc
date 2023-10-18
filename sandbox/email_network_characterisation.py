import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl

from networkx import algorithms as alg

OUTPUT_PATH = "./output/"
CMAP_STYLE = "winter"
NETWORK_NAME = "email"

NODE_SIZE = 5
EDGE_WIDTH = 0.1

"""FROM GML FORMAT"""
# G = nx.read_gml(f"./data/{NETWORK_NAME}.gml", label="id")

"""# FROM .TXT FILE"""
G = nx.read_edgelist(
    f"data/{NETWORK_NAME}.txt", create_using=nx.Graph(), nodetype=int)

"""From network model"""
# G = nx.barabasi_albert_graph(n=1000, m=3)
# G = nx.watts_strogatz_graph(1000, 5, 0.1)
# G = nx.erdos_renyi_graph(1000, 0.02)

"""Remove self loops and disconnected components"""
G.remove_edges_from(nx.selfloop_edges(G))
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
dmax = max(degree_sequence)

centrality = alg.betweenness_centrality(G)
centralities = [v for _, v in centrality.items()]

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

fig = plt.figure(f"Analysis of the {NETWORK_NAME} network",
                 figsize=(8, 8))
# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(5, 6)

ax0 = fig.add_subplot(axgrid[0:3, :])
# pos = nx.spring_layout(G, seed=10396953)
pos = nx.kamada_kawai_layout(G)
nx.draw_networkx_nodes(G, pos, ax=ax0, node_size=NODE_SIZE)
nx.draw_networkx_edges(G, pos, ax=ax0, alpha=0.4, width=EDGE_WIDTH)
ax0.set_title(f"Connected components of the {NETWORK_NAME} network")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.bar(*np.unique(degree_sequence, return_counts=True))
ax1.set_title("Degree histogram")
ax1.set_xlabel("Degree")
ax1.set_ylabel("# of Nodes")

ax2 = fig.add_subplot(axgrid[3:, 2:4])
ax2.bar(*np.unique(centralities, return_counts=True),
        width=np.mean(np.diff(np.unique(centralities)))*50)
ax2.set_title("Centrality histogram")
ax2.set_xlabel("Betweenness Centrality")
ax2.set_ylabel("# of Nodes")

ax3 = fig.add_subplot(axgrid[3:, 4:])
ax3.bar(*np.unique(corenesses, return_counts=True))
ax3.set_title("Coreness histogram")
ax3.set_xlabel("Coreness")
ax3.set_ylabel("# of Nodes")

fig.tight_layout()
plt.savefig(OUTPUT_PATH + f"network_characterisation_{NETWORK_NAME}.png")


"""Attribute to each node in the network its k_s (shell layer) value"""
fig = plt.figure(f"{NETWORK_NAME} network and outer shell", figsize=(12, 6))

"""Plot a specific shell layer for the given network (final layer)"""
desired_layer = final_layer
shell = nx.core.k_shell(G, k=desired_layer)

# Create a gridspec for adding subplots of different sizes
axgrid = fig.add_gridspec(6, 6)

nodes_color = [
    'red' if G.nodes[n]["layer"] == desired_layer else 'blue' for n in G.nodes]

ax0 = fig.add_subplot(axgrid[:, 0:3])
nx.draw(G, node_color=nodes_color, node_size=NODE_SIZE,
        width=EDGE_WIDTH, pos=pos)
ax0.set_title(
    f"Charachterisation of the {NETWORK_NAME} network - outer shell in red")
ax0.set_axis_off()

ax1 = fig.add_subplot(axgrid[:, 3:])
Gcc = shell.subgraph(sorted(
    nx.connected_components(shell), key=len, reverse=True)[0])
nx.draw_networkx_nodes(Gcc, pos, ax=ax1, node_size=NODE_SIZE, node_color="red")
nx.draw_networkx_edges(Gcc, pos, ax=ax1, alpha=0.4, width=EDGE_WIDTH)
ax1.set_title(f"Outer shell of the {NETWORK_NAME} network (detail)")
ax1.set_axis_off()

fig.tight_layout()
plt.savefig(OUTPUT_PATH + f"network_and_outer_shell_{NETWORK_NAME}.png")


"""Characterise shell layer that each node belongs to"""
fig, ax = plt.subplots()
colors = [G.nodes[i]["layer"] for i in list(G.nodes)]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Coreness ($k_S$)')
nx.draw_networkx_nodes(
    G, pos, node_size=NODE_SIZE,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax, width=EDGE_WIDTH)
plt.title("Coreness ($k_S$) of each node")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + f"node_coreness_characterisation_{NETWORK_NAME}.png")


"""Characterise degree of each node"""
fig, ax = plt.subplots()
colors = [tup[1] for tup in list(G.degree())]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Degree ($k$)')
nx.draw_networkx_nodes(
    G, pos, node_size=NODE_SIZE,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax, width=EDGE_WIDTH)
plt.title("Degree ($k$) of each node")
plt.tight_layout()
plt.savefig(OUTPUT_PATH + f"node_degree_characterisation_{NETWORK_NAME}.png")


"""Characterise betweenness centrality of each node"""
fig, ax = plt.subplots()
colors = list(centrality.values())
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Betweenness Centrality ($C_B$)')
nx.draw_networkx_nodes(
    G, pos, node_size=NODE_SIZE,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax, width=EDGE_WIDTH)
plt.title("Betweenness Centrality $C_B$ of each node")
plt.tight_layout()
plt.savefig(
    OUTPUT_PATH + f"node_centrality_characterisation_{NETWORK_NAME}.png")

"""Plot with all three characteristics as subplots"""
"""Coreness"""
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12, 4))
colors = [G.nodes[i]["layer"] for i in list(G.nodes)]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax[0], label='Coreness ($k_S$)')
nx.draw_networkx_nodes(
    G, pos, node_size=NODE_SIZE,
    node_color=colors, cmap=CMAP_STYLE, ax=ax[0])
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax[0], width=EDGE_WIDTH)
ax[0].set_title("Coreness ($k_S$) of each node")


"""Degree"""
colors = [tup[1] for tup in list(G.degree())]
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax[1], label='Degree ($k$)')
nx.draw_networkx_nodes(
    G, pos, node_size=NODE_SIZE,
    node_color=colors, cmap=CMAP_STYLE, ax=ax[1])
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax[1], width=EDGE_WIDTH)
ax[1].set_title("Degree ($k$) of each node")


"""Betweenness Centrality"""
centrality = alg.betweenness_centrality(G)
colors = list(centrality.values())
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax[2], label='Betweenness Centrality ($C_B$)')
nx.draw_networkx_nodes(
    G, pos, node_size=NODE_SIZE,
    node_color=colors, cmap=CMAP_STYLE, ax=ax[2])
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax[2], width=EDGE_WIDTH)
ax[2].set_title("Betweenness Centrality $C_B$ of each node")
plt.tight_layout()
plt.savefig(
    OUTPUT_PATH + f"centrality_degree_coreness_{NETWORK_NAME}.png")

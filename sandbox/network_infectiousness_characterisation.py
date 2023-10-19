import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

from scipy import io
from networkx import algorithms as alg


OUTPUT_PATH = "./output/"
CMAP_STYLE = "jet"
NETWORK_NAME = "power"

NODE_SIZE = 5
EDGE_WIDTH = 0.1

OUTPUT = "output/"
DEBUGGING = "debugging/"

# ----------------------------------------------------------------------- #
# get logged variable for plot debugging
mdic = io.loadmat(DEBUGGING + "sir_simulation_power_beta65.mat")
NETWORK_NAME = mdic["NETWORK_NAME"][0]
M = mdic["M"][0]

# Read the nework
G = nx.read_gml(f"data/{NETWORK_NAME}.gml", label="id")
# G = nx.read_edgelist(
#     f"data/{NETWORK_NAME}.txt", create_using=nx.Graph(), nodetype=int)
# Input graph has self loops which is not permitted
G.remove_edges_from(nx.selfloop_edges(G))
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])


"""Spreading potential of each node"""
fig, ax = plt.subplots(nrows=1, ncols=1)
colors = list(M/len(G.nodes)*100)
norm = mpl.colors.Normalize(vmin=min(colors), vmax=max(colors))
pos = nx.kamada_kawai_layout(G)
fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=CMAP_STYLE),
             ax=ax, label='Percentage of network infected')
nx.draw_networkx_nodes(
    G, pos, node_size=NODE_SIZE,
    node_color=colors, cmap=CMAP_STYLE, ax=ax)
nx.draw_networkx_edges(G, pos, alpha=0.4, ax=ax, width=EDGE_WIDTH)
ax.set_title(f"Spreading potential of each node in the {NETWORK_NAME} network")
ax.text(
    5.0, 5.0, "SIR model, $\\beta$ = 4%\nColormap reflects the percentage of\
        the network infected for a spreading process initiated at that node",
    bbox=dict(facecolor='yellow', alpha=1.0), fontsize="x-small")
plt.tight_layout()
plt.savefig(
    OUTPUT_PATH + f"cmap_spreading_potential_{NETWORK_NAME}.png")

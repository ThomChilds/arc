import matplotlib.pyplot as plt
import numpy as np
from scipy import io
import math

import networkx as nx
from networkx import algorithms as alg


OUTPUT = "output/"
DEBUGGING = "debugging/"

# ----------------------------------------------------------------------- #
# get logged variable for plot debugging
mdic = io.loadmat(DEBUGGING + "/sir_simulation_email-Eu-core.mat")
NETWORK_NAME = mdic["NETWORK_NAME"][0]
M = mdic["M"][0]

# Read the nework
# G = nx.read_gml(f"data/{NETWORK_NAME}.gml", label="id")
G = nx.read_edgelist(
    f"data/{NETWORK_NAME}.txt", create_using=nx.Graph(), nodetype=int)
# Input graph has self loops which is not permitted
G.remove_edges_from(nx.selfloop_edges(G))
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])


for i, node in enumerate(G.nodes):
    G["M"] = M[i]


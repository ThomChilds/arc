import numpy as np
from scipy import io

import networkx as nx

import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mconf

NETWORK_NAME = "power"


"""Network selection in which to simulate the infection/spreading process"""
"""FROM .GML FILE"""
G = nx.read_gml(f"data/{NETWORK_NAME}.gml", label="id")

"""FROM MODEL NETWORK"""
# G = nx.erdos_renyi_graph(1000, 0.1)
# G = nx.watts_strogatz_graph(1000, 5, 0.1)
# G = nx.barabasi_albert_graph(n=100, m=2)

"""FROM .TXT FILE"""
# G = nx.read_edgelist(
#     f"data/{NETWORK_NAME}.txt", create_using=nx.Graph(), nodetype=int)
# Input graph has self loops which is not permitted
G.remove_edges_from(nx.selfloop_edges(G))
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

NUMBER_NODES = G.number_of_nodes()
print(f"The total number of nodes is {NUMBER_NODES}.")

"""SIR infection model parameters."""
#     infected nodes will infect other nodes with probability beta, and recover
#     (become non-susceptible to reinfection) after one timestep
BETA = 0.65  # P(infectious node infecting a susceptible neighbour)
GAMMA = 1.0  # P(infectious node becoming recovered after one timestep)
NUM_ITERATIONS = 30  # Number of iterations for which to perform simulation
NUM_REPETITION_EACH_NODE = 50  # Number of realisations for each starting node

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
    print(f"Progress: {round(i/NUMBER_NODES*100, 3)}.")


# +-------------------------------------------------------------------------+
# FROM HERE ON IS JUST ANALYSIS; SO LET'S SAVE TO .mat FILE
# +-------------------------------------------------------------------------+
mdic = {"M": M,
        "NETWORK_NAME": NETWORK_NAME}
io.savemat(
    DEBUGGING + f"sir_simulation_{NETWORK_NAME}_beta{int(BETA * 100)}.mat",
    mdic)

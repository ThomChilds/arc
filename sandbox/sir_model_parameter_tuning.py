import networkx as nx
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mconf
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend

NETWORK_NAME = "email"
OUTPUT = "output/"

# Select the node in which to start the infection
starting_node = 0

# Relevant Datasets
# G = nx.read_gml(f"./data/{NETWORK_NAME}.gml", label="id")
# G = nx.erdos_renyi_graph(1000, 0.1)
# G = nx.watts_strogatz_graph(1000, 5, 0.1)
G = nx.barabasi_albert_graph(n=1000, m=3)
# G = nx.read_edgelist(
#     f"data/{NETWORK_NAME}.txt", create_using=nx.Graph(), nodetype=int)
# Input graph has self loops which is not permitted
G.remove_edges_from(nx.selfloop_edges(G))
G = G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

# Choose which model to use SIR or SIS (maybe SEIR)
model = ep.SIRModel(G)
config = mconf.Configuration()
config.add_model_parameter('beta', 0.17)
config.add_model_parameter('gamma', 1.0)
initial_infected = [starting_node]
config.add_model_initial_configuration('Infected', initial_infected)
model.set_initial_status(config)

# Sim
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)

# Plotting
viz = DiffusionTrend(model, trends)
viz.plot(
    OUTPUT + f"diffusion_trend_start_node_{starting_node}_{NETWORK_NAME}.png")

import networkx as nx
import matplotlib
import random
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig  as mconf
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend

### Relevant Datasets
G = nx.read_gml("../data/dolphins.gml", label="id")
# G = nx.erdos_renyi_graph(1000, 0.1)
# G = nx.watts_strogatz_graph(1000, 5, 0.1)
# G = nx.barabasi_albert_graph(n=100, m=2)
nx.draw(G, node_size=75)

# SIS Model
model= ep.SISModel(G)
config = mconf.Configuration()
config.add_model_parameter('beta', 0.01)
config.add_model_parameter('lambda', 0.8)
config.add_model_parameter('fraction_infected', 0.2)
model.set_initial_status(config)

# Sim
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)

# Plotting
nx.draw(G, node_size=75)
viz = DiffusionTrend(model, trends)
viz.plot()


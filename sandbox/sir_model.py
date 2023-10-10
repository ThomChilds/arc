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

# Choose which model to use SIR or SIS (maybe SEIR)
model = ep.SIRModel(G)
config = mconf.Configuration()
config.add_model_parameter('beta', 0.2)
config.add_model_parameter('gamma', 0.2)
initial_infected = [0, 1, 2]
config.add_model_initial_configuration('Infected', initial_infected)
# config.add_model_parameter('fraction_infected', 0.2)
model.set_initial_status(config)
# first_infected = random.choice(list(G.nodes()))

# Sim
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)

# Plotting
viz = DiffusionTrend(model, trends)
viz.plot()


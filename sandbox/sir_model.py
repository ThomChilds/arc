import networkx as nx
import matplotlib
import random
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig  as mconf
from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend


G = nx.read_gml("../data/dolphins.gml", label="id")
# G = nx.erdos_renyi_graph(1000, 0.1)
   
# for node in G.nodes():
#     G.nodes[node]['state'] = 'S'
#
#
# transmission_rate = 0.3
# recovery_rate = 0.1
#
# first_infected = random.choice(list(G.nodes()))
# G.nodes[first_infected]['state'] = 'I'
#
# sim_time = 50
# for t in range(sim_time):
#     G_aux = G.copy()
#
#     for node in G.nodes():
#         if G.node[node]['state'] == 'I':
#             neighbors = list(G.neighbors(node))

# Choose which model to use SIR or SIS (maybe SEIR)
model = ep.SIRModel(G)
config = mconf.Configuration()
config.add_model_parameter('beta', 0.1)
config.add_model_parameter('gamma', 0.1)
config.add_model_parameter('fraction_infected', 0.1)
# first_infected = random.choice(list(G.nodes()))
# config.add_model_initial_configuration("Infected", first_infected)

model.set_initial_status(config)

# Sim
iterations = model.iteration_bunch(200)
trends = model.build_trends(iterations)

# Plotting
viz = DiffusionTrend(model, trends)
viz.plot()




import os
import random
from compas.datastructures import Network
from compas.utilities import pairwise
from compas_plotters import NetworkPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'irregular.obj')

net = Network.from_obj(FILE)

start = random.choice(list(net.leaves()))
goal = random.choice(list(net.leaves()))
nodes = net.shortest_path(start, goal)

node_color = {}
edge_color = {}
edge_width = {}

for u, v in pairwise(nodes):
    node_color[v] = (0, 255, 0)
    edge_color[u, v] = edge_color[v, u] = (0, 255, 0)
    edge_width[u, v] = edge_width[v, u] = 3

node_color[start] = (255, 0, 0)
node_color[goal] = (0, 0, 255)

plotter = NetworkPlotter(net, figsize=(12, 7.5))
plotter.draw_nodes(facecolor=node_color)
plotter.draw_edges(color=edge_color, width=edge_width)
plotter.show()

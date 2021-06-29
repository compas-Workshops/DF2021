import os
from compas.datastructures import Network
from compas_plotters import NetworkPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'irregular.obj')

net = Network.from_obj(FILE)

node = 0
nbrs = net.neighbors(node)

node_color = {node: (255, 0, 0)}
for nbr in nbrs:
    node_color[nbr] = (0, 0, 255)

edge_color = {}
for nbr in nbrs:
    edge_color[node, nbr] = (0, 255, 0)
    edge_color[nbr, node] = (0, 255, 0)

plotter = NetworkPlotter(net, figsize=(12, 7.5))
plotter.draw_nodes(facecolor=node_color)
plotter.draw_edges(color=edge_color, width={edge: 2.0 for edge in edge_color})
plotter.show()

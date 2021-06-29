import os
from compas.datastructures import Network
from compas_plotters import NetworkPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'irregular.obj')

net = Network.from_obj(FILE)

node_color = {}
for node in net.nodes():
    nbrs = net.neighbors(node)
    if len(nbrs) == 5:
        node_color[node] = (255, 0, 0)

plotter = NetworkPlotter(net, figsize=(12, 7.5))
plotter.draw_nodes(facecolor=node_color)
plotter.draw_edges()
plotter.show()

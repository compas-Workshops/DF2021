import os
from compas.datastructures import Network
from compas_plotters import NetworkPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'irregular.obj')

net = Network.from_obj(FILE)

plotter = NetworkPlotter(net)
plotter.draw_nodes()
plotter.draw_edges()
plotter.show()

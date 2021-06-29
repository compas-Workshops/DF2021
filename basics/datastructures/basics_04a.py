import os
from compas.datastructures import Network
from compas_plotters import NetworkPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'lines.obj')

net = Network.from_obj(FILE)

nodes = sorted(net.nodes(), key=lambda node: net.node_attributes(node, 'xy'))

plotter = NetworkPlotter(net)

plotter.draw_nodes(facecolor={nodes[-1]: (0, 255, 0)})
plotter.draw_edges()

plotter.show()

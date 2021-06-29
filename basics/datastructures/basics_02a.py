import os
from compas.datastructures import Network

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'lines.obj')

net = Network.from_obj(FILE)

net.update_default_edge_attributes({'traffic': 0})

print(sorted(net.nodes(), key=lambda node: net.node_attributes(node, 'xy')))

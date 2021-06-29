import os
from compas.datastructures import Network

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'lines.obj')

net = Network.from_obj(FILE)

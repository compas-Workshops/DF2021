import os
import random
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'faces.obj')

mesh = Mesh.from_obj(FILE)

start = random.choice(list(mesh.edges()))
edges = mesh.edge_loop(start)

edge_color = {}
for edge in edges:
    edge_color[edge] = (0, 255, 0)

edge_color[start] = (255, 0, 0)

plotter = MeshPlotter(mesh, figsize=(12, 7.5))
plotter.draw_vertices()
plotter.draw_faces()
plotter.draw_edges(keys=edges, color=edge_color, width=2.0)
plotter.show()

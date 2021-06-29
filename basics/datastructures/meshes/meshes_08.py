import os
import random
from compas.datastructures import Mesh
from compas.utilities import flatten
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'twisted.obj')

mesh = Mesh.from_obj(FILE)

start = random.choice(list(mesh.edges()))
loop = mesh.edge_loop(start)
strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
strip[:] = list(set(flatten(strip)))

edgecolor = {}
for edge in loop:
    edgecolor[edge] = (0, 255, 0)

edgecolor[start] = (255, 0, 0)

facecolor = {}
for face in strip:
    facecolor[face] = (255, 200, 200)

plotter = MeshPlotter(mesh, figsize=(12, 7.5))
plotter.draw_vertices(radius=0.03)
plotter.draw_faces(facecolor=facecolor)
plotter.draw_edges(keys=loop, color=edgecolor, width=2.0)
plotter.show()

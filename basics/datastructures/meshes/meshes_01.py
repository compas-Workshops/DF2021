import os
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'faces.obj')

mesh = Mesh.from_obj(FILE)

vertex = list(set(mesh.vertices()) - set(mesh.vertices_on_boundary()))[0]
nbrs = mesh.vertex_neighbors(vertex)

vertex_color = {vertex: (255, 0, 0)}
for nbr in nbrs:
    vertex_color[nbr] = (0, 0, 255)

edge_color = {}
for nbr in nbrs:
    edge_color[vertex, nbr] = (0, 255, 0)
    edge_color[nbr, vertex] = (0, 255, 0)

plotter = MeshPlotter(mesh, figsize=(12, 7.5))

plotter.draw_vertices(facecolor=vertex_color)
plotter.draw_faces()
plotter.draw_edges(keys=edge_color, color=edge_color, width=2)

plotter.show()

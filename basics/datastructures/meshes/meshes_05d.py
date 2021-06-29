import os
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'faces.obj')

mesh = Mesh.from_obj(FILE)

boundary = mesh.vertices_on_boundary()
vertex = boundary[-4]
nbrs = mesh.vertex_neighbors(vertex, ordered=True)

color = {vertex: (255, 0, 0)}
color[nbrs[1]] = (255, 0, 0)

prev = vertex
vertex = nbrs[1]

nbrs = mesh.vertex_neighbors(vertex, ordered=True)
index = nbrs.index(prev)
nbrs = nbrs[index:] + nbrs[:index]

text = {}
for index, nbr in enumerate(nbrs):
    text[nbr] = str(index)

plotter = MeshPlotter(mesh, figsize=(12, 7.5))
plotter.defaults['vertex.fontsize'] = 8
plotter.draw_faces()
plotter.draw_vertices(facecolor=color, text=text, radius=0.2)
plotter.show()

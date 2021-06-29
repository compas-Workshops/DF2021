import os
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'faces.obj')

mesh = Mesh.from_obj(FILE)

vertices = sorted(mesh.vertices(), key=lambda vertex: mesh.vertex_attributes(vertex, 'xy'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(facecolor={vertices[0]: (255, 0, 0)})
plotter.draw_faces()
plotter.draw_edges()

plotter.show()

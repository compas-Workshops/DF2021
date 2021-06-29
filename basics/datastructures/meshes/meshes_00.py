import os
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'faces.obj')

mesh = Mesh.from_obj(FILE)

plotter = MeshPlotter(mesh, figsize=(12, 7.5))

plotter.draw_vertices()
plotter.draw_faces()

plotter.show()

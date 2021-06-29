import os
from compas.datastructures import Mesh
from compas_plotters import MeshPlotter

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, 'faces.obj')

mesh = Mesh.from_obj(FILE)

vertices = sorted(mesh.vertices(), key=lambda vertex: mesh.vertex_attributes(vertex, 'yx'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(
    text={vertex: str(index) for index, vertex in enumerate(vertices)},
    radius=0.2,
    facecolor={vertices[0]: (255, 0, 0), vertices[-1]: (0, 0, 255)}
)
plotter.draw_faces()
plotter.draw_edges()

plotter.show()

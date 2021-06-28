from random import random, choice

from compas.geometry import Pointcloud
from compas.geometry import Translation
from compas.geometry import scale_vector, normalize_vector
from compas.utilities import i_to_rgb
from compas_plotters import GeometryPlotter


def random_vector():
    vector = [choice([-1, +1]) * random(), choice([-1, +1]) * random(), 0]
    return scale_vector(normalize_vector(vector), random())


pcl = Pointcloud.from_bounds(10, 5, 0, 100)

plotter = GeometryPlotter(show_axes=True)

for point in pcl.points:
   plotter.add(point, facecolor=i_to_rgb(random(), normalize=True))

transformations = [Translation.from_vector(random_vector()) for _ in pcl]

plotter.zoom_extents()
plotter.pause(1)

for i in range(100):
   for point, T in zip(pcl, transformations):
       point.transform(T)
   plotter.redraw(pause=0.01)

plotter.show()


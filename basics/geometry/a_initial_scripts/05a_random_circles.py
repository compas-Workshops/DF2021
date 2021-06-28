import random

from compas.geometry import Pointcloud, Circle
from compas.utilities import i_to_red, i_to_green
from compas_plotters import GeometryPlotter

pcl = Pointcloud.from_bounds(10, 5, 0, 100)

plotter = GeometryPlotter(show_axes=True)

for point in pcl.points:
    plotter.add(point)

plotter.zoom_extents()
plotter.show()
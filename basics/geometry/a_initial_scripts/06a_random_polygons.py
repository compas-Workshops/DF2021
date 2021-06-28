import random
import math

from compas.geometry import Pointcloud, Polygon
from compas.geometry import Translation, Rotation
from compas_plotters import GeometryPlotter

pcl = Pointcloud.from_bounds(10, 5, 0, 10 * 4)
base = Polygon.from_sides_and_radius_xy(5, 0.3)

plotter = GeometryPlotter(show_axes=True)

for point in pcl.points:
    plotter.add(point)

plotter.zoom_extents()
plotter.show()

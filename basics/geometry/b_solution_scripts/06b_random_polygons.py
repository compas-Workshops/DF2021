import random
import math

from compas.geometry import Pointcloud, Polygon
from compas.geometry import Translation, Rotation
from compas_plotters import GeometryPlotter

pcl = Pointcloud.from_bounds(10, 5, 0, 10 * 4)
base = Polygon.from_sides_and_radius_xy(5, 0.3)

plotter = GeometryPlotter(show_axes=True)

for point in pcl.points:
   polygon = base.copy()
   T = Translation.from_vector(point)
   R = Rotation.from_axis_and_angle([0, 0, 1], random.random() * math.pi)
   X = T * R
   polygon.transform(X)
   plotter.add(polygon)

plotter.zoom_extents()
plotter.show()
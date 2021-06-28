from random import random
from compas.geometry import Pointcloud
from compas.geometry import Vector, Plane, Circle
from compas_plotters import GeometryPlotter

plotter = GeometryPlotter(figsize=(8, 5))

for point in Pointcloud.from_bounds(8, 5, 0, 17):
    plane = Plane(point, Vector(0, 0, 1))
    radius = random()
    circle = Circle(plane, radius)
    plotter.add(circle,
                facecolor=(1, radius, radius),
                edgecolor=(radius, 1, radius))

plotter.zoom_extents()
plotter.show()

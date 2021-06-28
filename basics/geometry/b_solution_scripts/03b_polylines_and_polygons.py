from compas.geometry import Point
from compas.geometry import Polyline, Polygon
from compas_plotters import GeometryPlotter

a = Point(0, 0)
b = Point(1, 0)
c = Point(1, 1)
d = Point(0, 1)

p1 = Polyline([a, b, c, d])
p2 = Polygon([a, b, c, d])

plotter = GeometryPlotter(show_axes=True)

plotter.add_from_list([a, b, c, d])

plotter.add(p1, color=(1, 0, 0), linewidth=3)
plotter.add(p2, facecolor=(0.7, 0.7, 1), linewidth=0)

plotter.zoom_extents()
plotter.show()

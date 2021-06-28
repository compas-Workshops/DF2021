from compas.geometry import Point
from compas.geometry import Line, Circle
from compas_plotters import GeometryPlotter

a = Point(0, 0)
b = Point(1, 0)
c = Point(1, 1)
d = Point(0, 1)

plotter = GeometryPlotter(show_axes=True)

plotter.add(a)
plotter.add(b)
plotter.add(c)
plotter.add(d)

plotter.zoom_extents()
plotter.show()

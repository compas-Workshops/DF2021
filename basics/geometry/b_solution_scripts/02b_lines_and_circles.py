from compas.geometry import Point
from compas.geometry import Line, Circle
from compas_plotters import GeometryPlotter

a = Point(0, 0)
b = Point(1, 0)
c = Point(1, 1)
d = Point(0, 1)

ac = Line(a, c)
c1 = Circle([b, [0, 0, 1]], 0.3)
c2 = Circle([d, [0, 0, 1]], 0.2)

plotter = GeometryPlotter(show_axes=True)

plotter.add(a)
plotter.add(b)
plotter.add(c)
plotter.add(d)

plotter.add(ac, color=(1, 0, 0))
plotter.add(c1, facecolor=(0.7, 1, 0.7), edgecolor=(0, 1, 0))
plotter.add(c2, facecolor=(0.7, 0.7, 1), edgecolor=(0, 0, 1))

plotter.zoom_extents()
plotter.show()
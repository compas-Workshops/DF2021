from compas.geometry import Point
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

plotter.add(b - a, point=a, color=(1, 0, 0))
plotter.add(c - b, point=b, color=(1, 1, 0))
plotter.add(d - c, point=c, color=(0, 1, 0))
plotter.add(a - d, point=d, color=(0, 0, 1))

plotter.zoom_extents()
plotter.show()
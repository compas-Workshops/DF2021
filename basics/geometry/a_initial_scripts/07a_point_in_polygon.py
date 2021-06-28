from compas.geometry import Pointcloud, Polygon
from compas.geometry import Translation
from compas_plotters import GeometryPlotter

pcl = Pointcloud.from_bounds(10, 5, 0, 100)
polygon = Polygon.from_sides_and_radius_xy(5, 2.0)
polygon.transform(Translation.from_vector([5, 2.5, 0]))

plotter = GeometryPlotter(show_axes=True)

plotter.add(polygon, edgecolor=(0, 0, 1), facecolor=(0.7, 0.7, 1.0))

for point in pcl.points:
    facecolor = (1, 1, 1)
    plotter.add(point, facecolor=facecolor)

plotter.zoom_extents()
plotter.show()

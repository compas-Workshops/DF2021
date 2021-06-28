from compas.geometry import Pointcloud, Polygon, Line
from compas.geometry import Translation
from compas.geometry import intersection_line_segment_xy
from compas.utilities import grouper, pairwise
from compas_plotters import GeometryPlotter

pcl = Pointcloud.from_bounds(10, 5, 0, 50)
polygon = Polygon.from_sides_and_radius_xy(5, 1.0)
polygon.transform(Translation.from_vector([5, 2.5, 0]))

plotter = GeometryPlotter(show_axes=True, figsize=(12, 7.5))

plotter.add(polygon, edgecolor=(0, 0, 1), facecolor=(0.7, 0.7, 1.0))

lines = []
for a, b in grouper(pcl.points, 2):
    line = Line(a, b)
    lines.append(line)
    plotter.add(line, color=(0.5, 0.5, 0.5))

plotter.redraw()
plotter.zoom_extents()
plotter.show()

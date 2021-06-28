import math
import random

from compas.geometry import Pointcloud
from compas.geometry import Translation, Rotation
from compas.geometry import Box
from compas.geometry import is_point_infront_plane
from compas.datastructures import Mesh

from compas_rhino.artists import PointArtist
from compas_rhino.artists import MeshArtist


pcl = Pointcloud.from_bounds(10, 5, 3, 100)
box = Box.from_width_height_depth(2, 2, 2)

T = Translation.from_vector([5, 2.5, 1.5])
R = Rotation.from_axis_and_angle([0, 0, 1], random.random() * math.pi)

box.transform(T * R)
mesh = Mesh.from_shape(box)

colors = []
for point in pcl:
    colors.append((0, 0, 255))

PointArtist.draw_collection(pcl, colors=colors, layer="ITA20::PCL", clear=True)

artist = MeshArtist(mesh, layer="ITA20::Box")
artist.clear_layer()
artist.draw_faces()
artist.draw_edges()

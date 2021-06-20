# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.geometry import Polyline, Frame, Transformation
from compas.geometry import project_points_plane
from compas.datastructures import Mesh
from compas.utilities import flatten
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolylineArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin_add_patch.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)


proxy = Proxy('compas.geometry')
bestfit = proxy.bestfit_frame_numpy

# (18, 31), (78, 87), (83, 73)
#start = (638, 842)
start = (1343, 1344)

# find the edge loop
loop = mesh.edge_loop(start)
loop_vertices = list(flatten(loop)) # not chained
seen = set()
loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]
points = mesh.vertices_attributes('xyz', keys=loop_vertices)
polyline = Polyline(points)
local_frame = bestfit(polyline)
world = Frame.worldXY()
T = Transformation.from_frame_to_frame(Frame(*local_frame), world)

polyline_T = polyline.transformed(T)
# # if the polyline is not in xy plane, run the following 
# points = polyline_T.points
# print(points)
# xy_points = project_points_plane(points, ([0, 0, 0], [0, 0, 1]))
# polyline_T = Polyline(xy_points)

polyartist=  PolylineArtist(polyline_T, layer="DF2021:: Arch")
polyartist.clear_layer()
polyartist.draw(show_points=True)

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u,v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})),join_faces=True)
artist.draw_edges(color=edgecolor)
artist.draw_vertexlabels()
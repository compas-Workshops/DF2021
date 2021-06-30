# ==============================================================================
# Import
# ==============================================================================
import os

from compas.geometry import Polyline, Frame, Transformation
from compas.geometry import offset_polyline, project_points_plane
from compas.geometry import normalize_vector, scale_vector, cross_vectors, subtract_vectors, dot_vectors, add_vectors
from compas.datastructures import Mesh
from compas.utilities import flatten
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolylineArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin_reactions.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')
mesh = Mesh.from_json(FILE_I)


proxy = Proxy('compas.geometry')
bestfit = proxy.bestfit_frame_numpy

# start = (1343, 1344)
start = (638, 842)

bdr_beam_dis = 0.1  # offset distance, beam height
beam_height = 0.1

# find the edge loop
loop = mesh.edge_loop(start)
loop_vertices = list(flatten(loop))  # not chained
seen = set()
loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]

points = []

# move the points along the reaction force direction to generate the beams
for vkey in loop_vertices:
    rx, ry, rz = mesh.vertex_attributes(vkey, ('rx', 'ry', 'rz'))
    react_dir = scale_vector(normalize_vector([rx, ry, rz]), -bdr_beam_dis)
    xyz = mesh.vertex_coordinates(vkey)
    beam_pt = add_vectors(xyz, react_dir)
    points.append(beam_pt)

polyline = Polyline(points)
local_frame = bestfit(polyline)

xaxis_local = local_frame[1]
yaxis_local = local_frame[2]
zaxis_local = normalize_vector(cross_vectors(xaxis_local, yaxis_local))

# check polyline direction
polyline_vec = subtract_vectors(points[-1], points[0])
cross_vec = cross_vectors(polyline_vec, zaxis_local)
if dot_vectors(cross_vec, [0, 0, 1]) < 0:
    zaxis_local = scale_vector(zaxis_local, -1)
print(zaxis_local)

polyline_o = Polyline(offset_polyline(polyline, -beam_height, zaxis_local))

world = Frame.worldXY()
T = Transformation.from_frame_to_frame(Frame(*local_frame), world)

polyline_i_T = polyline.transformed(T)
polyline_o_T = polyline_o.transformed(T)

# # if the polyline is not in xy plane, run the following 
# points = polyline_T.points
# print(points)
# xy_points = project_points_plane(points, ([0, 0, 0], [0, 0, 1]))
# polyline_T = Polyline(xy_points)

polyartist = PolylineArtist(polyline_i_T, layer="DF2021:: Beam")
polyartist.clear_layer()
polyartist.draw(show_points=True)

polyartist2 = PolylineArtist(polyline_o_T, layer="DF2021:: Beam")
polyartist2.draw(show_points=True)

edgecolor = {}
for (u, v) in loop:
    edgecolor[(u, v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)
# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})),join_faces=True)
artist.draw_edges(color=edgecolor)
#artist.draw_vertexlabels()
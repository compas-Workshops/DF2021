# ==============================================================================
# Import
# ==============================================================================
import os

from compas.geometry import Polygon, Polyline, Frame, Transformation
from compas.geometry import offset_polyline, project_points_plane
from compas.geometry import normalize_vector, cross_vectors
from compas.geometry import subtract_vectors, dot_vectors

from compas.datastructures import Mesh
from compas.utilities import flatten
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolygonArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch_reactions.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)

proxy = Proxy('compas.geometry')
bestfit = proxy.bestfit_frame_numpy

start = list(mesh.edges_where({'seam': True}))[0]

# find the edge loop
loop = mesh.edge_loop(start)
loop_vertices = list(flatten(loop)) 
seen = set()
loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]

points = mesh.vertices_attribute('beam_pt', keys=loop_vertices)
polyline = Polyline(points)

local_frame = bestfit(polyline)
xaxis_local = local_frame[1]
yaxis_local = local_frame[2]
zaxis_local = normalize_vector(cross_vectors(xaxis_local, yaxis_local))

# check polyline direction
polyline_vec = subtract_vectors(points[-1], points[0])
cross_vec = cross_vectors(polyline_vec, zaxis_local)
if dot_vectors(cross_vec, [0, 0, 1]) < 0:
    # zaxis_local = scale_vector(zaxis_local, -1)
    polyline = Polyline(points[::-1])

world = Frame.worldXY()
T_local_xy = Transformation.from_frame_to_frame(Frame(*local_frame), world)

beam_height = 0.15
polyline_T = polyline.transformed(T_local_xy)
points = polyline_T.points
xy_points = project_points_plane(points, ([0, 0, 0], [0, 0, 1]))
polyline_i_T = Polyline(xy_points)
polyline_o_T = Polyline(offset_polyline(polyline_i_T, -beam_height, [0, 0, 1]))

# join two polylines
points_T = polyline_i_T.points + polyline_o_T.points[::-1]
polygon_T = Polygon(points_T)
polygonartist = PolygonArtist(polygon_T, layer="DF21_D3::Beam::Seam::XY")
polygonartist.clear_layer()
polygonartist.draw(show_points=False, show_edges=True, show_face=False)

T_xy_local = Transformation.from_frame_to_frame(world, Frame(*local_frame))
polyline = polyline_i_T.transformed(T_xy_local)
polyline_o = polyline_o_T.transformed(T_xy_local)
points = polyline.points + polyline_o.points[::-1]
polygon = Polygon(points)
polygonartist = PolygonArtist(polygon, layer="DF21_D3::Beam::Seam::local")
polygonartist.clear_layer()
polygonartist.draw(show_points=False, show_edges=True, show_face=False)

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u, v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF21_D3::KnitPatch")
artist.clear_layer()
# artist.draw()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})), join_faces=True)
artist.draw_edges(color=edgecolor)
# artist.draw_vertexlabels()

# ==============================================================================
# Import
# ==============================================================================
import os

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
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch_reactions.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)

proxy = Proxy('compas.geometry')
bestfit = proxy.bestfit_frame_numpy

start = list(mesh.edges_where({'seam': True}))[0]
# print(start)

# find the edge loop
loop = mesh.edge_loop(start)
loop_vertices = list(flatten(loop)) 
seen = set()
loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]

points = mesh.vertices_attribute('beam_pt', keys=loop_vertices)
polyline = Polyline(points)

local_frame = bestfit(polyline)
world = Frame.worldXY()
T_local_xy = Transformation.from_frame_to_frame(Frame(*local_frame), world)

polyline_T = polyline.transformed(T_local_xy)

# if the polyline is not in xy plane, run the following
points = polyline_T.points
xy_points = project_points_plane(points, ([0, 0, 0], [0, 0, 1]))
polyline_T = Polyline(xy_points)

# transform the curve projected to xy plane back to the local frame
T_xy_local = Transformation.from_frame_to_frame(world, Frame(*local_frame))
polyline = polyline_T.transformed(T_xy_local)

polyartist = PolylineArtist(polyline, layer="DF21_D3::Beam::Seam::local")
polyartist.clear_layer()
polyartist.draw(show_points=True)

polyartist = PolylineArtist(polyline_T, layer="DF21_D3::Beam::Seam::XY")
polyartist.clear_layer()
polyartist.draw(show_points=True)

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u,v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF21_D3::KnitPatch")
artist.clear_layer()
# artist.draw()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})), join_faces=True)
artist.draw_edges(color=edgecolor)
# artist.draw_vertexlabels()

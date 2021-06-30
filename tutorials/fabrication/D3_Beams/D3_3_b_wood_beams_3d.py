# ==============================================================================
# Import
# ==============================================================================
import os

from compas.geometry import Polygon, Polyline, Frame, Transformation
from compas.geometry import offset_polyline, project_points_plane
from compas.geometry import normalize_vector, scale_vector, cross_vectors
from compas.geometry import subtract_vectors, dot_vectors, add_vectors

from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.utilities import flatten, pairwise
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablemesh_fofin_patch_reactions.json')
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

T_xy_local = Transformation.from_frame_to_frame(world, Frame(*local_frame))
polyline = polyline_i_T.transformed(T_xy_local)
polyline_o = polyline_o_T.transformed(T_xy_local)

# generate 2d mesh
vertices_T = polyline_i_T.points + polyline_o_T.points
faces = []
length = len(polyline.points)
for i in range(length - 1):
    faces.append([i, i + 1, length + i + 1, length + i])
beam_2d_T = Mesh.from_vertices_and_faces(vertices_T, faces)

meshartist = MeshArtist(beam_2d_T, layer="DF2021:: Beam:: Seam:: local_mesh")
meshartist.clear_layer()
meshartist.draw_faces(join_faces=True)
meshartist.draw_edges()

vertices = polyline.points + polyline_o.points
beam_2d = Mesh.from_vertices_and_faces(vertices, faces)

# ==============================================================================
# Generate 3D beams
# ==============================================================================
# copy the mesh
beam_side1 = beam_2d.copy()
beam_side2 = beam_2d.copy()

thickness = 0.05

for vkey in beam_2d.vertices():
    xyz = beam_2d.vertex_coordinates(vkey)

    left = scale_vector(zaxis_local, -0.5 * thickness)
    right = scale_vector(zaxis_local, 0.5 * thickness)

    beam_side1.vertex_attributes(vkey, 'xyz', add_vectors(xyz, left))
    beam_side2.vertex_attributes(vkey, 'xyz', add_vectors(xyz, right))

mesh_flip_cycles(beam_side2)

beam_3d = beam_side1.copy()
max_int_key = len(list(beam_3d.vertices()))
max_int_fkey = len(list(beam_3d.faces()))

for key, attr in beam_side2.vertices(True):
    beam_3d.add_vertex(key=key + max_int_key, **attr)

for fkey in beam_side2.faces():
    vertices = beam_side2.face_vertices(fkey)
    vertices = [key + max_int_key for key in vertices]
    beam_3d.add_face(vertices)

boundary = beam_side2.vertices_on_boundary()
boundary.append(boundary[0])

for a, b in pairwise(boundary):
    beam_3d.add_face([b, a, a + max_int_key, b + max_int_key])

meshartist = MeshArtist(beam_3d, layer="DF2021:: Beam:: Seam:: local_mesh")
#meshartist.clear_layer()
meshartist.draw_faces(join_faces=True)
meshartist.draw_edges()

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u, v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
#artist.draw()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})),join_faces=True)
artist.draw_edges(color=edgecolor)
#artist.draw_vertexlabels()
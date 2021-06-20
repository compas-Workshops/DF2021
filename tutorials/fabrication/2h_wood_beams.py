# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.geometry import Polygon, Polyline
from compas.geometry import offset_polyline
from compas.geometry import cross_vectors, dot_vectors
from compas.geometry import normalize_vector, scale_vector
from compas.geometry import add_vectors, subtract_vectors
from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.utilities import flatten
from compas.utilities import pairwise
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolygonArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin_add_patch.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)


proxy = Proxy('compas.geometry')
bestfit = proxy.bestfit_frame_numpy

for start in [(1343, 1344), (948, 576), (1422, 1423)]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    loop_vertices = list(flatten(loop)) # not chained
    seen = set()
    loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]
    points = mesh.vertices_attributes('xyz', keys=loop_vertices)
    polyline = Polyline(points)
    origin_local, xaxis_local, yaxis_local = bestfit(polyline)
    zaxis_local = normalize_vector(cross_vectors(xaxis_local, yaxis_local))

    # check polyline direction
    polyline_vec = subtract_vectors(points[-1], points[0])
    cross_vec = cross_vectors(polyline_vec, zaxis_local)
    if dot_vectors(cross_vec, [0, 0, 1]) <0:
        zaxis_local = scale_vector(zaxis_local, -1)
    print(zaxis_local)
    
    gap = 0.1  # gap for hooks
    dis = 0.1 # offset distance
    polyline_i = Polyline(offset_polyline(polyline, -gap, zaxis_local))
    polyline_o = Polyline(offset_polyline(polyline_i, -dis, zaxis_local))

    # generate 2d mesh
    vertices = polyline_i.points + polyline_o.points 
    faces = []
    length = len(polyline_i.points)
    for i in range(length - 1) :
        faces.append([i, i + 1, length + i + 1, length + i])
    beam_2d = Mesh.from_vertices_and_faces(vertices, faces)

    # copy
    beam_side1 = beam_2d.copy()
    beam_side2 = beam_2d.copy()

    thickness = 0.05

    for vkey in beam_2d.vertices():
        xyz = beam_2d.vertex_coordinates(vkey)

        up = scale_vector(zaxis_local, 0.5 * thickness)
        down = scale_vector(zaxis_local, -0.5 * thickness)

        beam_side1.vertex_attributes(vkey, 'xyz', add_vectors(xyz, up))
        beam_side2.vertex_attributes(vkey, 'xyz', add_vectors(xyz, down))

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

    beamartist = MeshArtist(beam_3d, layer="DF2021:: Beam")
    # beamartist.clear_layer()
    beamartist.draw_faces(join_faces=True)
    beamartist.draw_edges()

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u,v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)
    
artist = MeshArtist(mesh, layer="DF2021:: Base")
artist.clear_layer()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})),join_faces=True)
artist.draw_edges(color=edgecolor)
#artist.draw_vertexlabels()
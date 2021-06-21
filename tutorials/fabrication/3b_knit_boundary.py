# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.datastructures import Mesh
from compas.geometry import Point
from compas.geometry import normalize_vector, scale_vector, add_vectors
from compas.utilities import flatten

from compas_rhino.artists import MeshArtist, PointArtist
from compas_rhino.artists import PolylineArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin_reactions.json')
# FILE_O = os.path.join(HERE, 'bridge_fofin_add_patch.json')

mesh = Mesh.from_json(FILE_I)

bdr_points_dict = {} # dictonary saves: key, original point; item, new point
bdr_patch_dis = 0.05

mesh.update_default_face_attributes({'is_knit': True})

bdr_faces = []

for start in [(638, 842),  (948, 576), (1332, 493)]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    bdr_faces = []
    for (u, v) in loop:
        if u not in bdr_points_dict.keys():
            rx, ry, rz = mesh.vertex_attributes(u, ('rx', 'ry', 'rz'))
            react_dir = scale_vector(normalize_vector([rx, ry, rz]), -bdr_patch_dis)

            xyz = mesh.vertex_coordinates(u)
            new_key = mesh.add_vertex()
            mesh.vertex_attributes(new_key, 'xyz', add_vectors(xyz, react_dir))
            bdr_points_dict[u] = new_key
        if v not in bdr_points_dict.keys():
            rx, ry, rz = mesh.vertex_attributes(v, ('rx', 'ry', 'rz'))
            react_dir = scale_vector(normalize_vector([rx, ry, rz]), -bdr_patch_dis)

            xyz = mesh.vertex_coordinates(v)
            new_key = mesh.add_vertex()
            mesh.vertex_attributes(new_key, 'xyz', add_vectors(xyz, react_dir))
            bdr_points_dict[v] = new_key
        fkey = mesh.add_face([u, v, bdr_points_dict[v], bdr_points_dict[u]], attr_dict={'is_knit': False})
        bdr_faces.append(fkey)
    

    print(len(bdr_faces))
    for fkey in bdr_faces:
        face_center = Point(*mesh.face_centroid(fkey))
        point_artist = PointArtist(face_center, color=(255,0,0), layer="DF2021:: Bdr_holes")
        point_artist.draw()

# mesh.to_json(FILE_O)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})),join_faces=True)
artist.draw_edges()
# artist.draw_vertices()
#artist.draw_vertexlabels()
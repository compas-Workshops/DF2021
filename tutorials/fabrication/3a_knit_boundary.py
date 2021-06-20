# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.datastructures import Mesh
from compas.geometry import normalize_vector, scale_vector, add_vectors
from compas.utilities import flatten

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolylineArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin.json')
# FILE_O = os.path.join(HERE, 'bridge_fofin_hook.json')

mesh = Mesh.from_json(FILE_I)

bdr_points_dict = {} # dictonary saves: key, original point; item, new point
bdr_patch_dis = 0.05

for start in [(638, 842), (1332, 493)]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    for (u, v) in loop:
        if u not in bdr_points_dict.keys():
            vkey_normal = mesh.vertex_normal(u)
            vkey_normal = scale_vector(normalize_vector(vkey_normal), bdr_patch_dis)

            xyz = mesh.vertex_coordinates(u)
            new_key = mesh.add_vertex()
            mesh.vertex_attributes(new_key, 'xyz', add_vectors(xyz, vkey_normal))
            bdr_points_dict[u] = new_key
        if v not in bdr_points_dict.keys():
            vkey_normal = mesh.vertex_normal(v)
            vkey_normal = scale_vector(normalize_vector(vkey_normal), bdr_patch_dis)

            xyz = mesh.vertex_coordinates(v)
            new_key = mesh.add_vertex()
            mesh.vertex_attributes(new_key, 'xyz', add_vectors(xyz, vkey_normal))
            bdr_points_dict[v] = new_key
        mesh.add_face([u, v, bdr_points_dict[v], bdr_points_dict[u]])


# mesh.to_json(FILE_O)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges()
# artist.draw_vertices()
#artist.draw_vertexlabels()
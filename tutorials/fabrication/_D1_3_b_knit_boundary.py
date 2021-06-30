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
FILE_I = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch1.json')
FILE_O = os.path.join(HERE, '..', 'data', 'knit_patch1_feature.json')

mesh = Mesh.from_json(FILE_I)

bdr_points_dict = {} # dictonary saves: key, original point; item, new point
bdr_patch_dis = 0.05

mesh.update_default_face_attributes({'bdr_featrue': True})

vkey = mesh.get_any_vertex()
nbr1 = mesh.vertex_neighbors(vkey)[0]
nbr2 = mesh.vertex_neighbors(vkey)[1]
loop1 = mesh.edge_loop((vkey, nbr1))
loop2 = mesh.edge_loop((vkey, nbr2))

if len(loop1) > len(loop2):
    strips = mesh.edge_strip((vkey, nbr1))
else:
    strips = mesh.edge_strip((vkey, nbr2))

for start in [strips[0], strips[-1]]:
    # find the edge loop
    loop = mesh.edge_loop(start)
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
        fkey = mesh.add_face([u, v, bdr_points_dict[v], bdr_points_dict[u]], attr_dict={'bdr_featrue': False})

mesh.to_json(FILE_O)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch1:: Knit")
artist.clear_layer()
artist.draw_faces(faces=list(mesh.faces_where({'bdr_featrue': True})),join_faces=True)
artist.draw_edges()
# artist.draw_vertices()
#artist.draw_vertexlabels()
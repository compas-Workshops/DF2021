# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.datastructures import Mesh
from compas.geometry import Point, Line
from compas.geometry import normalize_vector, scale_vector, add_vectors
from compas.utilities import flatten

from compas_rhino.artists import MeshArtist, PointArtist, LineArtist
from compas_rhino.artists import PolylineArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch1.json')
FILE_O = os.path.join(HERE, '..', 'data', 'knit_patch1_feature.json')

mesh = Mesh.from_json(FILE_I)

bdr_points_dict = {}  # dictonary saves: key, original point; item, new point on
bdr_beam_dict = {}
bdr_patch_dis = 0.05
bdr_beam_dis = 0.1

mesh.update_default_face_attributes({'bdr_featrue': True, 'hook': False})

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
    bdr_faces = []
    beam_edges = []

    for (u, v) in loop:
        if u not in bdr_points_dict.keys():
            if mesh.vertex_degree(u) == 2:
                rx, ry, rz = mesh.vertex_attributes(v, ('rx', 'ry', 'rz'))
            else:
                rx, ry, rz = mesh.vertex_attributes(u, ('rx', 'ry', 'rz'))
            react_vec = normalize_vector([rx, ry, rz])
            patch_dir = scale_vector(react_vec, -bdr_patch_dis)

            xyz = mesh.vertex_coordinates(v)
            new_key = mesh.add_vertex()
            mesh.vertex_attributes(new_key, 'xyz', add_vectors(xyz, patch_dir))
            bdr_points_dict[u] = new_key
            bdr_beam_dict[u] = add_vectors(xyz, scale_vector(react_vec, -bdr_beam_dis))

        if v not in bdr_points_dict.keys():
            if mesh.vertex_degree(v) == 2:
                rx, ry, rz = mesh.vertex_attributes(u, ('rx', 'ry', 'rz'))
            else:
                rx, ry, rz = mesh.vertex_attributes(v, ('rx', 'ry', 'rz'))
            react_vec = normalize_vector([rx, ry, rz])
            patch_dir = scale_vector(react_vec, -bdr_patch_dis)

            xyz = mesh.vertex_coordinates(v)
            new_key = mesh.add_vertex()
            mesh.vertex_attributes(new_key, 'xyz', add_vectors(xyz, patch_dir))
            bdr_points_dict[v] = new_key
            bdr_beam_dict[v] = add_vectors(xyz, scale_vector(react_vec, -bdr_beam_dis))
        
        fkey = mesh.add_face([u, v, bdr_points_dict[v], bdr_points_dict[u]], attr_dict={'bdr_featrue': False})
        bdr_faces.append(fkey)
        beam_edges.append([bdr_beam_dict[u], bdr_beam_dict[v]])

    print(len(bdr_faces))
    for i, fkey in enumerate(bdr_faces):
        if i == 0 or i == len(bdr_faces) - 1 or i % 4 == 2:
            mesh.face_attribute(fkey, 'hook', True)
            face_center = Point(*mesh.face_centroid(fkey))
            point_artist = PointArtist(face_center, color=(255, 0, 0), layer="DF2021:: Bdr_holes")
            point_artist.draw()

            beam_pt = [sum(x) / len(x) for x in zip(*beam_edges[i])]
            beam_pt = Point(*beam_pt)
            point_artist = PointArtist(beam_pt, color=(0, 255, 0), layer="DF2021:: Beam_hooks")
            point_artist.draw()
            
            line = Line(face_center, beam_pt)
            line_artist = LineArtist(line)
            line_artist.draw()

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
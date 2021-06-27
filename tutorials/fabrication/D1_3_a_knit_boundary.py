# ==============================================================================
# Import
# ==============================================================================
import os
import random
import compas_rhino

from compas.datastructures import Mesh
from compas.geometry import subtract_vectors, normalize_vector

from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch1.json')

mesh = Mesh.from_json(FILE_I)

vkey = mesh.get_any_vertex()
nbr1 = mesh.vertex_neighbors(vkey)[0]
nbr2 = mesh.vertex_neighbors(vkey)[1]
loop1 = mesh.edge_loop((vkey, nbr1))
loop2 = mesh.edge_loop((vkey, nbr2))

if len(loop1) > len(loop2):
    strips = mesh.edge_strip((vkey, nbr1))
else:
    strips = mesh.edge_strip((vkey, nbr2))

lines = []
seen = []
for start in [strips[0], strips[-1]]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    for (u, v) in loop:
        if u not in seen:
            rx, ry, rz = mesh.vertex_attributes(u, ('rx', 'ry', 'rz'))
            residual = normalize_vector([rx, ry, rz])
            xyz = mesh.vertex_coordinates(u)
            lines.append(
            {'start': xyz,
            'end': subtract_vectors(xyz, residual),
            'arrow': 'end',
            'color': (0, 255, 0)}) 
            seen.append(u)

        if v not in seen:
            rx, ry, rz = mesh.vertex_attributes(v, ('rx', 'ry', 'rz'))
            residual = normalize_vector([rx, ry, rz])
            xyz = mesh.vertex_coordinates(v)
            lines.append(
            {'start': xyz,
            'end': subtract_vectors(xyz, residual),
            'arrow': 'end',
            'color': (0, 255, 0)})
            seen.append(v)


# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch1:: Knit")
artist.clear_layer()
artist.draw_faces(faces=list(mesh.faces_where({'bdr_featrue': True})),join_faces=True)
artist.draw_edges()
# artist.draw_vertices()
#artist.draw_vertexlabels()

compas_rhino.draw_lines(lines, layer="DF2021:: KnitPatch1:: Reactions")
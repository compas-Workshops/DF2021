# ==============================================================================
# Import
# ==============================================================================

import os

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch1.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Process
# ==============================================================================

corner = list(mesh.vertices_where({'vertex_degree': 2}))[0]
nbrs = mesh.vertex_neighbors(corner)

loop1 = mesh.edge_loop((corner, nbrs[0]))
loop2 = mesh.edge_loop((corner, nbrs[1]))

if len(loop1) > len(loop2):
    start = loop1[0]
else:
    start = loop2[0]

strip = mesh.edge_strip(start)

boundary1 = mesh.edge_loop(strip[0])
boundary2 = mesh.edge_loop(strip[-1])

# ==============================================================================
# Visualization
# ==============================================================================

edgecolor = {}
for u, v in boundary1:
    edgecolor[(u, v)] = edgecolor[(v, u)] = (0, 255, 0)
for u, v in boundary2:
    edgecolor[(u, v)] = edgecolor[(v, u)] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF21_D2::KnitPatch")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges(color=edgecolor)

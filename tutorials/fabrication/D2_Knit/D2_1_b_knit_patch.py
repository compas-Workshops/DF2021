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
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_refined.json')
mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Select faces
# ==============================================================================

vertex = 67
nbrs = mesh.vertex_neighbors(vertex)

if not mesh.is_vertex_on_boundary(vertex):
    raise Exception('The starting vertex should be on boundary.')

nbr = None
for temp in nbrs:
    if not mesh.is_vertex_on_boundary(temp):
        nbr = temp
        break

if not nbr:
    raise Exception('This is not possible.')

edges = mesh.edge_loop((vertex, nbr))

left = []
right = []

for u, v in edges:
    left += [mesh.halfedge_face(*edge) for edge in mesh.halfedge_strip((u, v))][:-1]
    right += [mesh.halfedge_face(*edge) for edge in mesh.halfedge_strip((v, u))][:-1]

# ==============================================================================
# Visualization
# ==============================================================================

facecolor = {}
for face in left:
    facecolor[face] = (255, 200, 200)

for face in right:
    facecolor[face] = (200, 255, 200)

artist = MeshArtist(mesh, layer="DF21_D2::KnitPatch")
artist.clear_layer()
artist.draw_faces(color=facecolor)
# artist.draw_edges()
# artist.draw_vertexlabels()

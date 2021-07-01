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
# Set strip faces
# ==============================================================================

loop = mesh.edge_loop((67, 510))

left = [mesh.halfedge_face(*edge) for edge in mesh.halfedge_strip((67, 510))][:-1]
right = [mesh.halfedge_face(*edge) for edge in mesh.halfedge_strip((510, 67))][:-1]

# ==============================================================================
# Visualization
# ==============================================================================

edgecolor = {}
for (u, v) in loop:
    edgecolor[(u, v)] = edgecolor[(v, u)] = (0, 255, 255)

edgecolor[(67, 510)] = (0, 0, 255)

facecolor = {}
for face in left:
    facecolor[face] = (255, 0, 0)
for face in right:
    facecolor[face] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF21_D2::KnitPatch")
artist.clear_layer()
artist.draw_faces(color=facecolor)
artist.draw_edges(color=edgecolor)
artist.draw_vertexlabels()

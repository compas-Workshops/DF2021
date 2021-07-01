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

edges = mesh.edge_loop((67, 510))

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

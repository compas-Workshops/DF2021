# ==============================================================================
# Import
# ==============================================================================

import os

from compas.geometry import Point
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist, PointArtist

# ==============================================================================
# Initialise
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch2.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF21_D2::KnitPatch2")
artist.clear_layer()
artist.draw_faces(color={fkey: (200, 255, 200) for fkey in mesh.faces()})
artist.draw_edges()

for u, v in mesh.edges_where({'hook': True}):
    point = Point(*mesh.edge_midpoint(u, v))
    artist = PointArtist(point, color=(0, 255, 0), layer="DF21_D2::KnitPatch2::Hooks")
    artist.draw()

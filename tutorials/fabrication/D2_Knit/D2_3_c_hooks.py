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
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch1.json')

mesh = Mesh.from_json(FILE_I)

for (u, v) in mesh.edges():
    if mesh.edge_attribute((u, v), 'hook') is True:
        point = Point(*mesh.edge_midpoint(u, v))
        point_artist = PointArtist(point, color=(0, 255, 0),
                       layer="DF21_D2::KnitPatch::Hooks")
        point_artist.draw()

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF21_D2::KnitPatch1")
artist.clear_layer()
artist.draw_faces(color={fkey: (255, 200, 200) for fkey in mesh.faces()})
artist.draw_edges()

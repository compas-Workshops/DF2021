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
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch.json')

mesh = Mesh.from_json(FILE_I)
seam = mesh.edge_loop((67, 510))
bdr_1 = mesh.edge_loop((16, 338))
bdr_2 = mesh.edge_loop((30, 383))
mesh.update_default_edge_attributes({'seam': False, 'bdr': None})
for edge in seam:
    mesh.edge_attribute(edge, 'seam', True)
for edge in bdr_1:
    mesh.edge_attribute(edge, 'bdr', 1)
for edge in bdr_2:
    mesh.edge_attribute(edge, 'bdr', 2)

mesh.to_json(FILE_I)

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in seam:
    edgecolor[(u, v)] = (255, 0, 0)
    edgecolor[(v, u)] = (255, 0, 0)
for (u, v) in bdr_1 + bdr_2:
    edgecolor[(u, v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)
    
facecolor = {}
for face in mesh.faces_where({'patch': 1}):
    facecolor[face] = (255, 200, 200)

for face in mesh.faces_where({'patch': 2}):
    facecolor[face] = (200, 255, 200)

artist = MeshArtist(mesh, layer="DF21_D2::KnitPatch")
artist.clear_layer()
artist.draw_faces(color=facecolor)
artist.draw_edges(color=edgecolor)
# artist.draw_vertexlabels()
artist.draw_facelabels(color=facecolor)

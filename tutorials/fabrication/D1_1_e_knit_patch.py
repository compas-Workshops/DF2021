# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.utilities import flatten, pairwise
from compas.topology import shortest_path
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch.json')

mesh = Mesh.from_json(FILE_I)
seam = mesh.edge_loop((67, 510))
mesh.update_default_edge_attributes({'seam': False})
for edge in seam:
    mesh.edge_attribute(edge, 'seam', True)

mesh.to_json(FILE_I)
# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in seam:
    edgecolor[(u, v)] = (255, 0, 0)
    edgecolor[(v, u)] = (255, 0, 0)

facecolor = {}
for face in mesh.faces_where({'patch': 1}):
    facecolor[face] = (255, 200, 200)

for face in mesh.faces_where({'patch': 2}):
    facecolor[face] = (200, 255, 200)

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(color=facecolor)
artist.draw_edges(color=edgecolor)
#artist.draw_vertexlabels()
#artist.draw_facelabels(color=facecolor)
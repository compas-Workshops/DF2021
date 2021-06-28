# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.utilities import flatten
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablemesh_fofin_refined.json')

mesh = Mesh.from_json(FILE_I)
#
# ==============================================================================
# Select faces
# ==============================================================================
start = (30, 382)
loop = mesh.edge_loop(start)
print(loop)
strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
strip[:] = list(set(flatten(strip)))

# ==============================================================================
# Visualization
# ==============================================================================

edgecolor = {}
for (u, v) in loop:
    edgecolor[(u,v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

edgecolor[start] = (255, 0, 0)

facecolor = {}
for face in strip:
    facecolor[face] = (255, 0, 0)

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
#artist.draw()
artist.draw_faces(color=facecolor)
artist.draw_edges(color=edgecolor)
artist.draw_vertexlabels()
# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.datastructures import Mesh
from compas.utilities import geometric_key
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)

# TODO: load edge cable 


# ==============================================================================
# Visualization
# ==============================================================================
facecolor = {}
for face in mesh.faces_where({'patch':1}):
    facecolor[face] = (255, 200, 200)
for face in mesh.faces_where({'patch':2}):
     facecolor[face] = (200, 255, 200)

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(color=facecolor)
artist.draw_edges()
artist.draw_facelabels(color=facecolor)
#artist.draw_vertexlabels()
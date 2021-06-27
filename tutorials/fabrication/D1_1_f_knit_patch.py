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
FILE_01 = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch1.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Patch1
# ==============================================================================
mesh_1 = mesh.copy()
mesh_1.name = "patch_1"
for fkey in mesh.faces_where({'patch': 2}):
    mesh_1.delete_face(fkey)
mesh_1.remove_unused_vertices()

mesh_1.to_json(FILE_01)

# ==============================================================================
# Visualization
# ==============================================================================
artist1 = MeshArtist(mesh_1, layer="DF2021:: KnitPatch1:: Knit")
artist1.clear_layer()
artist1.draw_faces(color={fkey:(255, 200, 200) for fkey in mesh.faces()})
artist1.draw_edges()
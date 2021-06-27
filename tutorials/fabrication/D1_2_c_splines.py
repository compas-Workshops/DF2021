# ==============================================================================
# Import
# ==============================================================================
import os
import random

import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I1 = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch1.json')
FILE_I2 = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch1.json')

mesh_1 = Mesh.from_json(FILE_I1)
mesh_2 = Mesh.from_json(FILE_I2)

length = 0

for (u, v) in mesh_1.edges():
    if mesh_1.vertex_attribute(u, 'is_anchor') is True and mesh_1.vertex_attribute(v, 'is_anchor') is True:
        length += mesh_1.edge_length(u, v)

for (u, v) in mesh_2.edges():
    if mesh_2.vertex_attribute(u, 'is_anchor') is True and mesh_2.vertex_attribute(v, 'is_anchor') is True:
        length += mesh_2.edge_length(u, v)

print(round(length, 1))
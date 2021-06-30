# ==============================================================================
# Import
# ==============================================================================

import os
import math as m

from compas.datastructures import Mesh

# ==============================================================================
# Initialise
# ==============================================================================

HERE = os.path.dirname(__file__)
FILE_I1 = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch1.json')
FILE_I2 = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch2.json')

mesh_1 = Mesh.from_json(FILE_I1)
mesh_2 = Mesh.from_json(FILE_I2)

# ==============================================================================
# Calculate the length and weight of Splines / Rebars
# ==============================================================================

# initialize the total length and weight
total_length = 0
total_weight = 0
weight = 7850  # kg/m3
section = 0.008**2 * m.pi

# loop through the edges to calculate edge length and weight
for u, v in mesh_1.edges_where({'is_spline': True}):
    edge_len = mesh_1.edge_length(u, v)
    total_length += edge_len
    total_weight += edge_len * weight * section

for u, v in mesh_2.edges_where({'is_spline': True}):
    edge_len = mesh_2.edge_length(u, v)
    total_length += edge_len
    total_weight += edge_len * weight * section

print("Total length of the splines is: %s m." % round(total_length, 2))
print("Total weight of the splines is: %s kg." % int(total_weight))

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
FILE_01 = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch1.json')
FILE_02 = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch2.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Patches
# ==============================================================================
mesh_1 = mesh.copy()
mesh_2 = mesh.copy()
mesh_1.name = "patch_1"
mesh_2.name = "patch_2"

for fkey in mesh.faces_where({'patch': 2}):
    mesh_1.delete_face(fkey)
mesh_1.remove_unused_vertices()

for fkey in mesh.faces_where({'patch': 1}):
    mesh_2.delete_face(fkey)
mesh_2.remove_unused_vertices()

modified_vkeys = []
seam_dis = 0.008

for (u, v) in mesh_1.edges_where({'seam': True}):
    print(u)
    if u not in modified_vkeys:
        u_x = mesh_1.vertex_attribute(u, 'x')
        mesh_1.vertex_attribute(u, 'x', u_x - seam_dis)
        modified_vkeys.append(u)
    if v not in modified_vkeys:
        v_x = mesh_1.vertex_attribute(v, 'x')
        mesh_1.vertex_attribute(v, 'x', v_x - seam_dis)
        modified_vkeys.append(v)

modified_vkeys = []
for (u, v) in mesh_2.edges_where({'seam': True}):
    print(u)
    if u not in modified_vkeys:
        u_x = mesh_2.vertex_attribute(u, 'x')
        mesh_2.vertex_attribute(u, 'x', u_x + seam_dis)
        modified_vkeys.append(u)
    if v not in modified_vkeys:
        v_x = mesh_2.vertex_attribute(v, 'x')
        mesh_2.vertex_attribute(v, 'x', v_x + seam_dis)
        modified_vkeys.append(v)

mesh_1.to_json(FILE_01)
mesh_2.to_json(FILE_02)

# ==============================================================================
# Visualization
# ==============================================================================
artist1 = MeshArtist(mesh_1, layer="DF2021_D1::KnitPatch1")
artist1.clear_layer()
artist1.draw_faces(color={fkey: (255, 200, 200) for fkey in mesh.faces()})
artist1.draw_edges()

artist2 = MeshArtist(mesh_2, layer="DF2021_D1::KnitPatch2")
artist2.clear_layer()
artist2.draw_faces(color={fkey: (200, 255, 200) for fkey in mesh.faces()})
artist2.draw_edges()

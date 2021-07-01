# ==============================================================================
# Import
# ==============================================================================
import os

from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.geometry import add_vectors
from compas.utilities import pairwise

from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin_reactions.json')
# FILE_O = os.path.join(HERE, 'bridge_fofin_add_patch.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Exercise... very similar to the beam...
# ==============================================================================

mesh_up = mesh.copy()
thickness = 0.05

for vkey in mesh.vertices():
    xyz = mesh.vertex_coordinates(vkey)
    v_normal = mesh.vertex_normal(vkey)

    up = scale_vector(v_normal, thickness)

    mesh_up.vertex_attributes(vkey, 'xyz', add_vectors(xyz, up))

mesh_flip_cycles(mesh)

concrete = mesh.copy()
max_int_key = len(list(mesh.vertices()))
max_int_fkey = len(list(mesh.faces()))

for key, attr in mesh_up.vertices(True):
    concrete.add_vertex(key=key + max_int_key, **attr)

for fkey in mesh_up.faces():
    vertices = mesh_up.face_vertices(fkey)
    vertices = [key + max_int_key for key in vertices]
    concrete.add_face(vertices)

boundary = mesh_up.vertices_on_boundary()
boundary.append(boundary[0])

for a, b in pairwise(boundary):
    concrete.add_face([b, a, a + max_int_key, b + max_int_key])

# ==============================================================================
# Visualization
# ==============================================================================
artist = MeshArtist(concrete, layer="DF2021:: Concrete")
# artist.clear_layer()
artist.draw_faces(join_faces=True)
#artist.draw_edges()

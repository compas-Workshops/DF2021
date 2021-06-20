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
FILE_I = os.path.join(HERE, 'corrugation_fofin.json')
FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Select faces
# ==============================================================================
start = 1332
mid = 948
end = 638

vertices_1 = shortest_path(mesh.adjacency, start, mid)
vertices_2 = shortest_path(mesh.adjacency, mid, end)

edges_1 = pairwise(vertices_1)
edges_2 = pairwise(vertices_2)
patch_1 = []
patch_2 = []

for start in edges_1:
    strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
    strip[:] = list(set(flatten(strip)))
    patch_1.extend(strip)

for start in edges_2:
    strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
    strip[:] = list(set(flatten(strip)))
    patch_2.extend(strip)

# ==============================================================================
# Set face attributes
# ==============================================================================
mesh._default_face_attributes({'patch': None})
for face in patch_1:
    if face:
        mesh.face_attribute(face, 'patch', 1)
for face in patch_2:
    if face:
        mesh.face_attribute(face, 'patch', 2)

print(list(mesh.faces_where({'patch':1})))
print(list(mesh.faces_where({'patch':2})))


mesh.to_json(FILE_0)

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in edges_1:
    edgecolor[(u, v)] = (255, 0, 0)
    edgecolor[(v, u)] = (255, 0, 0)

for (u, v) in edges_2:
    edgecolor[(u, v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

facecolor = {}
for face in patch_1:
    facecolor[face] = (255, 200, 200)

for face in patch_2:
    facecolor[face] = (200, 255, 200)

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(color=facecolor)
artist.draw_edges(color=edgecolor)
artist.draw_facelabels(color=facecolor)
#artist.draw_vertexlabels()
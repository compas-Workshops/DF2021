# ==============================================================================
# Import
# ==============================================================================
import os
import compas_rhino

from compas.geometry import Point
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist, PointArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch1.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Process
# ==============================================================================

corner = list(mesh.vertices_where({'vertex_degree': 2}))[0]
nbrs = mesh.vertex_neighbors(corner)

loop1 = mesh.edge_loop((corner, nbrs[0]))
loop2 = mesh.edge_loop((corner, nbrs[1]))

if len(loop1) > len(loop2):
    start = loop1[0]
else:
    start = loop2[0]

strip = mesh.edge_strip(start)

boundary1 = mesh.edge_loop(strip[0])
boundary2 = mesh.edge_loop(strip[-1])

mesh.update_default_edge_attributes({'hook': False})

for i, edge in enumerate(boundary1):
    if i % 4 == 1 or i == 0 or i == len(boundary1) - 1:
        mesh.edge_attribute(edge, 'hook', True)

for i, edge in enumerate(boundary2):
    if i % 4 == 1 or i == 0 or i == len(boundary2) - 1:
        mesh.edge_attribute(edge, 'hook', True)

mesh.to_json(FILE_I)

# ==============================================================================
# Visualization
# ==============================================================================

edgecolor = {}
for u, v in boundary1:
    edgecolor[(u, v)] = edgecolor[(v, u)] = (0, 255, 0)
for u, v in boundary2:
    edgecolor[(u, v)] = edgecolor[(v, u)] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF21_D2::KnitPatch")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges(color=edgecolor)

compas_rhino.clear_layer("DF21_D2::KnitPatch::Hooks")

for edge in mesh.edges_where({'hook': True}):
    point = Point(*mesh.edge_midpoint(*edge))
    print(point)
    artist = PointArtist(point, color=(0, 255, 0), layer="DF21_D2::KnitPatch::Hooks")
    artist.draw()

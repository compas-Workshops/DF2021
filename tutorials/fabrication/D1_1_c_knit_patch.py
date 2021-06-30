# ==============================================================================
# Import
# ==============================================================================
import os
import random

import compas_rhino
from compas.utilities import flatten
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablemesh_fofin_refined.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Draw the initial mesh
# ==============================================================================
artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(join_faces=True)
guid_edges = artist.draw_edges()
artist.redraw()

patch_1 = []
edges_1 = []
guid_edge = dict(zip(guid_edges, mesh.edges()))
guids = compas_rhino.select_lines(message="Select edges for patch 1.")
if guids:
   for guid in guids:
       if guid in guid_edge:
           start = guid_edge[guid]
           edges_1.append(start)
           strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
           strip[:] = list(set(flatten(strip)))
           patch_1.extend(strip)

artist.clear_layer()
artist.draw_faces(join_faces=True)
guid_edges = artist.draw_edges()
artist.redraw()

patch_2 = []
edges_2 = []
guid_edge = dict(zip(guid_edges, mesh.edges()))
guids = compas_rhino.select_lines(message="Select edges for patch 2.")
if guids:
    for guid in guids:
        if guid in guid_edge:
            start = guid_edge[guid]
            edges_2.append(start)
            strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
            strip[:] = list(set(flatten(strip)))
            patch_2.extend(strip)

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

artist.draw_faces(color=facecolor)
artist.draw_edges(color=edgecolor)
artist.draw_vertexlabels()
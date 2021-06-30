# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.geometry import Polyline, Frame, Transformation
from compas.geometry import project_points_plane
from compas.datastructures import Mesh
from compas.utilities import flatten
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolylineArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablemesh_fofin_patch_reactions.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)

start = list(mesh.edges_where({'seam': True}))[0]
loop = mesh.edge_loop(start)
loop_vertices = list(flatten(loop)) 
seen = set()
loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]

points = mesh.vertices_attribute('beam_pt', keys=loop_vertices)
polyline = Polyline(points)

polyartist = PolylineArtist(polyline, layer="DF2021:: Beam:: Seam:: local")
polyartist.clear_layer()
polyartist.draw(show_points=True)

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u, v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
#artist.draw()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})),join_faces=True)
artist.draw_edges(color=edgecolor)
#artist.draw_vertexlabels()
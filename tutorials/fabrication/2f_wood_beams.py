# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.geometry import Polygon, Polyline
from compas.geometry import offset_polyline
from compas.geometry import cross_vectors, normalize_vector, scale_vector, add_vectors
from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.utilities import flatten
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolygonArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin.json')
# FILE_0 = os.path.join(HERE, 'corrugation_patches.json')

mesh = Mesh.from_json(FILE_I)


proxy = Proxy('compas.geometry')
bestfit = proxy.bestfit_frame_numpy

# (18, 31), (78, 87), (83, 73)
start = (638, 842)

# find the edge loop
loop = mesh.edge_loop(start)
loop_vertices = list(flatten(loop)) # not chained
seen = set()
loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]
points = mesh.vertices_attributes('xyz', keys=loop_vertices)
polyline = Polyline(points)
origin_local, xaxis_local, yaxis_local = bestfit(polyline)
zaxis_local = normalize_vector(cross_vectors(xaxis_local, yaxis_local))

# offset the polyline
dis = 0.1 # offset distance
polyline_off = Polyline(offset_polyline(polyline, -dis, zaxis_local))

# generate 2d mesh
vertices = polyline.points + polyline_off.points 
faces = []
length = len(polyline.points)
for i in range(length - 1) :
    faces.append([i, i + 1, length + i + 1, length + i])
beam_2d = Mesh.from_vertices_and_faces(vertices, faces)

# copy
beam_side1 = beam_2d.copy()
beam_side2 = beam_2d.copy()

thickness = 0.05

for vkey in beam_2d.vertices():
    xyz = beam_2d.vertex_coordinates(vkey)

    up = scale_vector(zaxis_local, 0.5 * thickness)
    down = scale_vector(zaxis_local, -0.5 * thickness)

    beam_side1.vertex_attributes(vkey, 'xyz', add_vectors(xyz, up))
    beam_side2.vertex_attributes(vkey, 'xyz', add_vectors(xyz, down))

mesh_flip_cycles(beam_side2)

beamartist = MeshArtist(beam_side1, layer="DF2021:: Beam")
beamartist.clear_layer()
beamartist.draw_faces(join_faces=True)
beamartist.draw_edges()

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u,v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)
    
artist = MeshArtist(mesh, layer="DF2021:: Base")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges(color=edgecolor)
#artist.draw_vertexlabels()
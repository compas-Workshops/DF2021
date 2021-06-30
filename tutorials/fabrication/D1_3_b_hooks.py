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
FILE_I = os.path.join(HERE, '..', 'data', 'cablemesh_fofin_patch.json')

mesh = Mesh.from_json(FILE_I)

corner_vkey = None
for vkey in mesh.vertices():
    if mesh.vertex_degree(vkey) == 2:
        corner_vkey = vkey
        break

nbrs = mesh.vertex_neighbors(corner_vkey)

stripes1 = mesh.edge_strip((corner_vkey, nbrs[0]))
stripes2 = mesh.edge_strip((corner_vkey, nbrs[1]))

if len(stripes1) > len(stripes2):
    stripes = stripes2
else:
    stripes = stripes1

mesh.update_default_edge_attributes({'hook': False})
compas_rhino.clear_layer("DF2021:: KnitPatch1:: Hook")

edgecolor = {}
for edge in stripes:
    if mesh.edge_attribute(edge, 'seam') is True or mesh.edge_attribute(edge, 'bdr') is not None:
        loop = mesh.edge_loop(edge)
        for i, (u, v) in enumerate(loop):
            # visualize the edges
            edgecolor[(u, v)] = (0, 255, 0)
            edgecolor[(v, u)] = (0, 255, 0)

            if i % 4 == 1 or i == 0 or i == len(loop) - 1: 
                edge_center = Point(*mesh.edge_midpoint(u, v))
                mesh.edge_attribute((u, v), 'hook', True)
                print(edge_center)
                point_artist = PointArtist(edge_center, color=(0, 255, 0), layer="DF2021:: KnitPatch1:: Hook")
                point_artist.draw()

mesh.to_json(FILE_I)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges(color=edgecolor)
# artist.draw_vertices()
#artist.draw_vertexlabels()
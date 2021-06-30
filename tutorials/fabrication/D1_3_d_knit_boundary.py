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
FILE_I = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch2.json')

mesh = Mesh.from_json(FILE_I)

vkey = mesh.get_any_vertex()
nbr1 = mesh.vertex_neighbors(vkey)[0]
nbr2 = mesh.vertex_neighbors(vkey)[1]
loop1 = mesh.edge_loop((vkey, nbr1))
loop2 = mesh.edge_loop((vkey, nbr2))

if len(loop1) > len(loop2):
    strips = mesh.edge_strip((vkey, nbr1))
else:
    strips = mesh.edge_strip((vkey, nbr2))

edgecolor = {}
mesh.update_default_edge_attributes({'hook': False})
compas_rhino.clear_layer("DF2021:: KnitPatch2:: Hook")

for start in [strips[0], strips[-1]]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    for i, (u, v) in enumerate(loop):
        if i % 4 == 1 or i == 0 or i == len(loop) - 1: 
            mesh.edge_attribute((u, v), 'hook', True)
            edge_center = Point(*mesh.edge_midpoint(u, v))
            print(edge_center)
            point_artist = PointArtist(edge_center, color=(0, 255, 0), layer="DF2021:: KnitPatch2:: Hook")
            point_artist.draw()

mesh.to_json(FILE_I)
# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch2:: Knit")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges(color=edgecolor)
# artist.draw_vertices()
#artist.draw_vertexlabels()
# ==============================================================================
# Import
# ==============================================================================
import os
import compas_rhino

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '..', 'data', 'cablenmesh_fofin_patch1.json')

mesh = Mesh.from_json(FILE_I)

# find two long loops along the boundary
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
for start in [strips[0], strips[-1]]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    for (u, v) in loop:
        edgecolor[(u, v)] = (0, 255, 0)
        edgecolor[(v, u)] = (0, 255, 0)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch1:: Knit")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges(color=edgecolor)
# artist.draw_vertices()
#artist.draw_vertexlabels()
# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.datastructures import Mesh
from compas.utilities import flatten

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolylineArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin.json')
FILE_O = os.path.join(HERE, 'bridge_fofin_hook.json')

mesh = Mesh.from_json(FILE_I)

for start in [(638, 842), (1332, 493)]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    loop_vertices = list(flatten(loop)) # not chained
    seen = set()
    loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]
    
    mesh.update_default_vertex_attributes({'hook': False})
    for i, vkey in enumerate(loop_vertices):
        if i==0 or i == len(loop_vertices) -1:
            mesh.vertex_attribute(vkey, 'hook', True)
        elif i % 4 == 1:
            mesh.vertex_attribute(vkey, 'hook', True)

mesh.to_json(FILE_O)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges()
artist.draw_vertices(color={key: (255, 0, 0) for key in mesh.vertices_where({'hook': True})})
#artist.draw_vertexlabels()
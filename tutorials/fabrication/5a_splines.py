# ==============================================================================
# Import
# ==============================================================================
import os
import random

import compas_rhino
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin_reactions.json')
# FILE_O = os.path.join(HERE, 'bridge_fofin_add_patch.json')

mesh = Mesh.from_json(FILE_I)

radius = 0.008
lines = []
for start in [(1332, 493), (30, 1001), (948, 576), (567, 593), (638, 842)]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    for (u, v) in loop:
        sp, ep = mesh.edge_coordinates(u, v)
        lines.append({
                'start': sp,
                'end': ep,
                'radius': radius,
                'color': (255, 0,0),
                'name': "spline.{}-{}".format(u, v)
            })

compas_rhino.draw_cylinders(lines, layer="DF2021:: Spline", clear=False, redraw=True, cap=True)

# ==============================================================================
# Visualization
# ==============================================================================
artist = MeshArtist(mesh, layer="DF2021:: BaseMesh")
# artist.clear_layer()
#artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
#artist.draw_vertexlabels()
artist.draw_faces(join_faces=True)
artist.draw_edges()

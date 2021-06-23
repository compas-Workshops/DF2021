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

mesh = Mesh.from_json(FILE_I)

print(list(mesh.vertices_where({'is_anchor':True})))

radius = 0.008
lines = []
for (u, v) in mesh.edges():
    if mesh.vertex_attribute(u, 'is_anchor') is True and mesh.vertex_attribute(v, 'is_anchor') is True:
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

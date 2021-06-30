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
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch2.json')

mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Process
# ==============================================================================

radius = 0.008
lines = []

mesh.update_default_edge_attributes({'is_spline': False})

for u, v in mesh.edges():
    if (mesh.vertex_attribute(u, 'is_anchor') and mesh.vertex_attribute(v, 'is_anchor')):
        mesh.edge_attribute((u, v), 'is_spline', True)
    elif mesh.edge_attribute((u, v), 'cable'):
        mesh.edge_attribute((u, v), 'is_spline', True)

for u, v in mesh.edges_where({'is_spline': True}):
    sp, ep = mesh.edge_coordinates(u, v)
    lines.append({
        'start': sp,
        'end': ep,
        'radius': radius,
        'color': (255, 0, 0),
        'name': "spline.{}-{}".format(u, v)
    })

compas_rhino.draw_cylinders(lines, layer="DF21_D2::KnitPatch2::Spline", clear=False, redraw=True, cap=True)
mesh.to_json(FILE_I)

# ==============================================================================
# Visualization
# ==============================================================================

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch2:: Knit")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges()

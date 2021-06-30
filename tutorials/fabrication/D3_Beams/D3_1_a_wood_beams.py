# ==============================================================================
# Import
# ==============================================================================
import os

from compas.geometry import normalize_vector, subtract_vectors
from compas.datastructures import Mesh
import compas_rhino

from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch.json')
FILE_O = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_patch_reactions.json')

mesh = Mesh.from_json(FILE_I)
mesh.update_default_vertex_attributes({'beam_pt': None})

lines = []
compas_rhino.clear_layer("DF2021_D2::KnitPatch::Reactions")

edges = list(mesh.edges_where({'seam': True})) + list(mesh.edges_where({'bdr': 1})) + list(mesh.edges_where({'bdr': 2}))
for (u, v) in edges:
    if mesh.vertex_attribute(u, 'beam_pt') is None:
        rx, ry, rz = mesh.vertex_attributes(u, ('rx', 'ry', 'rz'))
        residual = normalize_vector([rx, ry, rz])
        xyz = mesh.vertex_coordinates(u)
        end = subtract_vectors(xyz, residual)
        lines.append(
            {'start': xyz, 
             'end': end, 
             'arrow': 'end',
             'color': (0, 255, 0)})
        mesh.vertex_attribute(u, 'beam_pt', end)

    if mesh.vertex_attribute(v, 'beam_pt') is None:
        rx, ry, rz = mesh.vertex_attributes(v, ('rx', 'ry', 'rz'))
        residual = normalize_vector([rx, ry, rz])
        xyz = mesh.vertex_coordinates(v)
        end = subtract_vectors(xyz, residual)
        lines.append(
            {'start': xyz,
             'end': end,
             'arrow': 'end',
             'color': (0, 255, 0)})
        mesh.vertex_attribute(v, 'beam_pt', end)

mesh.to_json(FILE_O)


# ==============================================================================
# Visualization
# ==============================================================================
compas_rhino.draw_lines(lines, layer="DF2021:: KnitPatch:: Reactions")

artist = MeshArtist(mesh, layer="DF2021:: KnitPatch:: Base")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges()
# artist.draw_vertexlabels()

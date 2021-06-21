# ==============================================================================
# Import
# ==============================================================================
import os
import compas_rhino
from compas.datastructures import Mesh 
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_O = os.path.join(DATA, 'basemesh.json')

print(HERE)
print(DATA)
print(FILE_O)

# ==============================================================================
# Mesh from xy lines
# ==============================================================================
guids = compas_rhino.select_lines(message='Select Lines')
compas_rhino.rs.HideObjects(guids)
lines = compas_rhino.get_line_coordinates(guids)
mesh = Mesh.from_lines(lines, delete_boundary_face=True)
# print(mesh)

# ==============================================================================
# Visualization
# ==============================================================================
artist = MeshArtist(mesh, layer="DF2021:: InputMesh")
artist.clear_layer()
#artist.draw()
#artist.draw_faces(join_faces=True)
artist.draw_edges()
#artist.draw_vertices()
#artist.draw_vertexlabels()
#artist.draw_facelabels()
artist.redraw()

# ==============================================================================
# Export
# ==============================================================================
mesh.to_json(FILE_O)
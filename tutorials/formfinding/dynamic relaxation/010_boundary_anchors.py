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
DATA = os.path.abspath(os.path.join(HERE, 'data'))
FILE_I = os.path.join(DATA, 'basemesh.json')
FILE_O = os.path.join(DATA, 'basemesh_anchors.json')

# ==============================================================================
# Mesh and Anchors
# ==============================================================================
mesh = Mesh.from_json(FILE_I)

# anchor the vertices on the left and right boundary
y_min = min(set(mesh.vertices_attribute('y')))
y_max = max(set(mesh.vertices_attribute('y')))

anchors = []
anchors.extend([35,21,0, 54,60,40,26,55,38])
anchors.extend(list(mesh.vertices_on_boundary()))
mesh.vertices_attribute('is_anchor', True, keys=anchors)

# ==============================================================================
# Visualization
# ==============================================================================
artist = MeshArtist(mesh, layer="DF2021:: InputMesh")
artist.clear_layer()
artist.draw_faces(join_faces=True)
artist.draw_edges()
artist.draw_vertices(vertices=anchors, color=(255, 0, 0))
#artist.draw_vertexlabels()
#artist.draw_facelabels()
artist.redraw()

# ==============================================================================
# Export
# ==============================================================================
mesh.to_json(FILE_O)
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
FILE_I = os.path.join(DATA, 'basemesh.json')
FILE_O = os.path.join(DATA, 'basemesh_anchors.json')

# ==============================================================================
# Mesh and Anchors
# ==============================================================================
mesh = Mesh.from_json(FILE_I)
mesh = mesh.subdivide(scheme = 'quad')

# anchor the vertices on the left and right boundary
y_min = min(set(mesh.vertices_attribute('y')))
y_max = max(set(mesh.vertices_attribute('y')))

anchors = []
anchors.extend(list(mesh.vertices_where({'y': y_min})))
anchors.extend(list(mesh.vertices_where({'y': y_max})))
mesh.vertices_attribute('is_anchor', True, keys=anchors)
mesh.vertices_attribute('z', -200, keys=list(mesh.vertices_where({'y': y_min})))

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
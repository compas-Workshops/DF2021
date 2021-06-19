# ==============================================================================
# Import
# ==============================================================================
import os

from compas.datastructures import Mesh
from compas.rpc import Proxy
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Proxy
# ==============================================================================
proxy = Proxy('compas.numerical')
fd = proxy.fd_numpy

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_I = os.path.join(DATA, 'basemesh_anchors.json')
FILE_O = os.path.join(DATA, 'fofinmesh.json')

# ==============================================================================
# Cablenet mesh datastructure
# ==============================================================================
# create the mesh from imported geometry
mesh = Mesh.from_json(FILE_I)

# set default vertex attributes
dva = {
    'rx': 0.0,            # X-component of an residual force.
    'ry': 0.0,            # Y-component of an residual force.
    'rz': 0.0,            # Z-component of an residual force.
    'px': 0.0,            # X-component of an externally applied load.
    'py': 0.0,            # Y-component of an externally applied load.
    'pz': 0.0,            # Z-component of an externally applied load.
    'is_anchor': False,   # Indicate that a vertex is anchored and can take reaction forces in XYZ.
}
mesh.update_default_vertex_attributes(dva)

# set default edge attributes
dea = {
    'q': 1.0,             # Force densities of an edge.
    'f': 0.0,             # Force in an edge.
    'l': 0.0,             # Stressed Length of an edge.
    'l0': 0.0,            # Unstressed Length of an edge.
}
mesh.update_default_edge_attributes(dea)

# ==============================================================================
# Compile numerical data as fofin input
# ==============================================================================
# to map vertex dictionary keys to the corresponding index in a vertex list
vertex_index = mesh.key_index()

# complile lists (ordered in indices) of geometry, loads and force densities
X = mesh.vertices_attributes('xyz')
P = mesh.vertices_attributes(['px', 'py', 'pz'])
Q = mesh.edges_attribute('q')

# translate anchored vertex keys to index list of fixed vertices
fixed = [vertex_index[vertex] for vertex in mesh.vertices_where({'is_anchor': True})]
# translate edges from vertex keys to indexes
edges = [(vertex_index[u], vertex_index[v]) for u, v in mesh.edges()]

# ==============================================================================
# Compute equilibrium
# ==============================================================================
X, Q, F, L, R = fd(X, edges, fixed, Q, P)

# ==============================================================================
# Update cablenet mesh
# ==============================================================================
for vertex in mesh.vertices():
    # translate back from indices to keys
    index = vertex_index[vertex]
    mesh.vertex_attributes(vertex, 'xyz', X[index])
    mesh.vertex_attributes(vertex, ['rx', 'ry', 'rz'], R[index])

for index, edge in enumerate(mesh.edges()):
    # translate back from indices to keys
    mesh.edge_attribute(edge, 'q', Q[index][0])
    mesh.edge_attribute(edge, 'f', F[index][0])
    mesh.edge_attribute(edge, 'l', L[index][0])

# ==============================================================================
# Visualize
# ==============================================================================
artist = MeshArtist(mesh, layer="DF2021:: FofinMesh")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
artist.draw_edges()
artist.draw_faces()

# ==============================================================================
# Export
# ==============================================================================

mesh.to_json(FILE_O)

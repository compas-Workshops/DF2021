import os

from compas.datastructures import Mesh
from compas.numerical import dr

from compas_rhino.artists import MeshArtist


# ==============================================================================
# Helpers > NEW
# ==============================================================================

def fofin(mesh):
    """Compute equilibrium and update the geometry.
    """
    # ==============================================================================
    # Compile numerical data as fofin input
    # ==============================================================================

    # to map vertex dictionary keys to the corresponding index in a vertex list
    vertex_index = mesh.key_index()

    # complile lists (ordered in indices) of geometry, loads, force densities
    X = mesh.vertices_attributes('xyz')
    P = mesh.vertices_attributes(['px', 'py', 'pz'])
    Q = mesh.edges_attribute('q')

    # translate anchored vertex keys to index list of fixed vertices
    fixed = [vertex_index[vertex] for vertex in mesh.vertices_where({'is_anchor': True})]  # noqa: E501
    # translate edges from vertex keys to indexes
    edges = [(vertex_index[u], vertex_index[v]) for u, v in mesh.edges()]

    # ==============================================================================
    # Compute equilibrium
    # ==============================================================================

    X, Q, F, L, R = dr(X, edges, fixed, P, Q)

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
        mesh.edge_attribute(edge, 'q', Q[index])
        mesh.edge_attribute(edge, 'f', F[index])
        mesh.edge_attribute(edge, 'l', L[index])


# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '../..', 'data'))
FILE_I = os.path.join(DATA, 'cablemesh_import.json')

# ==============================================================================
# a. Cablenet mesh datastructure
# ==============================================================================

# a1. create the mesh from imported geometry
mesh = Mesh.from_json(FILE_I)

# a2. set default vertex and edge attributes
dva = {
    'rx': 0.0,            # X-component of a residual force.
    'ry': 0.0,            # Y-component of a residual force.
    'rz': 0.0,            # Z-component of a residual force.
    'px': 0.0,            # X-component of an externally applied load.
    'py': 0.0,            # Y-component of an externally applied load.
    'pz': 0.0,            # Z-component of an externally applied load.
    'is_anchor': False    # Indicate that a vertex is anchored and can take reaction forces in XYZ.  # noqa: E501
}
mesh.update_default_vertex_attributes(dva)

dea = {
    'q': 1.0,             # Force densities of an edge.
    'f': 0.0,             # Force in an edge.
    'l': 0.0,             # Stressed Length of an edge.
    'l0': 0.0,            # Unstressed Length of an edge.
}
mesh.update_default_edge_attributes(dea)

# a3. Boundary conditions
boundary = mesh.vertices_on_boundaries()[0]
mesh.vertices_attribute('is_anchor', True, keys=boundary)

# ==============================================================================
# c. Compute equilibrium and update the geometry > NEW
# ==============================================================================

fofin(mesh)

# ==============================================================================
# Visualize
# ==============================================================================

baselayer = "DF21_C2::02_Basic Form Finding"

artist = MeshArtist(mesh, layer=baselayer+"::Mesh")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})  # noqa: E501
artist.draw_edges()
artist.draw_faces()

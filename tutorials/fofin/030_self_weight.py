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
# Helpers
# ==============================================================================

def selfweight(mesh):
    """Compute the selfweight per vertex and update the load attribute in negative z.
    """
    density = mesh.attributes['density']

    # for all vertices that are free
    for key, attr in mesh.vertices_where({'is_anchor': False}, True):

        # get the thickness of the vertex
        thickness = attr['t']

        # compute the tributary area of the vertex
        area = mesh.vertex_area(key)
        
        # compute the concrete weight
        selfweight = area * thickness * density

        # apply selfweight by updating vertex attribute (acting in negative z)
        attr['pz'] = selfweight

def fofin(mesh):

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
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_I = os.path.join(DATA, 'fofinmesh.json')
FILE_O = os.path.join(DATA, 'fofinmesh_sw.json')

# ==============================================================================
# Cablenet mesh datastructure
# ==============================================================================

# create the mesh from form found geometry with the set default attributes
mesh = Mesh.from_json(FILE_I)

## Boundary conditions
#boundary = mesh.vertices_on_boundaries()[0]
#mesh.vertices_attribute('is_anchor', True, keys=boundary)

# set new default vertex attributes
dva = {
    't': 0.00005,          # Thickness of the concrete shell.
}
mesh.update_default_vertex_attributes(dva)

# set mesh attributes
mesh.attributes['density'] = 14.0  # Density of the lightweight concrete.


# ==============================================================================
# Fofin for selfweight
# ==============================================================================
# compute selfweight for the current geometry
selfweight(mesh)

# form finding with selfweight loads and geometry update
fofin(mesh)

# ==============================================================================
# Visualize
# ==============================================================================
artist = MeshArtist(mesh, layer="DF2021:: FofinMesh_sw")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
artist.draw_edges()
artist.draw_faces()
artist.draw_vertexlabels()

# ==============================================================================
# Export
# ==============================================================================
mesh.to_json(FILE_O)

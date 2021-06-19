import os

from compas.datastructures import Mesh
from compas.rpc import Proxy

from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import length_vector

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
        attr['pz'] = -selfweight


def fofin(mesh):
    """Compute equilibrium and update the geometry.
    """
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


def update_residual(mesh, loads_previous):
    """Compute the residual forces with respect to the stored loads.
    """
    key_index = mesh.key_index()

    R = []
    for key in mesh.vertices_where({'is_anchor': False}):

        index = key_index[key]

        p_previous = loads_previous[index]
        p = mesh.vertex_attributes(key, ['px', 'py', 'pz'])
        r = mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])

        r = add_vectors(r, subtract_vectors(p, p_previous))

        mesh.vertex_attributes(key, ['rx', 'ry', 'rz'], r)

        r_length = length_vector(r)
        R.append(r_length)

    residuals = sum(R)

    return residuals


def fofin_selfweight(mesh):
    """Compute the equilibrium for the concrete selfweight with the iterative procedure.
    """
    # define maximum iterations and tolerance for residuals
    tol = 0.001
    kmax = 10

    # store previous selfweight loads (zero)
    loads_previous = mesh.vertices_attributes(('px', 'py', 'pz'))
    # !!! here already not zero anymore but must at least run one iteration

    # compute selfweight for the current geometry
    selfweight(mesh)

    # for all k smaller than kmax
    for k in range(kmax):

        # recompute the residuals with difference of selfweight from updated to previous geometry
        residuals = update_residual(mesh, loads_previous)

        # stopping criteria if updated residual is smaller than tolerance or at least once
        print('k', k, 'residuals', residuals)
        if residuals < tol and not k == 0:
            print('Convergence!')
            break

        # form finding with selfweight loads and geomtry update
        fofin(mesh)

        # store previous selfweight loads (computed before the updated geometry)
        loads_previous = mesh.vertices_attributes(('px', 'py', 'pz'))

        # recompute selfweight for the updated geometry
        selfweight(mesh)


# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_I = os.path.join(DATA, 'fofinmesh_sw.json')
FILE_O = os.path.join(DATA, 'fofinmesh_sw_q.json')


# ==============================================================================
# Cablenet mesh datastructure
# ==============================================================================

# create the mesh from form found geometry with the set default attributes
mesh = Mesh.from_json(FILE_I)
# set new default vertex attributes
dva = {
    't': 0.00005,          # Thickness of the concrete shell.
}
mesh.update_default_vertex_attributes(dva)

# set mesh attributes
mesh.attributes['density'] = 14.0  # Density of the lightweight concrete.

# ==============================================================================
# Single Cable
# ==============================================================================

# find cables to create crease
loop_1_st = (6, 88)
loop_1 = mesh.edge_loop(loop_1_st)

loop_2_st = (7,103)
loop_2 = mesh.edge_loop(loop_2_st)

loop_3_st = (14, 127)
loop_3 = mesh.edge_loop(loop_3_st)

# ==============================================================================
# Variable Force Denisties
# ==============================================================================
# explore increased force denisties for all edges
mesh.edges_attribute('q', 1)

# increase force densities of center cable to create crease
mesh.edges_attribute('q', -20, keys=loop_1+loop_2)
#mesh.edges_attribute('q', 20, keys=loop_3)
# ==============================================================================
# Fofin for selfweight
# ==============================================================================

fofin_selfweight(mesh)

# ==============================================================================
# Visualize
# ==============================================================================
artist = MeshArtist(mesh, layer="DF2021:: FofinMesh_sw")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})
artist.draw_edges()
artist.draw_faces()

# ==============================================================================
# Export
# ==============================================================================

mesh.to_json(FILE_O)

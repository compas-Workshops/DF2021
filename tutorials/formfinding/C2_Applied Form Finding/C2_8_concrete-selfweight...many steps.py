import os

from compas.datastructures import Mesh
from compas.numerical import dr

from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import length_vector

from compas_rhino.artists import MeshArtist
from C2_3_visualisation import draw_reactions
from C2_3_visualisation import draw_residuals
from C2_3_visualisation import draw_forces
from C2_3_visualisation import draw_loads


# ==============================================================================
# Helpers
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


def selfweight(mesh):
    """Compute the selfweight per vertex and update the load attribute in negative z.  # noqa: E501
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
    """Compute the equilibrium for the concrete selfweight with the iterative procedure.  # noqa: E501
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

        # recompute the residuals with difference of selfweight from updated to previous geometry  # noqa: E501
        residuals = update_residual(mesh, loads_previous)

        # stopping criteria if updated residual is smaller than tolerance or at least once  # noqa: E501
        print('k', k, 'residuals', residuals)
        if residuals < tol and not k == 0:
            print('Convergence!')
            break

        # form finding with selfweight loads and geomtry update
        fofin(mesh)

        # store previous selfweight loads (computed before the updated geometry)  # noqa: E501
        loads_previous = mesh.vertices_attributes(('px', 'py', 'pz'))

        # recompute selfweight for the updated geometry
        selfweight(mesh)


def longitudinal_cables(mesh):
    """Find all cables in the longitudinal direction.
    """

    # select starting corner
    corners = list(mesh.vertices_where({'vertex_degree': 2}))
    corner = corners[0]

    # check in which direction the edge is shorter
    corner_edges = mesh.vertex_neighbors(corner)

    edgeA = (corner, corner_edges[0])
    edgeB = (corner, corner_edges[1])

    loopA = mesh.edge_loop(edgeA)
    loopB = mesh.edge_loop(edgeB)

    if len(loopA) >= len(loopB):
        start = edgeA
    else:
        start = edgeB

    # get all edges parallel to the start edge
    starts = mesh.edge_strip(start)

    # get all cables for all parallel starts
    cables = []
    for start in starts:
        cable = mesh.edge_loop(start)
        cables.append(cable)

    return cables


# ==============================================================================
# Initialise
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_I = os.path.join(DATA, 'cablenmesh_import_refined.json')

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
    'pz': -0.1,           # Z-component of an externally applied load. # NEW! try with and without!  # noqa: E501
    'is_anchor': False,   # Indicate that a vertex is anchored and can take reaction forces in XYZ.  # noqa: E501
    't': 0.035            # Thickness of the concrete shell. # NEW!
}
mesh.update_default_vertex_attributes(dva)

# set default edge attributes
dea = {
    'q': 1.0,             # Force densities of an edge. # NEW: back to 1
    'f': 0.0,             # Force in an edge.
    'l': 0.0,             # Stressed Length of an edge.
    'l0': 0.0,            # Unstressed Length of an edge.
}
mesh.update_default_edge_attributes(dea)

# set mesh attributes # NEW!
mesh.attributes['density'] = 24.0  # Density of the lightweight concrete.

# ==============================================================================
# Find All Cables in the Long Direction
# ==============================================================================

cables = longitudinal_cables(mesh)

# ==============================================================================
# Add centre vertices to anchors
# ==============================================================================

# external boundary
boundary = mesh.vertices_on_boundaries()[0]

# find center cable to create internal boundary
centre_vertices = [u for u, v in cables[2]]

mesh.vertices_attribute('is_anchor', True, keys=boundary+centre_vertices)

# ==============================================================================
# Side Cables through Variable Force Densities
# ==============================================================================

# increase force densities to crease creases
mesh.edges_attribute('q', 10, keys=cables[1]+cables[3])

# ==============================================================================
# Compute equilibrium and update the geometry under changing selfweight # NEW!
# ==============================================================================

fofin_selfweight(mesh)

# ==============================================================================
# Visualize
# ==============================================================================

baselayer = "DF21_C2::08 Concrete Selfweight"

artist = MeshArtist(mesh, layer=baselayer+"::Mesh")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})  # noqa: E501
artist.draw_edges()
artist.draw_faces()

draw_reactions(mesh, baselayer=baselayer)
draw_residuals(mesh, baselayer=baselayer)
draw_forces(mesh, baselayer=baselayer)
draw_loads(mesh, baselayer=baselayer)

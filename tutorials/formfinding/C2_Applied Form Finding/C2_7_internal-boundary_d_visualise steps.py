import os

from compas.datastructures import Mesh
from compas.numerical import dr
from compas.utilities import flatten

from compas_rhino.artists import MeshArtist
from C2_3_visualisation import draw_reactions  # noqa F401
from C2_3_visualisation import draw_residuals  # noqa F401
from C2_3_visualisation import draw_forces  # noqa F401
from C2_3_visualisation import draw_loads  # noqa F401


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


# ==============================================================================
# c. Initialise
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '../..', 'data'))
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
    'pz': -0.1,           # Z-component of an externally applied load.
    'is_anchor': False,   # Indicate that a vertex is anchored and can take reaction forces in XYZ.  # noqa: E501
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
# d. Find All Cables in the Long Direction > NEW
# ==============================================================================

# d1. Longer Boundary
#     select starting corner
corners = list(mesh.vertices_where({'vertex_degree': 2}))
corner = corners[0]

#     check in which direction the edge is shorter
corner_edges = mesh.vertex_neighbors(corner)

edgeA = (corner, corner_edges[0])
edgeB = (corner, corner_edges[1])

loopA = mesh.edge_loop(edgeA)
loopB = mesh.edge_loop(edgeB)

if len(loopA) >= len(loopB):
    start_long = edgeA
    loop = loopA
else:
    start_long = edgeB
    loop = loopB

print(corner)
print(edgeA, edgeB)
print(start_long)
print(loop)

# d2. get all edges parallel to the start edge
starts = mesh.edge_strip(start_long)

# d3. get all cables for all parallel starts
cables = []
for start in starts:
    cable = mesh.edge_loop(start)
    cables.append(cable)

# ==============================================================================
# a. Add centre vertices to anchors
# ==============================================================================

# external boundary
boundary = mesh.vertices_on_boundaries()[0]

# find vertices on center continuous edges to create internal boundary
centre_vertices = list(set(flatten(cables[2])))

mesh.vertices_attribute('is_anchor', True, keys=boundary+centre_vertices)

# ==============================================================================
# b. Side Cables through Variable Force Densities > NEW
# ==============================================================================

# increase force densities to crease creases
mesh.edges_attribute('q', 10, keys=cables[1]+cables[3])

# ==============================================================================
# Compute equilibrium and update the geometry
# ==============================================================================

fofin(mesh)

# ==============================================================================
# Visualize
# ==============================================================================

# d1. Longer Boundary
edgecolor = {}
for edge in loop:
    if edge not in mesh.edges():
        edge = (edge[1], edge[0])
    edgecolor[edge] = (0, 255, 0)

if start_long not in mesh.edges():
    start_long = (start_long[1], start_long[0])
    print(start_long)
edgecolor[start_long] = (255, 0, 0)

vertexcolor = {}
vertexcolor[corner] = (255, 0, 0)

# d2. get all edges parallel to the start edge
# edgecolor = {}
# for edge in starts:
#     if edge not in mesh.edges():
#         edge = (edge[1], edge[0])
#     edgecolor[edge] = (0, 255, 0)

# if start_long not in mesh.edges():
#     start_long = (start_long[1], start_long[0])
#     print(start_long)
# edgecolor[start_long] = (255, 0, 0)

# vertexcolor = {}
# vertexcolor[corner] = (255, 0, 0)

# d3. get all cables for all parallel starts
# edgecolor = {}
# for edge in flatten(cables):
#     if edge not in mesh.edges():
#         edge = (edge[1], edge[0])
#     edgecolor[edge] = (0, 255, 0)

# for edge in starts:
#     if edge not in mesh.edges():
#         edge = (edge[1], edge[0])
#     edgecolor[edge] = (255, 0, 0)

# vertexcolor = {}
# vertexcolor[corner] = (255, 0, 0)

# always
baselayer = "DF21_C2::07 Internal Boundary_Refined_d"
artist = MeshArtist(mesh, layer=baselayer+"::Mesh")
artist.clear_layer()
artist.draw_vertices(color=vertexcolor)
artist.draw_edges(color=edgecolor)
artist.draw()

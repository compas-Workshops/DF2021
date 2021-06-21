# ==============================================================================
# Import
# ==============================================================================
import os

from compas.datastructures import Mesh
from compas.rpc import Proxy
from compas.geometry import distance_point_point_xy
from compas.geometry import midpoint_point_point_xy
from compas.geometry import intersection_line_line_xy
from compas_rhino.artists import MeshArtist
from compas.utilities import pairwise

# ==============================================================================
# Proxy
# ==============================================================================
fd = Proxy('compas.numerical').fd_numpy

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
# Boundary Conditions
# ==============================================================================

def split_boundary(pattern):
    boundaries = pattern.vertices_on_boundaries()
    exterior = boundaries[0]
    opening = []
    openings = [opening]
    for vertex in exterior:
        opening.append(vertex)
        if pattern.vertex_attribute(vertex, 'is_anchor'):
            opening = [vertex]
            openings.append(opening)
    print(openings)
    openings[-1] += openings[0]
    print(openings)
    del openings[0]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    openings[:] = [opening for opening in openings if len(opening) > 2]
    return openings

target_sag = 0.15
 
def compute_sag(pattern, opening):
    u, v = opening[0]
    if pattern.vertex_attribute(u, 'is_fixed'):
        a = pattern.vertex_attributes(u, 'xyz')
        aa = pattern.vertex_attributes(v, 'xyz')
    else:
        a = pattern.vertex_attributes(v, 'xyz')
        aa = pattern.vertex_attributes(u, 'xyz')
    u, v = opening[-1]
    if pattern.vertex_attribute(u, 'is_fixed'):
        b = pattern.vertex_attributes(u, 'xyz')
        bb = pattern.vertex_attributes(v, 'xyz')
    else:
        b = pattern.vertex_attributes(v, 'xyz')
        bb = pattern.vertex_attributes(u, 'xyz')
    span = distance_point_point_xy(a, b)
    apex = intersection_line_line_xy((a, aa), (b, bb))
    if apex is None:
        rise = 0.0
    else:
        midspan = midpoint_point_point_xy(a, b)
        rise = 0.5 * distance_point_point_xy(midspan, apex)
    sag = rise / span
    return sag
    
openings = split_boundary(mesh)
# convert the list of vertices to a list of segments
openings = [list(pairwise(opening)) for opening in openings]
targets = []
for opening in openings:
    targets.append(target_sag)

Q = []

for opening in openings:
    print(opening)
    print(len(opening))
#    q = mesh.edges_attribute('q', keys=opening)
#    q = sum(q) / len(q)
#    Q.append(q)
#    mesh.edges_attribute('q', q, keys=opening)
    
    
# ==============================================================================
# Relax Boundaries
# ==============================================================================
proxy = Proxy()
proxy.package = 'compas_tna.utilities'

anchors = list(mesh.vertices_where({'is_anchor': True}))
meshdata = proxy.relax_boundary_openings_proxy(mesh.to_data(), anchors)
mesh = Mesh.from_data(meshdata)

TOL2 = 0.001 ** 2

## update Qs to match target sag
#count = 0
#while True and count < 10:
#    count += 1
#    sags = [compute_sag(mesh, opening) for opening in openings]
#    if all((sag - target) ** 2 < TOL2 for sag, target in zip(sags, targets)):
#        break
#    for i in range(len(openings)):
#        sag = sags[i]
#        target = targets[i]
#        q = Q[i]
#        q = sag / target * q
#        Q[i] = q
#        opening = openings[i]
#        mesh.edges_attribute('q', Q[i], keys=opening)
#    meshdata = proxy.relax_boundary_openings_proxy(mesh.to_data(), anchors)
#    mesh = Mesh.from_data(meshdata)
#
#if count == 10:
#    print("did not converge after 10 iterations")
#else:
#    print("converged after %s iterations" % count)


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

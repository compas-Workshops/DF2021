import os

from compas.datastructures import Mesh
from compas.numerical import dr  # noqa: F401

from compas_rhino.artists import MeshArtist

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
# Visualize
# ==============================================================================

baselayer = "DF21_C2::02_Basic Form Finding"

artist = MeshArtist(mesh, layer=baselayer+"::InputMesh")
artist.clear_layer()

artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in mesh.vertices_where({'is_anchor': True})})  # noqa: E501
artist.draw_edges()
artist.draw_faces()

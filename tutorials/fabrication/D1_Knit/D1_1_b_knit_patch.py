# ==============================================================================
# Import
# ==============================================================================
import os

from compas.utilities import flatten
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, '../..', 'data', 'cablemesh_fofin_refined.json')
mesh = Mesh.from_json(FILE_I)

# ==============================================================================
# Select faces
# ==============================================================================
m_key = 67
nbrs = mesh.vertex_neighbors(m_key)

if len(nbrs) != 3:
    raise ValueError("Vertex does not lie on the boundary.")

edge_loops = []
for nbr in nbrs:
    edge_loop = []
    if mesh.is_vertex_on_boundary(nbr) is True:
        current, previous = (nbr, m_key)
        edge_loop.append((previous, current))

        while True:
            if current == m_key:
                break
            nbrs = mesh.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if mesh.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edge_loop.append((previous, current))

    edge_loops.append(edge_loop)

edges_1 = edge_loops[0]
edges_2 = edge_loops[1]

patch_1 = []
patch_2 = []

for start in edges_1:
    strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
    strip[:] = list(set(flatten(strip)))
    patch_1.extend(strip)

for start in edges_2:
    strip = [mesh.edge_faces(*edge) for edge in mesh.edge_strip(start)]
    strip[:] = list(set(flatten(strip)))
    patch_2.extend(strip)

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in edges_1:
    edgecolor[(u, v)] = (255, 0, 0)
    edgecolor[(v, u)] = (255, 0, 0)

for (u, v) in edges_2:
    edgecolor[(u, v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)

facecolor = {}
for face in patch_1:
    facecolor[face] = (255, 200, 200)

for face in patch_2:
    facecolor[face] = (200, 255, 200)

artist = MeshArtist(mesh, layer="DF2021_D1::KnitPatch")
artist.clear_layer()
artist.draw_faces(color=facecolor)
artist.draw_edges(color=edgecolor)
# artist.draw_vertexlabels()

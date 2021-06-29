from compas.geometry import add_vectors, subtract_vectors
from compas.datastructures import Network

import compas_rhino
from compas_rhino.artists import NetworkArtist

# ==============================================================================
# create a network
# ==============================================================================

# with 5 nodes and 4 edges

network = Network()

network.update_dna(is_anchor=False)
network.update_dna(rx=0, ry=0, rz=0)
network.update_dea(f=1)

a = network.add_node(x=0, y=0, z=0, is_anchor=True)
b = network.add_node(x=10, y=0, z=10, is_anchor=True)
c = network.add_node(x=10, y=10, z=0, is_anchor=True)
d = network.add_node(x=0, y=10, z=10, is_anchor=True)

e = network.add_node(x=5, y=5, z=0)

network.add_edge(a, e)
network.add_edge(b, e)
network.add_edge(c, e)
network.add_edge(d, e)

# ==============================================================================
# compute the residual forces in the current geometry > NEW
# ==============================================================================

for node in network.nodes():
    A = network.node_attributes(node, 'xyz')
    R = [0, 0, 0]

    for nbr in network.neighbors(node):
        B = network.node_attributes(nbr, 'xyz')

        edge = node, nbr
        if not network.has_edge(*edge):
            edge = nbr, node

        F = network.edge_attribute(edge, 'f')
        L = network.edge_length(*edge)
        R[0] += F * (B[0] - A[0]) / L
        R[1] += F * (B[1] - A[1]) / L
        R[2] += F * (B[2] - A[2]) / L
        
    network.node_attributes(node, ['rx', 'ry', 'rz'], R)

# ==============================================================================
# visualize the geometry
# ==============================================================================

# clear the Rhino model
compas_rhino.clear()

layer = "DF21_C0::FormFinding"
artist = NetworkArtist(network, layer=layer)

# color the anchors red
artist.draw_nodes(color={node: (255, 0, 0) for node in
                  network.nodes_where({'is_anchor': True})})
artist.draw_edges()

# ==============================================================================
# visualize the reaction forces > NEW (no more forces)
# ==============================================================================

lines = []
for node in network.nodes():
    start = network.node_attributes(node, 'xyz')
    residual = network.node_attributes(node, ['rx', 'ry', 'rz'])
    if network.node_attribute(node, 'is_anchor'):
        end = subtract_vectors(start, residual)
        color = (0, 255, 0)
    else:
        end = add_vectors(start, residual)
        color = (0, 255, 255)
    lines.append(
        {'start': start,
         'end': end,
         'arrow': 'end',
         'color': color})

compas_rhino.draw_lines(lines, layer=layer)
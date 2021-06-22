from compas.geometry import add_vectors, subtract_vectors, length_vector
from compas.datastructures import Network

import compas_rhino
from compas_rhino.artists import NetworkArtist


# ==============================================================================
# helper functions > NEW (refactoring of code)
# ==============================================================================

def update_residuals(network):
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


def update_geometry(network):
    for node in network.nodes_where({'is_anchor': False}):
        rx, ry, rz = network.node_attributes(node, ['rx', 'ry', 'rz'])
        x0, y0, z0 = network.node_attributes(node, 'xyz')
        x1 = x0 + 0.5 * rx
        y1 = y0 + 0.5 * ry
        z1 = z0 + 0.5 * rz
        network.node_attributes(node, 'xyz', [x1, y1, z1])


def draw_reactions(network, layer, color):
    lines = []
    for node in network.nodes_where({'is_anchor': True}):
        start = network.node_attributes(node, 'xyz')
        residual = network.node_attributes(node, ['rx', 'ry', 'rz'])
        end = subtract_vectors(start, residual)
        lines.append(
            {'start': start,
            'end': end,
            'arrow': 'end',
            'color': color})
    compas_rhino.draw_lines(lines, layer=layer)


def draw_residuals(network, layer, color, tol):
    lines = []
    for node in network.nodes_where({'is_anchor': False}):
        start = network.node_attributes(node, 'xyz')
        residual = network.node_attributes(node, ['rx', 'ry', 'rz'])
        if length_vector(residual) < tol:
            continue
        end = add_vectors(start, residual)
        lines.append(
            {'start': start,
            'end': end,
            'arrow': 'end',
            'color': color})
    compas_rhino.draw_lines(lines, layer=layer)


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
# try with a longer edge instead:
# b = network.add_node(x=20, y=-10, z=20, is_anchor=True)
c = network.add_node(x=10, y=10, z=0, is_anchor=True)
d = network.add_node(x=0, y=10, z=10, is_anchor=True)

e = network.add_node(x=5, y=5, z=0)

network.add_edge(a, e)
# try with a higher force instead:
# network.add_edge(a, e, f=2)
network.add_edge(b, e)
network.add_edge(c, e)
network.add_edge(d, e)

fixed = list(network.nodes_where({'is_anchor': True}))
free = list(network.nodes_where({'is_anchor': False}))


# ==============================================================================
# clear the Rhino model
# ==============================================================================
# and define the drawing helpers/parameters

compas_rhino.clear()
layer = "DF21::C0::FormFinding"
artist = NetworkArtist(network, layer=layer)


# ==============================================================================
# iterative equilibrium finding > NEW
# ==============================================================================
# define maximum iterations and tolerance for residuals
tol = 0.01
kmax = 100

# compute the residual forces in the original geometry
update_residuals(network)

for k in range(kmax):

    # stopping criteria
    R = network.nodes_attributes(['rx', 'ry', 'rz'], keys=free)
    res = sum(length_vector(r) for r in R)
    if res < tol:
        break

    # update the geometry based on the previous residuals
    update_geometry(network)
    # then recompute the residuals in the new geometry
    update_residuals(network)


# ==============================================================================
# visualization
# ==============================================================================

artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
artist.draw_edges()

draw_reactions(network, layer, (0, 255, 0))
draw_residuals(network, layer, (0, 255, 255), tol)
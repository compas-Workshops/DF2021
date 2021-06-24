import random
from compas.geometry import add_vectors, subtract_vectors, length_vector
from compas.datastructures import Network

from compas.numerical import dr

import compas_rhino
from compas_rhino.artists import NetworkArtist


# ==============================================================================
# helpers > NEW (callback)
# ==============================================================================

def update_network():
    for node in network.nodes():
        index = node_index[node]
        network.node_attributes(node, 'xyz', X[index])
        network.node_attributes(node, ['rx', 'ry', 'rz'], R[index])

    for index, edge in enumerate(network.edges()):
        network.edge_attribute(edge, 'q', Q[index])
        network.edge_attribute(edge, 'f', F[index])


def callback_visualize(k, X, crits, args):
    if k % 1 == 0:
        # update nodal coordinates
        compas_rhino.wait()
        for node in network.nodes():
            index = node_index[node]
            network.node_attributes(node, 'xyz', X[index])

        # visualize updated geometry
        artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
        artist.draw_edges()
        draw_loads(network, layer, (255, 0, 0))
        compas_rhino.rs.Redraw()
        compas_rhino.wait()



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


def draw_loads(network, layer, color):
    lines = []
    for node in network.nodes():
        start = network.node_attributes(node, 'xyz')
        load = network.node_attributes(node, ['px', 'py', 'pz'])
        end = add_vectors(start, load)
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
network.update_dna(px=0, py=0, pz=0)
network.update_dea(f=0, q=0.1)

a = network.add_node(x=0, y=0, z=0, is_anchor=True)
b = network.add_node(x=10, y=0, z=10, is_anchor=True)
c = network.add_node(x=10, y=10, z=0, is_anchor=True)
d = network.add_node(x=0, y=10, z=10, is_anchor=True)

e = network.add_node(x=5, y=5, z=0, pz=-3)

network.add_edge(a, e, q=random.uniform(0, 1))
network.add_edge(b, e, q=random.uniform(0, 1))
network.add_edge(c, e, q=random.uniform(0, 1))
network.add_edge(d, e, q=random.uniform(0, 1))


# ==============================================================================
# numerical data
# ==============================================================================

n = network.number_of_nodes()

node_index = {node: index for index, node in enumerate(network.nodes())}

fixed = list(network.nodes_where({'is_anchor': True}))
free = list(network.nodes_where({'is_anchor': False}))
fixed[:] = [node_index[node] for node in fixed]
free[:] = [node_index[node] for node in free]

edges = [(node_index[u], node_index[v]) for u, v in network.edges()]

X = network.nodes_attributes('xyz')
R = network.nodes_attributes(['rx', 'ry', 'rz'])
P = network.nodes_attributes(['px', 'py', 'pz'])
Q = network.edges_attribute('q')


# ==============================================================================
# clear the Rhino model
# ==============================================================================
# and define the drawing helpers/parameters

compas_rhino.clear()
layer = "DF21::C1::FormFinding"
artist = NetworkArtist(network, layer=layer)


# ==============================================================================
# compute equilibrium > NEW (callback)
# ==============================================================================

# calling dynamic relaxation function
X, Q, F, L, R = dr(X, edges, fixed, P, Q, callback=callback_visualize)

# update network
update_network()


# ==============================================================================
# visualization
# ==============================================================================

compas_rhino.clear()
artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
artist.draw_edges()

draw_reactions(network, layer, (0, 255, 0))
draw_residuals(network, layer, (0, 255, 255), 0.01)
draw_loads(network, layer, (255, 0, 0))
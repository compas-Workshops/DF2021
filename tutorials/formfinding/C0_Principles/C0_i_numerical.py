from compas.geometry import add_vectors, subtract_vectors, length_vector
from compas.datastructures import Network

import compas_rhino
from compas_rhino.artists import NetworkArtist


# ==============================================================================
# helpers > NEW (numerical equilibrium functions)
# ==============================================================================

def update_R():
    for i in range(n):
        R[i] = [0, 0, 0]
        a = X[i]
        for j in i_nbrs[i]:
            b = X[j]
            q = ij_fd[i, j]
            R[i][0] += q * (b[0] - a[0])
            R[i][1] += q * (b[1] - a[1])
            R[i][2] += q * (b[2] - a[2])

def update_X():
    for i in range(n):
        if i in fixed:
            continue
        X[i][0] += 0.5 * R[i][0]
        X[i][1] += 0.5 * R[i][1]
        X[i][2] += 0.5 * R[i][2]


def update_network():
    for node in network.nodes():
        index = node_index[node]
        network.node_attributes(node, ['x', 'y', 'z'], X[index])
        network.node_attributes(node, ['rx', 'ry', 'rz'], R[index])


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
network.update_dea(q=0.1)

a = network.add_node(x=0, y=0, z=0, is_anchor=True)
b = network.add_node(x=10, y=0, z=10, is_anchor=True)
c = network.add_node(x=10, y=10, z=0, is_anchor=True)
d = network.add_node(x=0, y=10, z=10, is_anchor=True)

e = network.add_node(x=5, y=5, z=0)

network.add_edge(a, e)
network.add_edge(b, e)
network.add_edge(c, e)
network.add_edge(d, e)

fixed = list(network.nodes_where({'is_anchor': True}))
free = list(network.nodes_where({'is_anchor': False}))


# ==============================================================================
# numerical data > NEW
# ==============================================================================

n = network.number_of_nodes()

# mapping of node keys to contiguous node indices
node_index = {node: index for index, node in enumerate(network.nodes())}

# indices of fixed and free nodes
fixed[:] = [node_index[node] for node in fixed]
free[:] = [node_index[node] for node in free]

X = network.nodes_attributes('xyz')
R = network.nodes_attributes(['rx', 'ry', 'rz'])

# mapping of node index to indices of all its neighbors
i_nbrs = {node_index[node]: [node_index[nbr] for nbr in network.neighbors(node)] for node in network.nodes()}

# mapping of edge tuple to force densities
ij_fd = {}
for u, v in network.edges():
    i = node_index[u]
    j = node_index[v]
    fd = network.edge_attribute((u, v), 'q')
    ij_fd[i, j] = fd
    ij_fd[j, i] = fd


# ==============================================================================
# clear the Rhino model
# ==============================================================================
# and define the drawing helpers/parameters

compas_rhino.clear()
layer = "DF21::C0::FormFinding"
artist = NetworkArtist(network, layer=layer)


# ==============================================================================
# iterative equilibrium > NEW (numerical helper functions)
# ==============================================================================
# define maximum iterations and tolerance for residuals
tol = 0.01
kmax = 100

# compute the residual forces in the original geometry
update_R()

for k in range(kmax):
    if k % 10 == 0:
        if sum(length_vector(R[i]) for i in free) < tol:
            break
    
    # update nested lists of coordinates and residuals
    update_X()
    update_R()

# update network
update_network()


# ==============================================================================
# visualization
# ==============================================================================

compas_rhino.clear()
artist.draw_nodes(color={node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})})
artist.draw_edges()

draw_reactions(network, layer, (0, 255, 0))
draw_residuals(network, layer, (0, 255, 255), tol)
draw_loads(network, layer, (255, 0, 0))
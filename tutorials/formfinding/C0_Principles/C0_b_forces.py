from compas.geometry import add_vectors, subtract_vectors
from compas.geometry import normalize_vector, scale_vector
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
# visualize the geometry
# ==============================================================================

# clear the Rhino model
compas_rhino.clear()

artist = NetworkArtist(network)
artist.layer = "DF21::C0::FormFinding"

# color the anchors red
node_color = {node: (255, 0, 0) for node in network.nodes_where({'is_anchor': True})}

artist.draw_nodes(color=node_color)
artist.draw_edges()


# ==============================================================================
# visualize the forces > NEW ONLY PLUS IMPORTS
# ==============================================================================

lines = []
for node in network.nodes():
    a = network.node_attributes(node, 'xyz')

    for nbr in network.neighbors(node):
        b = network.node_attributes(nbr, 'xyz')

        edge = node, nbr
        if not network.has_edge(*edge):
            edge = nbr, node

        force = network.edge_attribute(edge, 'f')
        direction = normalize_vector(subtract_vectors(b, a))
        vector = scale_vector(direction, force)
        lines.append({
            'start': a,
            'end': add_vectors(a, vector),
            'arrow': 'end',
            'color': (255, 0, 0)})

compas_rhino.draw_lines(lines, layer=artist.layer)
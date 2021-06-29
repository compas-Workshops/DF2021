import compas_rhino

from compas.geometry import Pointcloud, KDTree, Cylinder
from compas.datastructures import Network
from compas.utilities import pairwise
from compas_rhino.artists import NetworkArtist
from compas_rhino.artists import CylinderArtist

compas_rhino.clear()

network = Network()

cloud = Pointcloud.from_bounds(10, 5, 3, 200)
tree = KDTree(cloud)

for point in cloud:
    network.add_node(x=point[0], y=point[1], z=point[2])

for node in network.nodes():
    point = network.node_coordinates(node)
    for nbr in tree.nearest_neighbors(point, 4, distance_sort=True):
        if not network.has_edge(node, nbr[1], directed=False):
            network.add_edge(node, nbr[1])

start = network.get_any_node()
goal = network.get_any_node()
path = network.shortest_path(start, goal)
edges = [(u, v) if network.has_edge(u, v) else (v, u) for u, v in pairwise(path)]

artist = NetworkArtist(network)
artist.draw_nodes(color={start: (255, 0, 0), goal: (0, 0,  255)})
artist.draw_edges(color={edge: (0, 255, 0) for edge in edges})

for u, v in edges:
    o = network.edge_midpoint(u, v)
    n = network.edge_direction(u, v)
    h = network.edge_length(u, v)

    cylinder = Cylinder([(o, n), 0.02], h)
    artist = CylinderArtist(cylinder, color=(0, 255, 0))
    artist.draw(show_vertices=False)

from compas.datastructures import Network

net = Network()

a = net.add_node(x=0, y=0)
b = net.add_node(x=1, y=0)

ab = net.add_edge(a, b)

print(a)
print(b)

print(ab)

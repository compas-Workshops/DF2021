from compas.datastructures import Network

net = Network()

a = net.add_node('a')
b = net.add_node('b')

ab = net.add_edge(a, b)

print(a)
print(b)

print(ab)

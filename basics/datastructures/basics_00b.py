from compas.datastructures import Mesh

mesh = Mesh()

a = mesh.add_vertex(x=0, y=0)
b = mesh.add_vertex(x=1, y=0)
c = mesh.add_vertex(x=1, y=1)

abc = mesh.add_face([a, b, c])

print(a)
print(b)
print(c)

print(abc)

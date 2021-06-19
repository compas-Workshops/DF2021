import os
from compas.datastructures import Mesh
from compas_rhino.geometry import RhinoMesh
from compas_rhino.artists import MeshArtist
import compas_rhino
import rhinoscriptsyntax as rs
#
guid = compas_rhino.select_mesh(message='Select Mesh')
compas_rhino.rs.HideObjects(guid)
rhinomesh = RhinoMesh.from_guid(guid)
mesh = rhinomesh.to_compas(cls=Mesh)

#guids = compas_rhino.select_lines(message='Select Lines')
#compas_rhino.rs.HideObjects(guids)
#lines = compas_rhino.get_line_coordinates(guids)s
#mesh = Mesh.from_lines(lines, delete_boundary_face=True)
#
#
HERE = os.path.dirname(__file__)
name = "staircase_2"
FILE_O = os.path.join(HERE, 'data', name+'.json')


# =============== delete duplicated points ============
from compas.utilities import geometric_key
key_gkey = {key: geometric_key(mesh.vertex_attributes(key, 'xyz'), precision=10) for key in mesh.vertices()}
gkey_key = {gkey: key for key, gkey in iter(key_gkey.items())}

print(len(key_gkey.keys()))
print(len(gkey_key.keys()))

vertices = []
n_key_o_key = {}
for i, (vertex, key) in enumerate(gkey_key.items()):
    xyz_string = vertex.split(",")
#    x = round(float(xyz_string[0]),2)
#    y = round(float(xyz_string[1]),2)
#    z = round(float(xyz_string[2]),2)
    x = float(xyz_string[0])
    y = float(xyz_string[1])
    z = float(xyz_string[2])
    vertices.append([x, y, z])
    n_key_o_key[key] = [i, key]


for key in mesh.vertices():
    test = gkey_key[key_gkey[key]]
    if test != key:
       n_key_o_key[test].append(key)
print(n_key_o_key)

o_key_index = {key: key for key in mesh.vertices()}

for (n_key, o_key) in n_key_o_key.items():
    index = o_key[0]
    for key in o_key[1:]:
        o_key_index[key] = index

print(o_key_index)
faces = []
for fkey in mesh.faces():
    f_vkeys = mesh.face_vertices(fkey)
    new_f_vkeys = [o_key_index[key] for key in f_vkeys]
    faces.append(new_f_vkeys)

mesh = Mesh.from_vertices_and_faces(vertices, faces)
mesh.to_json(FILE_O)

#xyzs = []
#for vkey in mesh.vertices():
#    xyzs.append(mesh.vertex_coordinates(vkey))
#
#
#key_key_dict = {}
#
#gkey_key_dict = mesh.gkey_key()
#print(gkey_key_dict)
#for xyz in xyzs:
#    vkey = gkey_key_dict[geometric_key(xyz)]
#    anchors.append(vkey)
#    mesh.vertex_attribute(vkey, 'is_anchor', True)
    
    
print((list(mesh.faces())))
print([mesh.face_vertices(fkey) for fkey in mesh.faces()])
print(len(list(mesh.vertices())))

# add text
centroid = mesh.centroid()

#pt = rs.AddPoint(*centroid)
rs.AddTextDot(name, (centroid[0], centroid[1], centroid[2]))

artist = MeshArtist(mesh, layer="Seg::" + name)
artist.clear_layer()
artist.draw_faces(join_faces=True)
#artist.draw_facenormals()
artist.redraw()
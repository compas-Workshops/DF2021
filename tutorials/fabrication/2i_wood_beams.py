# ==============================================================================
# Import
# ==============================================================================
import os
import random

from compas.geometry import Polygon, Polyline, Point, Frame, Transformation
from compas.geometry import offset_polyline
from compas.geometry import cross_vectors, dot_vectors
from compas.geometry import normalize_vector, scale_vector
from compas.geometry import add_vectors, subtract_vectors
from compas.datastructures import Mesh
from compas.datastructures import mesh_flip_cycles
from compas.utilities import flatten
from compas.utilities import pairwise
from compas.rpc import Proxy

from compas_rhino.artists import MeshArtist
from compas_rhino.artists import PolygonArtist, PointArtist

# ==============================================================================
# Initialise
# ==============================================================================
HERE = os.path.dirname(__file__)
FILE_I = os.path.join(HERE, 'bridge_fofin_reactions.json')

mesh = Mesh.from_json(FILE_I)

proxy = Proxy('compas.geometry')
bestfit = proxy.bestfit_frame_numpy

bdr_beam_dis = 0.1 # offset distance, beam height
beam_height = 0.1

for start in [(1332, 493), (948, 576), (638, 842)]:
    # find the edge loop
    loop = mesh.edge_loop(start)
    loop_vertices = list(flatten(loop)) # not chained
    seen = set()
    loop_vertices = [x for x in loop_vertices if x not in seen and not seen.add(x)]
    points = []

    # move the points along the reaction force direction to generate the beams
    for vkey in loop_vertices:
        rx, ry, rz = mesh.vertex_attributes(vkey, ('rx', 'ry', 'rz'))
        react_dir = scale_vector(normalize_vector([rx, ry, rz]), -bdr_beam_dis)
        xyz = mesh.vertex_coordinates(vkey)
        beam_pt = add_vectors(xyz, react_dir)
        points.append(beam_pt)

    # points for the hooks
    hooks = []
    for i, (u, v) in enumerate(pairwise(points)):
        if i == 0 or i == len(points) - 2 or i % 5 == 1:
            hook_pt = [sum(x) / len(x) for x in zip(u, v)]
            hook_pt = Point(*hook_pt)
            hooks.append(hook_pt)
            point_artist = PointArtist(hook_pt, color=(0, 255, 0), layer="DF2021:: Beam_hooks")
            point_artist.draw()

    polyline = Polyline(points)
    local_frame = bestfit(polyline)

    xaxis_local = local_frame[1]
    yaxis_local = local_frame[2]
    zaxis_local = normalize_vector(cross_vectors(xaxis_local, yaxis_local))

    # check polyline direction
    polyline_vec = subtract_vectors(points[-1], points[0])
    cross_vec = cross_vectors(polyline_vec, zaxis_local)
    if dot_vectors(cross_vec, [0, 0, 1]) <0:
        zaxis_local = scale_vector(zaxis_local, -1)
    print(zaxis_local)

    polyline_o = Polyline(offset_polyline(polyline, -beam_height, zaxis_local))

    # 2d data
    world = Frame.worldXY()
    T = Transformation.from_frame_to_frame(Frame(*local_frame), world)

    polyline_i_T = polyline.transformed(T)
    polyline_o_T = polyline_o.transformed(T)

    polygon = Polygon(polyline_i_T.points + polyline_o_T.points[::-1])
    polygonartist = PolygonArtist(polygon, layer="DF2021:: Beam2d")
    polygonartist.draw(show_points=False, show_edges=True, show_face=False)
    
    for pt in hooks:
        hook_T = pt.transformed(T)
        point_artist = PointArtist(hook_T, color=(0, 255, 0), layer="DF2021:: Beam_hooks_xy")
        point_artist.draw()
    
    # generate 2d mesh
    vertices = polyline.points + polyline_o.points 
    faces = []
    length = len(polyline.points)
    for i in range(length - 1) :
        faces.append([i, i + 1, length + i + 1, length + i])
    beam_2d = Mesh.from_vertices_and_faces(vertices, faces)

    # copy
    beam_side1 = beam_2d.copy()
    beam_side2 = beam_2d.copy()

    thickness = 0.05

    for vkey in beam_2d.vertices():
        xyz = beam_2d.vertex_coordinates(vkey)

        up = scale_vector(zaxis_local, 0.5 * thickness)
        down = scale_vector(zaxis_local, -0.5 * thickness)

        beam_side1.vertex_attributes(vkey, 'xyz', add_vectors(xyz, up))
        beam_side2.vertex_attributes(vkey, 'xyz', add_vectors(xyz, down))

    mesh_flip_cycles(beam_side2)

    beam_3d = beam_side1.copy()
    max_int_key = len(list(beam_3d.vertices()))
    max_int_fkey = len(list(beam_3d.faces()))

    for key, attr in beam_side2.vertices(True):
        beam_3d.add_vertex(key=key + max_int_key, **attr)

    for fkey in beam_side2.faces():
        vertices = beam_side2.face_vertices(fkey)
        vertices = [key + max_int_key for key in vertices]
        beam_3d.add_face(vertices)

    boundary = beam_side2.vertices_on_boundary()
    boundary.append(boundary[0])

    for a, b in pairwise(boundary):
        beam_3d.add_face([b, a, a + max_int_key, b + max_int_key])

    beamartist = MeshArtist(beam_3d, layer="DF2021:: Beam")
    # beamartist.clear_layer()
    beamartist.draw_faces(join_faces=True)
    beamartist.draw_edges()

# ==============================================================================
# Visualization
# ==============================================================================
edgecolor = {}
for (u, v) in loop:
    edgecolor[(u,v)] = (0, 255, 0)
    edgecolor[(v, u)] = (0, 255, 0)
    
artist = MeshArtist(mesh, layer="DF2021:: Base")
artist.clear_layer()
artist.draw_faces(faces=list(mesh.faces_where({'is_knit': True})),join_faces=True)
artist.draw_edges(color=edgecolor)
#artist.draw_vertexlabels()
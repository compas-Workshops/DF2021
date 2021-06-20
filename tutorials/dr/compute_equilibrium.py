import os

from compas.utilities import Colormap

from compas_fofin.datastructures import Cablenet
#from compas_fofin.fofin import update_xyz_numpy

#from compas_plotters import MeshPlotter
from compas_fofin.rhino import CablenetArtist
#from compas_rhino.artists import MeshArtist as CablenetArtist

# ==============================================================================
# Create a cablenet
# ==============================================================================

HERE = os.path.dirname(__file__)
HERE =  os.path.join(HERE, '..', 'fabrication')
FILE_I = os.path.join(HERE, 'bridge_fofin.json')
FILE_O = os.path.join(HERE, 'bridge_fofin_reactions.json')
FILE_P = os.path.join(HERE, 'hypar.png')

cablenet = Cablenet.from_json(FILE_I)

cablenet.attributes['density'] = 0.0




# ==============================================================================
# Identify anchors
# ==============================================================================
st_edges = [(638,842), (948, 576), (1332, 493), (567, 593), (30, 1001)]
for st_edge in st_edges:
    cables = cablenet.get_continuous_edges(st_edge)
    keys = list(set([key for cable in cables for key in cable]))
    print(keys)
    cablenet.vertices_attribute('is_anchor', True, keys=keys)

cablenet.vertices_attribute('is_anchor', True, keys=list(cablenet.vertices_on_boundary()))


# ==============================================================================
# Compute equilibrium
# ==============================================================================
from compas.rpc import Proxy
proxy = Proxy('compas_fofin.fofin')
fofin = proxy.update_xyz_proxy
cablenetdata = fofin(cablenet.to_data())
cablenet = Cablenet.from_data(cablenetdata)

#update_xyz_numpy(cablenet)

# ==============================================================================
# Visualize
# ==============================================================================

heights = cablenet.vertices_attribute('z')
cmap = Colormap(heights, 'black')
vertexcolor = {key: cmap(z) for key, z in zip(cablenet.vertices(), heights)}

forces = cablenet.edges_attribute('f')
cmap = Colormap(forces, 'rgb')
edgecolor = {key: cmap(f) for key, f in zip(cablenet.edges(), forces)}

artist = CablenetArtist(cablenet)
artist.clear_layer()
artist.draw_vertices(color={vertex: (255, 0, 0) for vertex in cablenet.vertices_where({'is_anchor': True})})
artist.draw_edges()
artist.draw_faces()
#artist.draw_vertexlabels()

artist.draw()

#plotter = MeshPlotter(cablenet, figsize=(16, 9))
#plotter.draw_vertices(facecolor=vertexcolor, radius=0.05)
#plotter.draw_edges(width=2.0, color=edgecolor)
#
#plotter.save(FILE_P, dpi=150)
#plotter.show()

# ==============================================================================
# Export
# ==============================================================================

cablenet.to_json(FILE_O)

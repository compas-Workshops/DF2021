import os

from compas_rhino.geometry import RhinoSurface
from compas.datastructures import Mesh

import compas_rhino
from compas_rhino.artists import MeshArtist


# ==============================================================================
# Helpers
# ==============================================================================

def mesh_from_rhinosurface():
    """Make a mesh from a Rhino surface.
    """
    guid = compas_rhino.select_surface(message='select one polysurface')
    surface = RhinoSurface.from_guid(guid)
    mesh = surface.to_compas(Mesh)
    return mesh

# ==============================================================================
# Paths
# ==============================================================================

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, '..', 'data'))
FILE_O = os.path.join(DATA, 'cablenmesh_import.json')

# ==============================================================================
# Import from Rhino
# ==============================================================================

mesh = mesh_from_rhinosurface()

# ==============================================================================
#  Visualize
# ==============================================================================

artist = MeshArtist(mesh, layer="DF21_C2::01_Geometry Import::Mesh")
artist.clear_layer()
artist.draw_vertexlabels()
artist.draw_facelabels()
artist.draw()

# ==============================================================================
# Export
# ==============================================================================

mesh.to_json(FILE_O)
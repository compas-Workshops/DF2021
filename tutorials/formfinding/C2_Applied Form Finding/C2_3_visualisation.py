import compas_rhino
from compas.geometry import length_vector, add_vectors
from compas.geometry import scale_vector
from compas.utilities import i_to_red


# ==============================================================================
# Visualization Helpers
# ==============================================================================

def draw_reactions(mesh, baselayer, color=(0, 255, 0), scale=1):
    """Visualise the reaction forces in rhino as green arrows.
    """
    lines = []
    for key in mesh.vertices_where({'is_anchor': True}):
        start = mesh.vertex_attributes(key, 'xyz')
        residual = mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
        end = add_vectors(start, scale_vector(residual, -scale))
        lines.append({
            'start': start,
            'end': end,
            'name': "{}.reaction.{}".format(key, round(length_vector(residual), 3)),  # noqa: E501
            'arrow': 'end',
            'color': color
        })

    layer = baselayer+"::Reactions"
    compas_rhino.draw_lines(lines, layer=layer, clear=True)


def draw_residuals(mesh, baselayer, color=(0, 255, 255), tol=0.001, scale=1):
    """Visualise the residual forces in rhino as cyan arrows.
    """
    lines = []
    for key in mesh.vertices_where({'is_anchor': False}):
        start = mesh.vertex_attributes(key, 'xyz')
        residual = mesh.vertex_attributes(key, ['rx', 'ry', 'rz'])
        end = add_vectors(start, scale_vector(residual, scale))
        if length_vector(residual) < tol:
            continue
        lines.append({
            'start': start,
            'end': end,
            'name': "{}.residual.{}".format(key, round(length_vector(residual), 3)),  # noqa: E501
            'arrow': 'end',
            'color': color})

    layer = baselayer+"::Residuals"
    compas_rhino.draw_lines(lines, layer=layer, clear=True)


def draw_forces(mesh, baselayer, color=(255, 0, 0), scale=0.1, tol=0.001):
    """Visualise the edge forces in rhino as red-gradient pipes.
    """
    f_max = []
    for edge in mesh.edges():
        f = mesh.edge_attribute(edge, 'f')
        f_max.append(abs(f))
    f_max = max(f_max)

    cylinders = []
    for edge in mesh.edges():
        f = mesh.edge_attribute(edge, 'f')
        radius = scale * f
        if radius < tol:
            continue
        start_end = mesh.edge_coordinates(*edge)

        cylinders.append({
            'start': start_end[0],
            'end': start_end[1],
            'name': "{}.force.{}".format(edge, round(f, 3)),
            'radius': radius,
            'color': i_to_red(abs(f)/f_max)})

    layer = baselayer+"::Forces"
    compas_rhino.draw_cylinders(cylinders, layer=layer, clear=True)


def draw_loads(mesh, baselayer, color=(0, 255, 0), scale=1):
    """Visualise the external loads in rhino as green arrows.
    """
    lines = []
    for key in mesh.vertices_where({'is_anchor': False}):
        start = mesh.vertex_attributes(key, 'xyz')
        load = mesh.vertex_attributes(key, ['px', 'py', 'pz'])
        end = add_vectors(start, scale_vector(load, scale))
        lines.append({
            'start': start,
            'end': end,
            'name': "{}.load.{}".format(key, round(length_vector(load), 3)),
            'arrow': 'end',
            'color': color})

    layer = baselayer+"::Loads"
    compas_rhino.draw_lines(lines, layer=layer, clear=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass

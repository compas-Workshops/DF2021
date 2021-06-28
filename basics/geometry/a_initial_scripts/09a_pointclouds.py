import random
import time

from compas.geometry import Pointcloud
from compas.geometry import scale_vector, normalize_vector
from compas.geometry import Translation
from compas.utilities import i_to_rgb

import compas_rhino
from compas_rhino.artists import PointArtist


def random_vector():
    return scale_vector(
        normalize_vector([
            random.choice([-1, +1]) * random.random(),
            random.choice([-1, +1]) * random.random(),
            random.choice([-1, +1]) * random.random(),
        ]), random.random())


pcl = Pointcloud.from_bounds(10, 5, 3, 100)
colors = [i_to_rgb(random.random()) for _ in pcl]
transformations = [Translation.from_vector(random_vector()) for _ in pcl]

PointArtist.draw_collection(
    pcl,
    colors=colors,
    layer="ITA20::PCL",
    clear=True)

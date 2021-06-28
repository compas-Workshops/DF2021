from random import random
from compas.geometry import Pointcloud
from compas.geometry import Sphere
from compas_view2.app import App

viewer = App()

for point in Pointcloud.from_bounds(8, 5, 3, 17):
    radius = random()
    sphere = Sphere(point, radius)
    viewer.add(sphere, facecolor=(1, radius, radius), linecolor=(radius, 1, radius))

viewer.show()

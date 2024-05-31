import numpy as np
import cv2

from rtx_engine.camera.perspective_camera import Camera
from rtx_engine.helper import *
from rtx_engine.world import World
from rtx_engine.material import Material
from rtx_engine.objects.plane import Plane
from rtx_engine.objects.sphere import Sphere

# setting up the world
world = World(
    ambient = 0.3,
    background = cv2.imread('assets/background.jpg')
)

# adding a sphere at (75, 0, 0) with radius 50 units
world.addObject(
    Sphere(
        np.array([75, 0, -50]),50,
        Material(
            color        = np.array([1,0,1]),
            specularCoef = 40,
            reflective   = 0.3,
            mapping      = cv2.imread('assets/texture.jpg')
        )
    )
)
world.addObject(
    Sphere(
        np.array([120, -50, 10]), 25,
        Material(
            color        = np.array([1,0,1]),
            specularCoef = 100,
            reflective   = 0,
            mapping      = cv2.imread('assets/earth.jpg')
        )
    )
)

# adding a plane at [0, 0, -100] with normal vector [1, 0, 0.01]
world.addObject(
    Plane(
        np.array([0,0,-100]),
        norm(np.array([1,0,0.01])),
        Material(
            color        = np.array([45, 108, 99]),
            specularCoef = 100,
            reflective   = 0.5,
            mapping      = None
        )
    )
)

# adding light source
world.addLight(100, -100, 100)


# setting up camera
world.setCamera(
    Camera(
        np.array([0,0,200]),
        norm(np.array([0,0,-1])),
        400,300
    )
)

# rendering and displaying img
img = world.render()

# using cv2 to display np image
cv2.imshow('output', img)

cv2.waitKey(0)

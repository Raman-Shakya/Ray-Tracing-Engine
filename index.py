import numpy as np
import math
import cv2
from camera import *

class World:
    def __init__(self):
        self.elements = []
        self.lights   = []
        self.camera   = 0
        self.ambient  = 0.3
        self.background = None
        self.background = cv2.imread('background.jpg')

    def addLight(self, x,y,z, color=np.array([255,255,255])):
        self.lights.append(
            Light(
                np.array([x,y,z]),
                color
            )
        )

class Material:
    def __init__(self, color=np.array([255,255,255]), specularCoef=float('inf'), reflective=0.1, mapping=None):
        self.color        = color
        self.specularCoef = specularCoef
        self.reflective   = reflective
        self.mapping      = mapping


class Light:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Sphere:
    def __init__(self, pos, raidus, material):
        self.pos    = pos
        self.radius = raidus
        self.material = material

    # ray sphere collision
    def getDist(self, origin, dir): # return format -> length, point of intersection, normal (direction)
        t = dot(dir, self.pos-origin)
        y = mag(self.pos - origin - dir*t)

        if y <= self.radius:
            x = (self.radius**2-y**2)**.5
            length = t-x
            if length<=0.1:
                length += x+x
                if length<=0.1:
                    return float('inf'), None, None # sphere is behind the ray (miss)
            
            intersection = origin + dir*length
            normal       = intersection - self.pos

            return length, intersection, norm(normal) # hit
            
        return float('inf'), None, None # miss

class Plane:
    def __init__(self, anchor, direction, material):
        self.anchor = anchor
        self.normal = direction
        self.material = material
    
    # ray plane intersection
    def getDist(self, origin, dir): # return format -> length, point of intersection, normal (direction)
        rslope = dot(dir, self.normal)
        if rslope==0: return float('inf'), None, None # if ray is parallel to the plane

        t = 1/rslope*(dot(self.anchor,self.normal)-dot(origin, self.normal))
        if t<=.1:
            return float('inf'), None, None # miss
        
        return t, origin + dir*t, self.normal
        


# helper function
def mag(ar):
    return (ar[0]**2+ar[1]**2+ar[2]**2)**.5
def dot(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

# setting up the world
world = World()

world.elements.append(
    Sphere(
        np.array([75,0,0]),50,
        Material(
            color        = np.array([1,0,1]),
            specularCoef = 100,
            reflective   = 0,
            mapping      = cv2.imread('earth.jpg')
        )
    )
)
# world.elements.append(
#     Plane(
#         np.array([0,0,-100]),
#         norm(np.array([1,0,0.01])),
#         Material(
#             color        = np.array([0,0,0]),
#             specularCoef = float('inf'),
#             reflective   = 0.2,
#             mapping      = cv2.imread('earth.jpg')
#         )
#     )
# )

# world.addSphere(50,0,0,50, np.array([0,0,1]))
# world.addPlane(np.array([0, 50, 0]), np.array([0,-1,0]), np.array([0,0,0]))
world.addLight(-100,-20,50)

# setting up camera
camera = Camera(
    np.array([0,0,200]),
    norm(np.array([0,0,-1])),
    400,300
)

# rendering and displaying img
img = camera.render(world)
# while True:
    
#     camera.dir = norm(-camera.pos)

#     img = camera.render(world)
#     cv2.imshow('output', img)


#     k = cv2.waitKey(0)
#     if k==ord('a'):
#         camera.pos[0]-=50
#     if k==ord('s'):
#         camera.pos[2]+=50
#     if k==ord('d'):
#         camera.pos[0]+=50
#     if k==ord('w'):
#         camera.pos[2]-=50
#     if k==ord('q'):
#         break


cv2.imshow('output', img)
# cv2.imwrite('filename.jpg', img)

cv2.waitKey(0)

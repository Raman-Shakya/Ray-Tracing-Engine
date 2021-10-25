import numpy as np
import math
import cv2
from camera import *

class World:
    def __init__(self):
        self.elements = []
        self.lights   = []
        self.camera   = 0
        
    def addSphere(self, x,y,z,r, color=np.array([0,0,0])):
        self.elements.append(
            Sphere(
                np.array([x,y,z]),
                r,
                color
            )
        )
    
    def addPlane(self, pos=np.array([0,0,0]), dir=np.array([0, 1, 0]), color=np.array([0,0,0])):
        self.elements.append(
            Plane(
                pos,
                dir,
                color
            )
        )

    def addLight(self, x,y,z, color=np.array([1,1,1])):
        self.lights.append(
            Light(
                np.array([x,y,z]),
                color
            )
        )
    
class Light:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color

class Sphere:
    def __init__(self, pos, raidus, color):
        self.pos    = pos
        self.radius = raidus
        self.color  = color

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
    def __init__(self, anchor, direction, color):
        self.anchor = anchor
        self.normal = direction
        self.color  = color
    
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
world.addSphere(0,0,0,50, np.array([1,0,0]))
world.addSphere(100,0,0,20, np.array([0,0,1]))
world.addPlane(np.array([0, 100, 0]), np.array([0,-1,0]), np.array([1,1,0]))
world.addLight(200,0,200)

# setting up camera
camera = Camera(
    np.array([0,0,200]),
    np.array([0,0,-1]),
    400, 300
)

# rendering and displaying img
img = camera.render(world)
# img = cv2.GaussianBlur(img,(3,3),cv2.BORDER_DEFAULT)

cv2.imshow('output', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
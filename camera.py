from cv2 import magnitude
import numpy as np
import math

class Camera:
    def __init__(self, pos, dir, width, height):
        self.pos = pos
        self.dir = dir
        self.width = width
        self.height = height

    def render(self, world):
        img = np.zeros((self.height, self.width, 3), np.float32)

        for i in range(self.height):
            for j in range(self.width):
                RayHead = np.array([j-self.width//2, i-self.height//2, 0])
                dir = norm( RayHead - self.pos ) # ray dir

                Dist, color, intersection, normal = self.getDist(world.elements, self.pos, dir)               
                skyColor = np.array([235, 206, 135])/255
                # skyColor = np.array([0,0,0])
                
                if Dist != float('inf'): # if ray hits an element
                    
                    backVect = world.lights[0].pos-intersection # vect to light
                    
                    backRayDist = self.getDist(world.elements, intersection, norm(backVect))[0]

                    ang = (math.pi - angle(normal, backVect))/math.pi/2
                    
                    col = color * ang

                    if backRayDist <= mag(backVect): # inshadow
                        col = np.array([0,0,0])
                        # col = col*0.8 + skyColor*0

                    
                    
                    img[i][j] = col
                else:
                    img[i][j] = skyColor

                


        return img

    def getDist(self, elements, pos, dir):
        minDist = float('inf')
        color   = np.array([0,0,0])
        normal  = None
        intersection = None

        for element in elements:

            temp = element.getDist(pos, dir)
            if  minDist > temp[0]:
                minDist = temp[0]
                normal  = temp[2]
                intersection = temp[1]

                color = element.color

        return minDist, color, intersection, normal

def norm(vector):
    mag = (vector[0]**2+vector[1]**2+vector[2]**2)**.5
    return vector/mag
def mag(ar):
    return (ar[0]**2+ar[1]**2+ar[2]**2)**.5
def dot(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def angle(vector1, vector2):
    return math.acos(dot(vector1, vector2)/(mag(vector1)*mag(vector2)))
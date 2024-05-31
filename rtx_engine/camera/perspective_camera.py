import numpy as np
import random
from rtx_engine.helper import *

class Camera:
    def __init__(self, pos, dir, width, height):
        self.pos = pos
        self.dir = dir
        self.width = width
        self.height = height
        self.upguide= np.array([0,-1,0])

    def render(self, world):
        img = np.zeros((self.height, self.width, 3), np.uint8)
        noSamples = 1

        right = norm(np.cross(self.upguide, self.dir))
        up    = norm(np.cross(right, self.dir))

        for i in range(self.height):
            for j in range(self.width):
                
                color = np.array([0,0,0], np.float32)
                for _ in range(noSamples):
                    RayHead = right*(j-self.width//2+random.random()) + up*(i-self.height//2+random.random())
                    dir = norm( RayHead - self.pos ) # ray dir

                    color+= self.getColor(dir, world, self.pos)
                img[i][j] = color/noSamples
        
        return img


    def getColor(self, dir, world, pos, depth=0):
        Dist, intersection, normal, element = self.getDist(world.elements, pos, dir)               

        if Dist != float('inf'): # if ray hits an element
            
            backVect = world.lights[0].pos-intersection # vect to light
            lightDist = mag(backVect)
            backVect = norm(backVect)

            backRayDist = self.getDist(world.elements, intersection, backVect)[0]

            tempL = dot(backVect, normal)
            if tempL<=0: tempL = 0
            reflectedRayDirLight = norm(backVect - 2*normal*tempL)
            reflectedRayDir = norm(dir - 2*normal*(dot(dir, normal)))

            if type(element.material.mapping)==np.ndarray:
                eColor = getUVcolor(element.material.mapping, -normal)
            else:
                eColor = element.material.color

            temp = dot(reflectedRayDirLight, dir)
            if temp<0: temp=0

            ambient = eColor*world.ambient
            diffuse = eColor*dot(backVect, normal)
            specular = world.lights[0].color*temp**element.material.specularCoef
          
            if backRayDist <= lightDist: # inshadow
                color = ambient
            else:
                color = diffuse+specular+ambient
                if color[0]>255:
                    color[0]=255
                if color[1]>255:
                    color[1]=255
                if color[2]>255:
                    color[2]=255

            # return color
            if depth==3: return color
            
            if element.material.reflective!=0:
                return (element.material.reflective*self.getColor(reflectedRayDir, world, intersection, depth+1) + (1-element.material.reflective)*color)
            else:
                return color

        if type(world.background)==np.ndarray:
            return getUVcolor(world.background, -dir)
        else:
            return np.array([0,0,0])

    def getDist(self, elements, pos, dir):
        minDist = float('inf')

        normal       = None
        intersection = None
        object       = None

        for element in elements:

            temp = element.getDist(pos, dir)
            if  minDist > temp[0]:
                minDist = temp[0]
                normal  = temp[2]
                intersection = temp[1]
                object  = element

        return minDist, intersection, normal, object
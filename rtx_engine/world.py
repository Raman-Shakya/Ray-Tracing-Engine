import cv2
import numpy as np
from .light.point_light import Light

class World:
    def __init__(self, ambient = 0.3, background = None):
        self.elements = []
        self.lights   = []
        self.camera   = 0
        self.ambient  = ambient
        self.background = background
    
    def addLight(self, x,y,z, color=np.array([255,255,255])):
        self.lights.append(
            Light(
                np.array([x,y,z]),
                color
            )
        )

    def render(self):
        if not self.camera:
            raise Exception('camera not set')
        if not self.lights:
            raise Exception('lights not set')
        
        return self.camera.render(self)
    
    def setCamera(self, camera):
        self.camera = camera

    def addObject(self, object):
        self.elements.append(object)
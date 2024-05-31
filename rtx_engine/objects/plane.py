from rtx_engine.helper import *

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
        
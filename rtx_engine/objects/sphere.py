from rtx_engine.helper import *

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

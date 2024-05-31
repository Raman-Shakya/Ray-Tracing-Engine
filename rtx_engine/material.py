import numpy as np

class Material:
    def __init__(self, color=np.array([255,255,255]), specularCoef=float('inf'), reflective=0.1, mapping=None):
        self.color        = color
        self.specularCoef = specularCoef
        self.reflective   = reflective
        self.mapping      = mapping
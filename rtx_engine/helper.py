import math

# helper functions
def norm(vector):
    mag = (vector[0]**2+vector[1]**2+vector[2]**2)**.5
    return vector/mag
def mag(ar):
    return (ar[0]**2+ar[1]**2+ar[2]**2)**.5
def dot(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]
def angle(vector1, vector2):
    return math.acos(dot(vector1, vector2)/(mag(vector1)*mag(vector2)))
def getUVcolor(img, dir):
    u = (0.5 + math.atan2(dir[0],dir[2])/(2*math.pi))*len(img[0])
    v = (0.5 - math.asin(dir[1])/math.pi)*len(img)
    return img[int(v),int(u)]
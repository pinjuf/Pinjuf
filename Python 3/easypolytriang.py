import numpy as np
from numpy import pi, e

def to_polar(x, y):
  r = np.sqrt(x**2+y**2)
  t = np.arctan2(y, x)
  return r, t
  
def to_cart(r, t):
    return np.cos(t)*r, np.sin(t)*r
    
def point_in_triangle(pt, v1, v2, v3):
    def area(p1, p2, p3):
        x1, y1, x2, y2, x3, y3 = *p1, *p2, *p3
        return abs((x1*((y2-y3))+x2*((y3-y1))+x3*((y1-y2)))/2)

    a  = area(v1, v2, v3)
    d1 = area(pt, v1, v2)
    d2 = area(pt, v2, v3)
    d3 = area(pt, v3, v1)
    if (d1+d2+d3)<=a:
        return True
    return False

def is_convex(p1, p2, p3):
    x1, y1 = p3
    x2, y2 = p2
    x3, y3 = p1
    
    _, t1 = to_polar(x1-x2, y1-y2)
    _, t2 = to_polar(x3-x2, y3-y2)
    t1 -= t2
    if 0<t1<np.pi:
        return True
    return False

def rotate(l, k):
    return l[k:] + l[:k]

def triangulate(inpoints):
    if inpoints[1]==inpoints[-1]: inpoints.pop(-1)
    while True:
        points = inpoints.copy()
        triangles = []
        
        a = rotate(points, -1)
        b = points.copy()
        c = rotate(points, 1)

        for n in range(len(points)-2):
            for ap, bp, cp, i in zip(a, b, c, range(len(points))):
                if is_convex(ap, bp, cp):
                    trigs = 0
                    triglist = []
                    for p in inpoints:
                        if point_in_triangle(p, ap, bp, cp):
                            triglist += [p]
                    for pt in ap, bp, cp:
                        try:
                            triglist.remove(pt)
                        except:
                            pass
                    
                    if triglist:
                        continue
                    triangles.append((ap, bp, cp))
                    del points[i]
                    
                    break

            points = rotate(points, 2)
        
            a = rotate(points, -1)
            b = points.copy()
            c = rotate(points, 1)

        if len(triangles)>=len(inpoints)-2:
            return triangles
        else:
            inpoints.reverse()

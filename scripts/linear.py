
import math

def dist(a, b):
    return math.sqrt(sum(map(lambda i,j: (i-j)*(i-j), a, b)))

def magnitude( a ):
    x, y = a
    return math.sqrt( x*x + y*y )

def scalar_product( a, b ):
    ax, ay = a
    bx, by = b
    return ax*bx+ay*by

def cross_product(a, b, c):
    """Cross product AB x AC"""
    ax, ay = a
    bx, by = b
    cx, cy = c
    return (bx-ax) * (cy-ay) - (by-ay) * (cx-ax)

def vector_add( a, b ):
    ax, ay = a
    bx, by = b
    return (ax+bx, ay+by)

def vector_sub( a, b ):
    ax, ay = a
    bx, by = b
    return (ax-bx, ay-by)

def scalar_mul( s, a ):
    x, y = a
    return (s*x, s*y)

def normalize( a ):
    x, y = a
    d = math.sqrt(x*x+y*y)
    return (x/d, y/d)

def interpolate( a, b, frac ):
    ax, ay = a
    bx, by = b
    return ( bx*frac+ax*(1-frac), by*frac+ay*(1-frac) )

def segment_intersection( s1, s2 ):
    a, b = s1
    c, d = s2
    cross1 = cross_product(a, b, c)
    cross2 = cross_product(a, d, b)

    cross3 = cross_product(c, d, a)
    cross4 = cross_product(c, b, d)

    interpol = 0
    if cross1+cross2 != 0:
        interpol = cross1/(cross1+cross2)

    if (cross1 == 0 or cross2 == 0 or ( cross1 > 0 ) == ( cross2 > 0)) and \
       (cross3 == 0 or cross4 == 0 or ( cross3 > 0 ) == ( cross4 > 0)) :
        return interpolate(c, d, interpol)

    return None


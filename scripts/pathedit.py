
import itertools
from math import *
from linear import *

FLEX = 1j
epsilon = 1e-8

def full_indent(a, b, angle, context):
    indent = context['indent']
    return replace_line( a, b, (
        ( -indent, FLEX ),
    ) )

def two_notches(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    return replace_line( a, b, (
        (       0, FLEX  ),
        ( -indent, width ),
        (       0, FLEX  ),
        ( -indent, width ),
        (       0, FLEX      ),
    ) )


def sticky_outy_bits(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    return replace_line( a, b, (
        ( -indent, width ),
        (       0, width ),
        ( -indent, FLEX  ),
        (       0, width ),
        ( -indent, width ),
    ) )


def sticky_inny_bits(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    return replace_line( a, b, (
        (       0, width ),
        ( -indent, width ),
        (       0, FLEX  ),
        ( -indent, width ),
        (       0, width ),
    ) )


def start_bits(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    return replace_line( a, b, (
        ( -indent, width ),
        (       0, width ),
        ( -indent, FLEX  ),
    ) )


def end_bits(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    return replace_line( a, b, (
        ( -indent, FLEX  ),
        (       0, width ),
        ( -indent, width ),
    ) )


def start_corner(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    return replace_line( a, b, (
        (       0, width ),
        ( -indent, FLEX  ),
        (       0, 0     ),
    ) )


def end_corner(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    return replace_line( a, b, (
        (       0, 0     ),
        ( -indent, FLEX  ),
        (       0, width ),
    ) )


def cut_corners(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    if width*2 > dist(b,a):
        return full_indent(a, b, angle, context)

    return replace_line( a, b, (
        ( -indent, width ),
        (       0, FLEX  ),
        ( -indent, width ),
    ) )


def cut_corners_inverse(a, b, angle, context):

    width = context['width']
    indent = context['indent']

    if width*2 > dist(b,a):
        return identity(a, b, angle, context)

    return replace_line( a, b, (
        (       0, width ),
        ( -indent, FLEX  ),
        (       0, width ),
    ) )



def alt_corners_inverse(a, b, angle, context):

    width = context['alt']
    indent = context['indent']

    if width*2 > dist(b,a):
        return identity(a, b, angle, context)

    return replace_line( a, b, (
        (       0, width ),
        ( -indent, FLEX  ),
        (       0, width ),
    ) )



def uneven_corners(a, b, angle, context):

    left = context['left']
    right = context['right']
    indent = context['indent']
    if left + right > dist(b,a):
        return identity(a, b, angle, context)

    return replace_line( a, b, (
        (       0, left  ),
        ( -indent, FLEX  ),
        (       0, right ),
    ) )


def uneven_corners_reverse(a, b, angle, context):

    left = context['left']
    right = context['right']
    indent = context['indent']
    if left + right > dist(b,a):
        return identity(a, b, angle, context)

    return replace_line( a, b, (
        (       0, right ),
        ( -indent, FLEX  ),
        (       0, left  ),
    ) )

def identity(a, b, angle, context):
    return [a, b]


def replace_line(a, b, jag):
    
    edges = []
    x, y = a
    dx, dy = normalize(vector_sub(b, a))

    flex = sum(x.imag for _,x in jag)
    assert flex > 0
    flex_factor = (dist(b,a)-sum(x.real for _,x in jag)) / flex
    
    l = 0
    for indent, w in jag:
        edges.append( (x + dx*l + dy*indent, y + dy*l - dx*indent) )
        l += w.real + w.imag*flex_factor
        edges.append( (x + dx*l + dy*indent, y + dy*l - dx*indent) )

    if jag[0][0] == 0:
        edges[0] = a # keep float equality

    if jag[-1][0] == 0:
        edges[-1] = b # keep float equality

#    print(edges)
    return edges

def lengths_and_angles_to_polyline(lengths, arcs, start_at=(0,0), start_angle=0):
   v = start_at
   a = start_angle
   poly = [v]
   for l, da in itertools.zip_longest(lengths, arcs, fillvalue=0):
       v = vector_add(v, (l*cos(a), l*sin(a)))
       poly.append(v)
       a += da
   return poly


def purge_doubles(path):
    elems = []
    for a, b in zip(path, path[1:]+path[:1]):
        if a != b:
            elems.append(a)
    return elems

def cleanup(path):
    path = purge_doubles(path)
    elems = []
    for a, b, c in zip(path[-1:]+path[:-1], path, path[1:]+path[:1]):
        if abs(dist(a, c)+dist(b, c)-dist(a,b)) > epsilon and \
           abs(dist(c, a)+dist(b, a)-dist(c,b)) > epsilon:
            elems.append(b)
    return elems
        
shape_map = {
#    's' : jagged_shortedge,
#    'l' : jagged_longedge,
#    'S' : jagged_shortedge,
#    'L' : jagged_longedge,
    '2' : two_notches,
    'b' : sticky_outy_bits,
    'B' : sticky_inny_bits,
    'c' : cut_corners,
    'C' : cut_corners_inverse,
    'a' : alt_corners_inverse,
    'u' : uneven_corners,
    'U' : uneven_corners_reverse,
    'I' : identity,
    'f' : full_indent,
    's' : start_bits,
    'e' : end_bits,
    'S' : start_corner,
    'E' : end_corner,
}

def subdivide(shape, types, angles, context, shape_map=shape_map):

    if angles == None:
        angles = [None]*len(shape)

    edges = []
    for a, b, t, angle in zip(shape, shape[1:]+shape[:1], types, angles):
        edges.append( shape_map[t](a, b, angle, context))

    for i in range(len(edges)):
        orig = shape[i]
        a,b = edges[i-1][-2:]
        c,d = edges[i][:2]
        if b != orig or c != orig:
            p = segment_intersection( (a,b), (c,d) )
            if p != None:
                edges[i-1][-1] = p
                edges[i][0] = p
            elif b != orig and c != orig:
                p = segment_intersection( (b,orig), (c,d) )
                if p != None:
                    edges[i][0] = p
                else:
                    p = segment_intersection( (a,b), (orig,c) )
                    if p != None:
                        edges[i-1][-1] = p
                    else:
                        edges[i-1] += [orig]

    return cleanup( [ c for e in edges for c in e ] )

def polygon_crossproduct_sum(poly):
    total = 0
    a = poly[0]
    for i in range(len(poly)-2):
        b,c = poly[i+1:i+3]
        total += cross_product(a, b, c)
    return total

def is_inside_out(poly):
    return polygon_crossproduct_sum(poly) < 0

def flip_x(poly):
    return [ (-a, b) for a, b in reversed(poly) ]

def flip_y(poly):
    return [ (a, -b) for a, b in reversed(poly) ]

def grow(poly, width):

    points = []

    for a, b, c in zip(poly[-1:]+poly[:-1], poly, poly[1:]+poly[:1]):
        ax, ay = a
        bx, by = b
        cx, cy = c
        dx_ab, dy_ab = normalize( (by-ay, -(bx-ax)) )
        dx_bc, dy_bc = normalize( (cy-by, -(cx-bx)) )

        mid_x, mid_y = (dx_ab+dx_bc)/2., (dy_ab+dy_bc)/2.
        invdist2 = mid_x*mid_x + mid_y*mid_y

        points.append( (bx+width*mid_x/invdist2, by+width*mid_y/invdist2) )

    return points


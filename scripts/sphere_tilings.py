
import math

phi=(1+math.sqrt(5))/2;
cuberoot_penta=pow(118*phi+85+6*math.sqrt(1173*phi+729), 1/3);
cuberoot_quad=pow(24*math.sqrt(78)-181, 1/3);
cuberoot_tri=pow(6*math.sqrt(177)-71,1/3);

number_of_arcs = {
    'penta' : 30,
    'quad'  : 12,
    'tri'   : 6,
}

cosines = {
    'penta' : (1/6)*( (4*phi+1) + (12*phi+7)/cuberoot_penta - cuberoot_penta ),
    'quad'  : (1/6)*( 5 - 23/cuberoot_quad + cuberoot_quad ),
    'tri'   : (1/6)*( 1 - 11/cuberoot_tri + cuberoot_tri ),
}


def chiral_2_to_1_angles(kind='penta'):
    cos_A = cosines[ kind ]
    A = math.acos(cos_A)
    cos_alpha = 1/(1-cos_A)-1
    alpha = math.acos(cos_alpha)
    return (A, alpha)


def chiral_2_to_1(r, width, subdivisions=1, kind='penta'):
    assert kind in cosines
    assert subdivisions >= 1

    arc_count = number_of_arcs[ kind ]

    cos_A = cosines[ kind ]
    sin_A = math.sqrt( 1 - cos_A*cos_A )
    A = math.acos(cos_A)
    cos_alpha = 1/(1-cos_A)-1

    alpha = math.acos(cos_alpha)

    circle_arc = alpha/2/subdivisions
    dihedral = math.pi-circle_arc

    facet_r = r*math.tan(circle_arc/2)

    half_w = width/2

    shapes = []

    shapes.append( [
        ( -facet_r,                    -half_w ),
        ( -facet_r,                     half_w ),
        (  (half_w)* (cos_A - 1)/sin_A, half_w ),
        (  cos_A*facet_r -sin_A*half_w, facet_r*sin_A +half_w*cos_A ),
        (  cos_A*facet_r +sin_A*half_w, facet_r*sin_A -half_w*cos_A ),
        (  (half_w)* (cos_A + 1)/sin_A, half_w ),
        (  facet_r,                     half_w ),
        (  facet_r,                    -half_w )
    ] )

    shape_counts = [ arc_count * 2 ]

    if subdivisions > 1:
        shapes.append( [
            ( -facet_r, -half_w ),
            ( -facet_r,  half_w ),
            (  facet_r,  half_w ),
            (  facet_r, -half_w )
        ] )
        shape_counts.append( arc_count * 3 * (subdivisions-1) )

    return { 'dihedral' : dihedral, 'shapes' : shapes, 'shape_counts' : shape_counts }


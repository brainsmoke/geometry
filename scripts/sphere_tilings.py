
import math

def chiral_2_to_1(r, width, subdivisions=1, kind='penta'):
    assert kind in ('penta', 'tri')
    assert subdivisions >= 1

    phi=(1+math.sqrt(5))/2;
    cuberoot_penta=pow(118*phi+85+6*math.sqrt(1173*phi+729), 1/3);
    cuberoot_tri=pow(6*math.sqrt(177)-71,1/3);

    angles = {
        'penta' : (1/6)*( (4*phi+1) + (12*phi+7)/cuberoot_penta - cuberoot_penta ),
        'tri'   : (1/6)*( 1 - 11/cuberoot_tri + cuberoot_tri ),
    }

    arc_count = {
        'penta' : 30,
        'tri'   : 6,
    }

    cos_A = angles[ kind ]
    sin_A = math.sqrt( 1 - cos_A*cos_A )
    A = math.acos(cos_A)
    cos_alpha = 1/(1-cos_A)-1

    alpha = math.acos(cos_alpha)

    circle_arc = alpha/(4*subdivisions)
    dihedral = math.pi-circle_arc

    facet_r = r*math.tan(circle_arc)

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

    for _ in range(1, subdivisions):
        shapes.append( [
            ( -facet_r, -half_w ),
            ( -facet_r,  half_w ),
            (  facet_r,  half_w ),
            (  facet_r, -half_w )
        ] )

    return { 'dihedral' : dihedral, 'shapes' : shapes }


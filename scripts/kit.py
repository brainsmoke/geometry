import math, cmath, itertools

import sphere_tilings, pathedit, linear

def line_len(shape, ix):
    return linear.dist(shape[ix], shape[(ix+1)%len(shape)])

def tube(kind, r, width, height, subdivisions, thickness, notch_width):

    objects = []

    radius_tiling = sphere_tilings.chiral_2_to_1(r,           width, subdivisions, kind)
    top_tiling    = sphere_tilings.chiral_2_to_1(r-thickness, width, subdivisions, kind)
    bottom_tiling = sphere_tilings.chiral_2_to_1(r-height,    width, subdivisions, kind)

    top_joint = top_tiling['shapes'][0]
    bottom_joint = bottom_tiling['shapes'][0]
    radius_joint = radius_tiling['shapes'][0]

    dihedral = top_tiling['dihedral']
    ctx = {
        'width' : notch_width,
        'left'  : notch_width + line_len(radius_joint, 1) - line_len(top_joint, 1),
        'alt'   : notch_width + line_len(radius_joint, 1) - line_len(top_joint, 1),
        'right' : notch_width,
        'indent': thickness
    }

    c1, c2 = top_tiling['shape_counts'][0], bottom_tiling['shape_counts'][0]

    objects.append( ( [ pathedit.subdivide(top_joint, 'IccIccIc', None, ctx) ],
                      None,
                      f'top joint {c1}x') )

    objects.append( ( [ pathedit.flip_x(pathedit.subdivide(bottom_joint, 'IccIccIc', None, ctx)) ],
                      None,
                      f'bottom joint {c2}x' ) )

    radius_div_len, bottom_div_len = [], []

    if subdivisions > 1:
        radius_div = radius_tiling['shapes'][1]
        top_div = top_tiling['shapes'][1]
        bottom_div = bottom_tiling['shapes'][1]
        c3, c4 = top_tiling['shape_counts'][1], bottom_tiling['shape_counts'][1]
        objects.append( ( [ pathedit.subdivide(top_div, 'IcIc', None, ctx) ],
                          None,
                          f'top division {c3}x' ) )

        objects.append( ( [ pathedit.flip_x(pathedit.subdivide(bottom_div, 'IcIc', None, ctx)) ],
                          None,
                          f'bottom division {c4}x' ) )

        bottom_div_len = [ line_len(bottom_div, 1) ] * (subdivisions-1)
        radius_div_len = [ line_len(radius_div, 1) ] * (subdivisions-1)

    tau = math.tau
    angles_arc_small = [ dihedral - tau/2 ] * (subdivisions) + [ tau/4 ]*2 + \
                       [ tau/2 - dihedral ] * (subdivisions) + [ tau/4 ]

    angles_arc_large = [ dihedral - tau/2 ] * (subdivisions*2) + [ tau/4 ]*2 + \
                       [ tau/2 - dihedral ] * (subdivisions*2) + [ tau/4 ]

    lengths_arc_small = [
        line_len(bottom_joint, 2),
        ] + bottom_div_len + [
        line_len(bottom_joint, 1),
        height,
        line_len(radius_joint, 1),
        ] + radius_div_len + [
        line_len(radius_joint, 2),
    ]

    lengths_arc_large = [
        line_len(bottom_joint, 4),
        ] + bottom_div_len + [
        line_len(bottom_joint, 7),
        ] + bottom_div_len + [
        line_len(bottom_joint, 5),
        height,
        line_len(radius_joint, 5),
        ] + radius_div_len + [
        line_len(radius_joint, 7),
        ] + radius_div_len + [
        line_len(radius_joint, 4),
    ]

    notches_small = 'C'*(subdivisions  +1) + 'IU' + 'a'*(subdivisions  -1) + 'uI'
    notches_large = 'C'*(subdivisions*2+1) + 'IU' + 'a'*(subdivisions*2-1) + 'uI'

    small_side = pathedit.lengths_and_angles_to_polyline(lengths_arc_small, angles_arc_small)
    large_side = pathedit.lengths_and_angles_to_polyline(lengths_arc_large, angles_arc_large)

    objects.append( ( [ pathedit.subdivide(large_side, notches_large, None, ctx ) ],
                      None,
                      f'large side {c1}x' ) )

    objects.append( ( [ pathedit.subdivide(small_side, notches_small, None, ctx ) ],
                      None,
                      f'small side {c1}x' ) )

    return objects

def flat(kind, r, width, subdivisions, thickness, notch_depth):

    tiling = sphere_tilings.chiral_2_to_1(r-thickness, width, subdivisions, kind)
    tiling_shapes = tiling['shapes']
    dihedral = tiling['dihedral']
    shape_desc = [ f'{c}x' for c in tiling['shape_counts'] ]

    ctx = { 'width' : thickness, 'indent': notch_depth }

    objects = []
    objects.append( ( [ pathedit.subdivide(tiling_shapes[0], '2II2II2I', None, ctx) ],
                      None,
                      f'{tiling["shape_counts"][0]}x' ) )


    for i in range(1, len(tiling_shapes)):
        objects.append( ( [ pathedit.subdivide(tiling_shapes[i], '2I2I', None, ctx) ],
                           None,
                           f'{tiling["shape_counts"][i]}x' ) )

    v1 = cmath.rect(notch_depth, 3*(cmath.tau/8)+dihedral/2)
    d1 = cmath.rect(thickness,   1*(cmath.tau/8)+dihedral/2)
    v2 = cmath.rect(notch_depth, 3*(cmath.tau/8)-dihedral/2)
    d2 = cmath.rect(thickness,   5*(cmath.tau/8)-dihedral/2)

    joint = [ (z.real, z.imag) for z in (-d2, v2-d2, v2, 0, v1, v1-d1, -d1) ]

    objects.append( ( [joint], None, f'{tiling["shape_counts"][0]*6//2}x' ) )

    return objects


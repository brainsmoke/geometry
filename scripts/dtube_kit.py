import math, cmath, itertools

import sphere_tilings, pathedit, linear

def line_len(shape, ix):
    return linear.dist(shape[ix], shape[(ix+1)%len(shape)])

def double_tube(kind, r, width, top_space, bottom_space, subdivisions, thickness, notch_width):

    height = 3*thickness+top_space+bottom_space
    radius_tiling = sphere_tilings.chiral_2_to_1(r,                       width, subdivisions, kind)
    top_tiling    = sphere_tilings.chiral_2_to_1(r-thickness,             width, subdivisions, kind)
    mid_tiling    = sphere_tilings.chiral_2_to_1(r-2*thickness-top_space, width, subdivisions, kind)
    bottom_tiling = sphere_tilings.chiral_2_to_1(r-height,                width, subdivisions, kind)

    top_joint = top_tiling['shapes'][0]
    bottom_joint = bottom_tiling['shapes'][0]
    radius_joint = radius_tiling['shapes'][0]
    mid_joint = mid_tiling['shapes'][0]

    dihedral = top_tiling['dihedral']
    ctx = {
        'width' : notch_width,
        'left'  : notch_width + line_len(radius_joint, 1) - line_len(top_joint, 1),
        'alt'   : notch_width + line_len(radius_joint, 1) - line_len(top_joint, 1),
        'right' : notch_width,
        'indent': thickness
    }
    ctx2 = dict(ctx)
    ctx2['width'] *= 1.5

    shapes = [
        [ pathedit.subdivide(top_joint, 'IccIccIc', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx) ],
        [ pathedit.subdivide(mid_joint, 'IbbIseIb', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx2) ],
        [ pathedit.flip(pathedit.subdivide(bottom_joint, 'IccIccIc', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx)) ],
    ]

    c1, c2, c3 = top_tiling['shape_counts'][0], mid_tiling['shape_counts'][0], bottom_tiling['shape_counts'][0]

    shape_desc = [ f'top joint {c1}x',
                   f'mid joint {c2}x',
                   f'bottom joint {c3}x']

    radius_div_len, bottom_div_len = [], []

    if subdivisions > 1:
        radius_div = radius_tiling['shapes'][1]
        top_div = top_tiling['shapes'][1]
        mid_div = mid_tiling['shapes'][1]
        bottom_div = bottom_tiling['shapes'][1]
        shapes += [
            [ pathedit.subdivide(top_div, 'IcIc', (dihedral,0,dihedral,0), ctx) ],
            [ pathedit.subdivide(mid_div, 'IbIb', (dihedral,0,dihedral,0), ctx2) ],
            [ pathedit.flip(pathedit.subdivide(bottom_div, 'IcIc', (dihedral,0,dihedral,0), ctx)) ],
        ]

        c4, c5, c6 = top_tiling['shape_counts'][1], mid_tiling['shape_counts'][1], bottom_tiling['shape_counts'][1]

        shape_desc += [ f'top division {c4}x',
                        f'mid division {c5}x',
                        f'bottom division {c6}x' ]

        bottom_div_len = [ line_len(bottom_div, 1) ] * (subdivisions-1)
        radius_div_len = [ line_len(radius_div, 1) ] * (subdivisions-1)

    tau = math.tau
    angles_arc_small = [ tau/4 ] + [ dihedral - tau/2 ] * (subdivisions) + [ tau/4 ] + \
                       [ tau/4 ] + [ tau/2 - dihedral ] * (subdivisions) + [ tau/4 ]

    angles_arc_large = [ tau/4 ] + [ dihedral - tau/2 ] * (subdivisions*2) + [ tau/4 ] + \
                       [ tau/4 ] + [ tau/2 - dihedral ] * (subdivisions*2) + [ tau/4 ]

    lengths_arc_small = [
        height,
        line_len(bottom_joint, 2),
        ] + bottom_div_len + [
        line_len(bottom_joint, 1),
        height,
        line_len(radius_joint, 1),
        ] + radius_div_len + [
        line_len(radius_joint, 2),
    ]

    lengths_arc_large = [
        height,
        line_len(bottom_joint, 4)
        ] + bottom_div_len + [
        line_len(bottom_joint, 7)
        ] + bottom_div_len + [
        line_len(bottom_joint, 5),
        height,
        line_len(radius_joint, 5),
        ] + radius_div_len + [
        line_len(radius_joint, 7)
        ] + radius_div_len + [
        line_len(radius_joint, 4)
    ]

    notches_small = 'I' + 'C'*(subdivisions  +1) + 'IU' + 'a'*(subdivisions  -1) + 'u'
    notches_large = 'I' + 'C'*(subdivisions*2+1) + 'IU' + 'a'*(subdivisions*2-1) + 'u'

    small_side = pathedit.lengths_and_angles_to_polyline(lengths_arc_small, angles_arc_small)
    large_side = pathedit.lengths_and_angles_to_polyline(lengths_arc_large, angles_arc_large)

    shapes.append( [ pathedit.subdivide(large_side, notches_large, (0,)*len(large_side), ctx ) ] )
    shapes.append( [ pathedit.subdivide(small_side, notches_small, (0,)*len(small_side), ctx ) ] )

    shape_desc += [ f'large side {c1}x',
                    f'small side {c1}x' ]

    return shapes, shape_desc


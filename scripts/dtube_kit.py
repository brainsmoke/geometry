import math, cmath, itertools

import sphere_tilings, pathedit, linear

def line_len(shape, ix):
    return linear.dist(shape[ix], shape[(ix+1)%len(shape)])

def rev(l):
    return list(reversed(l))

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
        [ pathedit.subdivide(mid_joint, 'IbbIESIb', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx2) ],
        [ pathedit.flip_x(pathedit.subdivide(bottom_joint, 'IccIccIc', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx)) ],
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
            [ pathedit.flip_x(pathedit.subdivide(bottom_div, 'IcIc', (dihedral,0,dihedral,0), ctx)) ],
        ]

        c4, c5, c6 = top_tiling['shape_counts'][1], mid_tiling['shape_counts'][1], bottom_tiling['shape_counts'][1]

        shape_desc += [ f'top division {c4}x',
                        f'mid division {c5}x',
                        f'bottom division {c6}x' ]

        bottom_div_len = [ line_len(bottom_div, 1) ] * (subdivisions-1)
        radius_div_len = [ line_len(radius_div, 1) ] * (subdivisions-1)
        mid_div_len    = [ line_len(mid_div,    1) ] * (subdivisions-1)

    tau = math.tau

    angles_arc_small = [ dihedral - tau/2 ] * (subdivisions) + [ tau/4 ]*2 + \
                       [ tau/2 - dihedral ] * (subdivisions) + [ tau/4 ]

    angles_arc_large = [ dihedral - tau/2 ] * (subdivisions*2) + [ tau/4 ]*2 + [ -tau/4 ]*2 + [ tau/4 ]*2 + \
                       [ tau/2 - dihedral ] * (subdivisions*2) + [ tau/4 ]*2 + [ -tau/4 ]*2 + [ tau/4 ]

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
        thickness+bottom_space,
        ctx2['width'],
        thickness,
        ctx2['width'],
        thickness+top_space,
        line_len(radius_joint, 5),
        ] + radius_div_len + [
        line_len(radius_joint, 7),
        ] + radius_div_len + [
        line_len(radius_joint, 4),
        thickness+top_space,
        ctx2['width'],
        thickness,
        ctx2['width'],
    ]

    notches_small = 'C'*(subdivisions  +1) + 'IU' + 'a'*(subdivisions  -1) + 'uI'
    notches_large = 'C'*(subdivisions*2+1) + 'IIIIIU' + 'a'*(subdivisions*2-1) + 'uIIIII'

    small_side = pathedit.lengths_and_angles_to_polyline(lengths_arc_small, angles_arc_small)
    large_side = pathedit.lengths_and_angles_to_polyline(lengths_arc_large, angles_arc_large)

    small_side_shape = [ pathedit.subdivide(small_side, notches_small, (0,)*len(small_side), ctx ) ]
    large_side_shape = [ pathedit.subdivide(large_side, notches_large, (0,)*len(large_side), ctx ) ]

    mid_lengths_small = [ line_len(mid_joint, 2) ] + mid_div_len + [ line_len(mid_joint, 1) ] 
    mid_lengths_large = [ line_len(mid_joint, 4) ] + mid_div_len + [ line_len(mid_joint, 7) ] \
                                                   + mid_div_len + [ line_len(mid_joint, 5) ]

    mid_arcs_small = [ dihedral - tau/2 ] * (subdivisions+1)
    mid_arcs_large = [ dihedral - tau/2 ] * (subdivisions+1)*2

    mid_holes_small = pathedit.lengths_and_angles_to_polyline(mid_lengths_small, mid_arcs_small, start_at=(0, thickness+bottom_space))
    mid_holes_small = pathedit.subdivide(mid_holes_small, 'b'*(subdivisions+1), (0,)*len(mid_holes_small), ctx2)
    for s in range(subdivisions+1):
        small_side_shape.append( rev(mid_holes_small[s*11+1:s*11+5]) )
        small_side_shape.append( rev(mid_holes_small[s*11+5:s*11+9]) )

    mid_holes_large = pathedit.lengths_and_angles_to_polyline(mid_lengths_large, mid_arcs_large, start_at=(0, thickness+bottom_space))
    mid_holes_large = pathedit.subdivide(mid_holes_large, 'I'+'b'*(subdivisions*2-1)+'I', (0,)*len(mid_holes_large), ctx2)

    for s in range(subdivisions*2-1):
        large_side_shape.append( rev(mid_holes_large[s*11+3:s*11+7]) )
        large_side_shape.append( rev(mid_holes_large[s*11+7:s*11+11]) )

    shapes.append( large_side_shape )
    shapes.append( small_side_shape )

    shape_desc += [ f'large side {c1}x',
                    f'small side {c1}x' ]

    return shapes, shape_desc


import math, cmath

import sphere_tilings, pathedit, linear

def line_len(shape, ix):
    return linear.dist(shape[ix], shape[(ix+1)%len(shape)])

def arc( lengths, arcs ):
   v = 0, 0
   a = 0
   poly = [v]
   for l, da in zip(lengths, arcs):
       v = linear.vector_add(v, (l*math.sin(a), l*math.cos(a)))
       poly.append(v)
       a += da
   return poly[:-1]

def tube(kind, r, width, height, subdivisions, thickness, notch_width):

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

    shapes = [
         pathedit.subdivide(top_joint, 'IccIccIc', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx),
         pathedit.flip(pathedit.subdivide(bottom_joint, 'IccIccIc', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx)),
    ]

    c1, c2 = top_tiling['shape_counts'][0], bottom_tiling['shape_counts'][0]

    shape_desc = [ f'top joint {c1}x',
                   f'bottom joint {c2}x']

    radius_div_len, bottom_div_len = [], []

    if subdivisions > 1:
        radius_div = radius_tiling['shapes'][1]
        top_div = top_tiling['shapes'][1]
        bottom_div = bottom_tiling['shapes'][1]
        shapes += [
            pathedit.subdivide(top_div, 'IcIc', (dihedral,0,dihedral,0), ctx),
            pathedit.flip(pathedit.subdivide(bottom_div, 'IcIc', (dihedral,0,dihedral,0), ctx)),
        ]

        c3, c4 = top_tiling['shape_counts'][1], bottom_tiling['shape_counts'][1]

        shape_desc += [ f'top division {c3}x',
                        f'bottom division {c4}x' ]

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

    small_side = arc(lengths_arc_small, angles_arc_small)
    large_side = arc(lengths_arc_large, angles_arc_large)

    shapes.append( pathedit.subdivide(large_side, notches_large, (0,)*len(large_side), ctx ) )
    shapes.append( pathedit.subdivide(small_side, notches_small, (0,)*len(small_side), ctx ) )

    shape_desc += [ f'large side {c1}x',
                    f'small side {c1}x' ]

    return shapes, shape_desc

def flat(kind, r, width, subdivisions, thickness, notch_depth):

    tiling = sphere_tilings.chiral_2_to_1(r-thickness, width, subdivisions, kind)
    shapes = tiling['shapes']
    dihedral = tiling['dihedral']
    shape_desc = [ f'{c}x' for c in tiling['shape_counts'] ]

    ctx = { 'width' : thickness, 'indent': notch_depth }

    shapes[0] = pathedit.subdivide(shapes[0], '2II2II2I', (dihedral,0,0,dihedral,0,0,dihedral,0), ctx)
    for i in range(1, len(shapes)):
        shapes[i] = pathedit.subdivide(shapes[i], '2I2I', (dihedral,0,dihedral,0), ctx)

    v1 = cmath.rect(notch_depth, 3*(cmath.tau/8)+dihedral/2)
    d1 = cmath.rect(thickness,   1*(cmath.tau/8)+dihedral/2)
    v2 = cmath.rect(notch_depth, 3*(cmath.tau/8)-dihedral/2)
    d2 = cmath.rect(thickness,   5*(cmath.tau/8)-dihedral/2)

    joint = [ (z.real, z.imag) for z in ( 0, v1, v1+d1, d1, d1+v2, d1+v2-d2, d1-d2 ) ]

    shapes.append(joint)
    c = tiling['shape_counts'][0] * 6/2
    shape_desc.append(f'{c}x')

    return shapes, shape_desc


#!/usr/bin/env python3
import cmath, sys, math

def nextpoint( a, b1, b2 ):
    ax, ay, az = a
    b1x, b1y, b1z = b1
    b2x, b2y, b2z = b2
    return (b1x+b2x-ax, b1y+b2y-ay, b1z+b2z-az)

def interpol(a, b, inter):
    ax, ay, az = a
    bx, by, bz = b
    return ( ax+inter*(bx-ax), ay+inter*(by-ay), az+inter*(bz-az) )

def interpol2(a, b, inter):
    ax, ay = a
    bx, by = b
    return ( ax+inter*(bx-ax), ay+inter*(by-ay) )

def vector_add( a, b ):
    ax, ay, az = a
    bx, by, bz = b
    return (ax+bx, ay+by, az+bz)

def vector_sub( a, b ):
    ax, ay, az = a
    bx, by, bz = b
    return (ax-bx, ay-by, az-bz)

def scalar_mul( s, a ):
    x, y, z = a
    return (s*x, s*y, s*z)

def normalize( a ):
    x, y, z = a
    d = math.sqrt(x*x+y*y+z*z)
    return (x/d, y/d, z/d)

def length( a ):
    x, y, z = a
    return math.sqrt(x*x+y*y+z*z)

def scalar_product(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return ( ax*bx + ay*by + az*bz )

def cross_product(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return ( ay*bz-by*az, az*bx-bz*ax, ax*by-bx*ay )

def get_normal( poly ):
    v1 = vector_sub(poly[-1], poly[0])
    v2 = vector_sub(poly[1], poly[0])
    return normalize ( cross_product ( v1, v2 ) )

def get_density( poly ):
    v1 = normalize(vector_sub(poly[-1], poly[0]))
    v2 = normalize(vector_sub(poly[1], poly[0]))
    return length ( cross_product ( v1, v2 ) )

def dihedral(p1, p2):
    return scalar_product( get_normal(p1), get_normal(p2) )

def dist_sq(p1, p2):
    return sum( (a-b)*(a-b) for a, b in zip(p1, p2))

def dist(p1, p2):
    return math.sqrt(dist_sq(p1, p2))

def polozono(segments, height, edge_len):
    n_rings = segments+1
    rings = [ [] for _ in range(n_rings) ]
    rings[0] = [ (0,0,0) ] * segments
    facets = [ [] for _ in range(n_rings-2) ]

    dz = height/segments
    r1 = (edge_len*edge_len-dz*dz)**.5
    for i in range(segments):
        rot = cmath.rect(r1, i*cmath.tau/segments)
        x, y, z = rot.real, rot.imag, dz

        rings[1].append( (x,y,z) )

    for ring in range(n_rings-2):
        for i in range(segments):
            a, b, d = rings[ring][i-1], rings[ring+1][i-1], rings[ring+1][i]
            c = nextpoint(a, b, d)
            facets[ring].append( (a, b, c, d) )
            rings[ring+2].append( c )

    return rings, facets

def solid(rings):
    print ("""polyhedron(points=["""+ ','.join(f"[{x},{y},{z}]" for r in rings for x, y, z in r) + """], faces=[""")
    segments = len(rings[0])

    for r in range(len(rings)-2):
        for i in range(segments):
            a = r*segments + (i-1)%segments
            b = (r+1)*segments + (i-1)%segments
            c = (r+2)*segments + (i)%segments
            d = (r+1)*segments + (i)%segments
            print (f"[{a},{b},{c},{d}],")

    print ("""]);""")

def openscad_facet(points, thickness):
    delta = scalar_mul(thickness, get_normal(points))
    x, y, z = delta
    print (f"/* delta: {x},{y},{z} */")
    double_points = points + [ vector_add(x, delta) for x in points ]
    n = len(points)
    print ("""polyhedron(points=["""+','.join(f"[{x:f},{y:f},{z:f}]" for x, y, z in double_points) + """], faces=[""")
    print ('[' + ','.join(str(x) for x in range(n)) + '],')
    for i in range(n):
        print ('[' + ','.join( str(x) for x in ( (i+1)%n, i, i+n, n+(i+1)%n ) ) + '],')
    print ('[' + ','.join(str(x) for x in range(2*n-1, n-1, -1)) + ']')
    print ("""]);""")



def weave(facets, ratio, height, thickness):
    print ("""module x() {""")
    for f_ring in facets:
        for a,b,c,d in f_ring:
            points = [ a, b, c, interpol(c, d, ratio), interpol(b, d, ratio), interpol(a, d, ratio) ]
            openscad_facet(points, thickness)
    print ("""}""")
    dis = -height/2
    print (f"translate([0,0,{dis}]) x();")

def weave2(facets, ratio, height, thickness):
    print ("""module x() {""")
    for f_ring in facets:
        for a,b,c,d in f_ring:
            points = [ a, b, c, d ]
            ring_ratio = ratio/get_density(points)
            if ring_ratio < 1:
                points = [ a, b, c, interpol(c, d, ring_ratio), interpol(b, d, ring_ratio), interpol(a, d, ring_ratio) ]
            openscad_facet(points, thickness)
    print ("""}""")
    dis = -height/2
    print (f"translate([0,0,{dis}]) x();")


def weave3(facets, ratio, ratio2, height, thickness):
    print ("""/* kind: {}, ratio: {}, ratio2: {} */""".format("weave3", ratio, ratio2))
    print ("""module x() {""")
    for i,f_ring in enumerate(facets):
        for a,b,c,d in f_ring:
            points = [ a, b, c, d ]
            ring_ratio = ratio
            if i < len(facets)-1:
                shift_ratio = (1-ratio)*ratio2
            else:
                shift_ratio = 0
            if i == 0:
                points = [ interpol(b, a, ring_ratio), b, interpol(b, c, ring_ratio), interpol(d, c, ring_ratio+shift_ratio), interpol(d, c, shift_ratio), interpol(b, d, ring_ratio), d, interpol(d, a, ring_ratio) ]
            else:
                points = [ a, b, interpol(b, c, ring_ratio), interpol(d, c, ring_ratio+shift_ratio), interpol(d, c, shift_ratio), interpol(b, d, ring_ratio), interpol(a, d, ring_ratio) ]
            openscad_facet(points, thickness)
    print ("""}""")
    dis = -height/2
    print (f"translate([0,0,{dis}]) x();")


def weave4(facets, ratio, height, thickness):
    print ("""/* kind: {}, ratio: {} */""".format("weave4", ratio))
    print ("""module x() {""")
    for i,f_ring in enumerate(facets):
        for a,b,c,d in f_ring:
            points = [ a, b, c, d ]
            ring_ratio = ratio
            if i < len(facets)-1:
                p3 = interpol(b, c, ring_ratio)
                shift_ratio = (dist_sq(c, d) + dist_sq(p3, c) - dist_sq(p3, d)) / (2*dist_sq(c, d))
            else:
                shift_ratio = 1-ring_ratio
            if i == 0:
                points = [ interpol(b, a, ring_ratio), b, interpol(b, c, ring_ratio), interpol(c, d, shift_ratio), interpol(c, d, ring_ratio+shift_ratio), interpol(b, d, ring_ratio), d, interpol(d, a, ring_ratio) ]
            else:
                points = [ a, b, interpol(b, c, ring_ratio), interpol(c, d, shift_ratio), interpol(c, d, shift_ratio+ring_ratio), interpol(b, d, ring_ratio), interpol(a, d, ring_ratio) ]
            openscad_facet(points, thickness)
    print ("""}""")
    dis = -height/2
    print (f"translate([0,0,{dis}]) x();")


def weave5(facets, ratio, height, thickness):
    print ("""/* kind: {}, ratio: {} */""".format("weave4", ratio))
    print ("""module x() {""")
    for i,f_ring in enumerate(facets):
        for a,b,c,d in f_ring:
            points = [ a, b, c, d ]
            ring_ratio = ratio
            if i < len(facets)-1:
                p3 = interpol(b, c, ring_ratio)
                shift_ratio = (dist_sq(c, d) + dist_sq(p3, c) - dist_sq(p3, d)) / (2*dist_sq(c, d))
            else:
                shift_ratio = 1-ring_ratio
            points = [ a, b, interpol(b, c, ring_ratio), interpol(c, d, shift_ratio), interpol(c, d, shift_ratio+ring_ratio), interpol(b, d, ring_ratio), interpol(a, d, ring_ratio) ]
            openscad_facet(points, thickness)
    print ("""}""")
    dis = -height/2
    print (f"translate([0,0,{dis}]) x();")

def dist(a,b):
    ax,ay,az = a
    bx,by,bz = b
    return math.sqrt( (ax-bx)*(ax-bx) + (ay-by)*(ay-by) + (az-bz)*(az-bz) )

def svgheader():
   print("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg8"
   inkscape:version="1.0.2 (e86c870879, 2021-01-15)"
   sodipodi:docname="drawing-4.svg">
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="400"
     inkscape:cy="560"
     inkscape:document-units="mm"
     inkscape:current-layer="layer1"
     inkscape:document-rotation="0"
     showgrid="false"
     inkscape:window-width="1364"
     inkscape:window-height="750"
     inkscape:window-x="1"
     inkscape:window-y="17"
     inkscape:window-maximized="0" />
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
""")

def svgfooter():
    print("""</g></svg>""")


def flat(facets, ratio=None):
    svgheader()
    x = 0
    for f_ring in facets:
        a,b,c,d = f_ring[0]
        h, w = dist(a,c), dist(b,d)
        points = [ (0,-h/2), (-w/2,0), (0,h/2), (w/2, 0) ]
        if ratio != None:
            a,b,c,d = points
            points = [ a, b, c, interpol2(c, d, ratio), interpol2(b, d, ratio), interpol2(a, d, ratio) ]

        l,r = min(x for x,y in points), max(x for x,y in points)
        print ("""<g transform="translate({:f},0)" >""".format(x-l) )
        print ("""<path style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(x[0])+','+str(x[1]) for x in points) + ' Z" /></g>')
        x += r-l + 2
    svgfooter()


def flat2(facets, ratio=None):
    svgheader()
    x = 0
    for f_ring in facets:
        a,b,c,d = f_ring[0]
        h, w = dist(a,c), dist(b,d)
        points = [ (0,-h/2,0), (-w/2,0,0), (0,h/2,0), (w/2, 0,0) ]
        if ratio != None:
            a,b,c,d = points
            ring_ratio = ratio/get_density(points)
            if ring_ratio < 1:
                points = [ a, b, c, interpol(c, d, ring_ratio), interpol(b, d, ring_ratio), interpol(a, d, ring_ratio) ]

        l,r = min(x for x,y,_ in points), max(x for x,y,_ in points)
        print ("""<g transform="translate({:f},0)" >""".format(x-l) )
        print ("""<path style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(x[0])+','+str(x[1]) for x in points) + ' Z" /></g>')
        x += r-l + 2
    svgfooter()


def flat3(facets, ratio, ratio2, height):
    svgheader()
    x = 0
    print ("""<!-- kind: {}, ratio: {}, ratio2: {} -->""".format("weave3", ratio, ratio2))
    for i,f_ring in enumerate(facets):
        a,b,c,d = f_ring[0]
        h, w = dist(a,c), dist(b,d)
        points = [ (0,-h/2,0), (-w/2,0,0), (0,h/2,0), (w/2, 0,0) ]
        rhomb = points
        a,b,c,d = points
        ring_ratio = ratio
        if i < len(facets)-1:
            shift_ratio = (1-ratio)*ratio2
        else:
            shift_ratio = 0
        if i == 0:
            points = [ interpol(b, a, ring_ratio), b, interpol(b, c, ring_ratio), interpol(d, c, ring_ratio+shift_ratio), interpol(d, c, shift_ratio), interpol(b, d, ring_ratio), d, interpol(d, a, ring_ratio) ]
        else:
            points = [ a, b, interpol(b, c, ring_ratio), interpol(d, c, ring_ratio+shift_ratio), interpol(d, c, shift_ratio), interpol(b, d, ring_ratio), interpol(a, d, ring_ratio) ]

        l,r = min(x for x,y,_ in points), max(x for x,y,_ in points)

        print ("""<g transform="translate({:f},0)" >""".format(x-l) )
        print ("""<path style="fill:none;stroke:#ff0000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(px[0])+','+str(px[1]) for px in rhomb) + ' Z" />')
        print ("""<path style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(px[0])+','+str(px[1]) for px in points) + ' Z" /></g>')
        x += r-l + 2
    svgfooter()


def flat4(facets, ratio, height):
    svgheader()
    x = 0
    print ("""<!-- kind: {}, ratio: {} -->""".format("flat4", ratio))
    for i,f_ring in enumerate(facets):
        a,b,c,d = f_ring[0]
        h, w = dist(a,c), dist(b,d)
        points = [ (0,-h/2,0), (-w/2,0,0), (0,h/2,0), (w/2, 0,0) ]
        rhomb = points
        a,b,c,d = points
        ring_ratio = ratio
        if i < len(facets)-1:
            p3 = interpol(b, c, ring_ratio)
            shift_ratio = (dist_sq(c, d) + dist_sq(p3, c) - dist_sq(p3, d)) / (2*dist_sq(c, d))
        else:
            shift_ratio = 1-ring_ratio
        if i == 0:
            points = [ interpol(b, a, ring_ratio), b, interpol(b, c, ring_ratio), interpol(c, d, shift_ratio), interpol(c, d, ring_ratio+shift_ratio), interpol(b, d, ring_ratio), d, interpol(d, a, ring_ratio) ]
        else:
            points = [ a, b, interpol(b, c, ring_ratio), interpol(c, d, shift_ratio), interpol(c, d, shift_ratio+ring_ratio), interpol(b, d, ring_ratio), interpol(a, d, ring_ratio) ]

        l,r = min(x for x,y,_ in points), max(x for x,y,_ in points)

        print ("""<g transform="translate({:f},0)" >""".format(x-l) )
        print ("""<path style="fill:none;stroke:#ff0000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(px[0])+','+str(px[1]) for px in rhomb) + ' Z" />')
        print ("""<path style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(px[0])+','+str(px[1]) for px in points) + ' Z" /></g>')
        x += r-l + 2
    svgfooter()


def dihedrals(facets, slot_width, slot_length, slot_padd, slot_padd2):
    x = 0
    dihedral_dot_prods = [ dihedral(facets[0][0], facets[0][1]   ) ] + \
                         [ dihedral(facets[i][0], facets[i+1][0] ) for i in range(len(facets)-1) ] + \
                         [ dihedral(facets[len(facets)-1][0], facets[len(facets)-1][1]) ]

    for cos_th in dihedral_dot_prods:
        print ( math.degrees(math.acos(cos_th)))
        print("XXXX")

def conn(facets, slot_width, slot_length, slot_padd, slot_padd2):
    svgheader()
    x = 0
    dihedral_dot_prods = [ dihedral(facets[0][0], facets[0][1]   ) ] + \
                         [ dihedral(facets[i][0], facets[i+1][0] ) for i in range(len(facets)-1) ] + \
                         [ dihedral(facets[len(facets)-1][0], facets[len(facets)-1][1]) ]

    half_path = [
                (0,          0),
                (-slot_padd, 0),
                          (-slot_padd,             -slot_width),
                          (-slot_padd-slot_length, -slot_width),
                (-slot_padd-slot_length,   0),
                (-slot_padd-slot_padd2-slot_length, 0),
        (-slot_padd2-slot_length, slot_padd),
    ]
    rev_path = [ (-x, y) for x, y in reversed(half_path)][:-1]

    
    for cos_th in dihedral_dot_prods:
        sin_th = (1-cos_th*cos_th)**.5

        path = half_path + [ (x*cos_th-y*sin_th, y*cos_th+x*sin_th) for x, y in rev_path ]
        l,r = min(x for x,y in path), max(x for x,y in path)
        print ("""<g transform="translate({:f},0)" >""".format(x-l) )
        print ("""<path style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(x[0])+','+str(x[1]) for x in path) + ' Z" /></g>')
        x += r-l + 2
    svgfooter()


def conn2(facets, slot_width, slot_length, slot_padd, slot_padd2):
    svgheader()
    x = 0
    dihedral_dot_prods = [ dihedral(facets[0][0], facets[0][1]   ) ] + \
                         [ dihedral(facets[i][0], facets[i+1][0] ) for i in range(len(facets)-1) ] + \
                         [ dihedral(facets[len(facets)-1][0], facets[len(facets)-1][1]) ]

    half_path = [
                (0,          0),
                (-slot_padd-slot_padd2-slot_length, 0),
        (-slot_padd2-slot_length, slot_padd),
    ]
    rev_path = [ (-x, y) for x, y in reversed(half_path)][:-1]

    
    for cos_th in dihedral_dot_prods:
        sin_th = (1-cos_th*cos_th)**.5

        path = half_path + [ (x*cos_th-y*sin_th, y*cos_th+x*sin_th) for x, y in rev_path ]
        l,r = min(x for x,y in path), max(x for x,y in path)
        print ("""<g transform="translate({:f},0)" >""".format(x-l) )
        print ("""<path style="fill:none;stroke:#000000;stroke-width:0.264583px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1" """)
        print ('d="M ' + " ".join(str(x[0])+','+str(x[1]) for x in path) + ' Z" /></g>')
        x += r-l + 2
    svgfooter()

if __name__ == '__main__':
    thickness = 3

    kind, segments, height, edge_len, ratio, ratio2, slot_width, slot_length, slot_padd, slot_padd2 = (sys.argv + [None, None, None, None, None, None, None, None, None, None, None])[1:11]
    if segments == None:
        segments = '9'
    if height == None:
        height = '620'
    if edge_len == None:
        edge_len = '100'
    if ratio == None:
        ratio = 1/4
    if ratio2 == None:
        ratio2 = 0.
    if slot_width == None:
        slot_width = 3
    if slot_length == None:
        slot_length = 10
    if slot_padd == None:
        slot_padd = 3
    if slot_padd2 == None:
        slot_padd2 = 10

    segments, height, edge_len, ratio, ratio2 = int(segments), float(height), float(edge_len), float(ratio), float(ratio2)

    slot_width, slot_length, slot_padd, slot_padd2 = float(slot_width), float(slot_length), float(slot_padd), float(slot_padd2)

    rings, facets = polozono( segments, height, edge_len )
    if kind == 'solid':
        solid(rings)
    elif kind == 'weave':
        weave(facets, ratio, height, thickness)
    elif kind == 'weave2':
        weave2(facets, ratio, height, thickness)
    elif kind == 'weave3':
        weave3(facets, ratio, ratio2, height, thickness)
    elif kind == 'weave4':
        weave4(facets, ratio, height, thickness)
    elif kind == 'weave5':
        weave5(facets, ratio, height, thickness)
    elif kind == 'flat':
        flat(facets, ratio)
    elif kind == 'flat2':
        flat2(facets, ratio)
    elif kind == 'flat3':
        flat3(facets, ratio, ratio2, height)
    elif kind == 'flat4':
        flat4(facets, ratio, height)
    elif kind == 'conn':
        conn(facets, slot_width, slot_length, slot_padd, slot_padd2)
    elif kind == 'conn2':
        conn2(facets, slot_width, slot_length, slot_padd, slot_padd2)
    elif kind == 'dihedrals':
        dihedrals(facets, slot_width, slot_length, slot_padd, slot_padd2)
    else:
         raise "meh."


#!/usr/bin/env python3

import sys, cmath

import plot, sphere_tilings, pathedit

kind = (sys.argv[1:] + ['penta'])[0]
r = 200 # outer radius, measured at the midpoint of the facet
width = 22
h = 22
subdivisions=1
notch_depth = 10

thickness=3
#cutwidth=.3
cutwidth=0

tiling = sphere_tilings.chiral_2_to_1(r-thickness, width, subdivisions, kind)
shapes = tiling['shapes']
dihedral = tiling['dihedral']
shape_counts = tiling['shape_counts']

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

plot.start(cutwidth=cutwidth)


for points, n in zip(shapes, shape_counts):
    plot.plot([points], f'{n}x')

plot.end()

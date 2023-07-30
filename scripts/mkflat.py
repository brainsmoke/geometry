#!/usr/bin/env python3

import sys, cmath

import plot, kit

kind = (sys.argv[1:] + ['penta'])[0]
r = 200 # outer radius, measured at the midpoint of the facet
width = 22
h = 22
subdivisions=1
notch_depth = 10

thickness=3
#cutwidth=.3
cutwidth=0

shapes, shape_desc = kit.flat(kind, r, width, subdivisions, thickness, notch_depth)

plot.start(cutwidth=cutwidth)

for points, desc in zip(shapes, shape_desc):
    plot.plot([points], desc)

plot.end()

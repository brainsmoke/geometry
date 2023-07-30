#!/usr/bin/env python3

import sys, cmath

import plot, kit

kind = (sys.argv[1:] + ['penta'])[0]
r = 360 # outer radius, measured at the midpoint of the facet
width = 22
height = 22
subdivisions=3
notch_width = 3

thickness=3
#cutwidth=.3
cutwidth=0

shapes, shape_desc = kit.tube(kind, r, width, height, subdivisions, thickness, notch_width)

plot.start(cutwidth=cutwidth)

for points, desc in zip(shapes, shape_desc):
    plot.plot([points], desc)

plot.end()

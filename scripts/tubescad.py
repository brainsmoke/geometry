#!/usr/bin/env python3

import sys, cmath

import kit, scad

kind = (sys.argv[1:] + ['penta'])[0]
assert kind in ('penta', 'tri')
r = 250 # outer radius, measured at the midpoint of the facet
width = 18
height = 18
subdivisions=2
notch_width = 3

thickness=3

shapes, shape_desc = kit.tube(kind, r, width, height, subdivisions, thickness, notch_width)

scad.tube(shapes, kind, r, width, height, subdivisions, thickness)


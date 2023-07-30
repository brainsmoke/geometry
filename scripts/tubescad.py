#!/usr/bin/env python3

import sys, cmath

import kit

kind = (sys.argv[1:] + ['penta'])[0]
assert kind in ('penta', 'tri')
r = 250 # outer radius, measured at the midpoint of the facet
width = 18
height = 18
subdivisions=2
notch_width = 3

thickness=3

shapes, shape_desc = kit.tube(kind, r, width, height, subdivisions, thickness, notch_width)

print(f"""
r = {r};
w = {width};
h = {height};
subdivisions = {subdivisions};
thickness = {thickness};

include <tubearc.scad>;
include <{kind}.scad>;
 
""")

def shape_module(name, points):
    print (f"module {name}"+""" ()
{
	linear_extrude(thickness) polygon(["""+','.join(f"[{x}, {y}]" for x,y in points)+"""]);
}""")


shape_module("top_joint", shapes[0])
shape_module("bottom_joint", shapes[1])
arc_ix = 2
top_div = []
bottom_div = []
if subdivisions > 1:
    arc_ix=4
    top_div = shapes[2]
    bottom_div = shapes[3]
shape_module("top_div", top_div)
shape_module("bottom_div", bottom_div)

shape_module("big_arc", shapes[arc_ix])
shape_module("small_arc", shapes[arc_ix+1])

print(f"{kind}()extend()arc();")


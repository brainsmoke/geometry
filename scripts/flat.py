#!/usr/bin/env python3

import sys, cmath, argparse

import kit, sphere_tilings, scad, plot

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-scad', action='store_true')
group.add_argument('-svg', action='store_true')

parser.add_argument('-tiling', type=str, default='penta', choices=['tri', 'quad', 'penta'], help="kind of tiling")

size_group = parser.add_mutually_exclusive_group()
size_group.add_argument('-r', type=float, default=250., help="outer radius, measured at the midpoint of the facet")
size_group.add_argument('-segment-top', type=float, help="segment size, measured from the top side")
size_group.add_argument('-segment-bottom', type=float, help="segment size, measured from the bottom side")

parser.add_argument('-width', type=float, default=22., help="tube width")
parser.add_argument('-subdivisions', type=int, default=1, help="number of subdivisions")
parser.add_argument('-thickness', type=float, default=3., help="material thickness")
parser.add_argument('-notch-depth', type=float, default=10, help="notch depth")
parser.add_argument('-kerf-offset', type=float, default=0, help="half the laser cutter's cutting width")

args = parser.parse_args()

kind = args.tiling
r = args.r
width = args.width
subdivisions= args.subdivisions
notch_depth = args.notch_depth
thickness=args.thickness
kerf_offset=args.kerf_offset

for seg_size, r_off in ( (args.segment_top,     0),
                         (args.segment_bottom,  thickness) ):
    if seg_size != None:
        r = sphere_tilings.radius_from_segment_size(seg_size, subdivisions, kind) + r_off

objects = kit.flat(kind, r, width, subdivisions, thickness, notch_depth)

if args.scad:
    paths = [ o[0] for o in objects ]
    scad.flat(paths, kind, r, width, subdivisions, thickness)
elif args.svg:
    plot.start(kerf_offset=kerf_offset)

    for cuts, engravings, desc in objects:
        plot.plot(cuts, engravings, text=desc)
 
    plot.end()


#!/usr/bin/env python3

import sys, cmath, argparse

import kit, scad, plot

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

out_group = parser.add_mutually_exclusive_group(required=True)
out_group.add_argument('-scad', action='store_true')
out_group.add_argument('-svg', action='store_true')

parser.add_argument('-tiling', type=str, default='penta', choices=['tri', 'quad', 'penta'], help="kind of tiling")

size_group = parser.add_mutually_exclusive_group()
size_group.add_argument('-r', type=float, default=250., help="outer radius, measured at the midpoint of the facet")
size_group.add_argument('-segment-top', type=float, help="segment size, measured from the top of the tube")
size_group.add_argument('-segment-bottom', type=float, help="segment size, measured from the bottom ot the tube")
size_group.add_argument('-segment-ceiling', type=float, help="segment size, measured from the bottom of the top segment")
size_group.add_argument('-segment-floor', type=float, help="segment size, measured from the top of the bottom segment")

parser.add_argument('-width', type=float, default=22., help="tube width")
parser.add_argument('-height', type=float, default=22., help="tube height")
parser.add_argument('-subdivisions', type=int, default=2, help="number of subdivisions")
parser.add_argument('-thickness', type=float, default=3., help="material thickness")
parser.add_argument('-notch-size', type=float, default=3., help="notch size")
parser.add_argument('-kerf-offset', type=float, default=0, help="half the laser cutter's cutting width")

args = parser.parse_args()

kind = args.tiling
r = args.r
width = args.width
height = args.height
subdivisions= args.subdivisions
notch_size = args.notch_size
thickness=args.thickness
kerf_offset=args.kerf_offset

for seg_size, r_off in ( (args.segment_top,     0),
                         (args.segment_bottom,  height),
                         (args.segment_ceiling, thickness),
                         (args.segment_floor,   height-thickness) ):
    if seg_size != None:
        r = kit.get_radius_from_segment_size(kind, subdivisions, seg_size) + r_off

shapes, shape_desc = kit.tube(kind, r, width, height, subdivisions, thickness, notch_size)

if args.scad:
    scad.tube(shapes, kind, r, width, height, subdivisions, thickness)
elif args.svg:
    plot.start(kerf_offset=kerf_offset)

    for points, desc in zip(shapes, shape_desc):
        plot.plot([points], desc)
 
    plot.end()


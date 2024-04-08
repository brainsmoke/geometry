#!/usr/bin/env python3

import sys, cmath, argparse

import dtube_kit, sphere_tilings, scad, plot

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

out_group = parser.add_mutually_exclusive_group(required=True)
out_group.add_argument('-scad', action='store_true')
out_group.add_argument('-svg', action='store_true')

parser.add_argument('-tiling', type=str, default='penta', choices=['tri', 'quad', 'penta'], help="kind of tiling")

size_group = parser.add_mutually_exclusive_group()
size_group.add_argument('-r', type=float, default=250., help="outer radius, measured at the midpoint of the facet")
size_group.add_argument('-mid-segment', type=float, help="segment size, measured from the top of the middle segment")

parser.add_argument('-width', type=float, default=22., help="tube width")
parser.add_argument('-top-space', type=float, default=20., help="....")
parser.add_argument('-bottom-space', type=float, default=20., help="....")
parser.add_argument('-subdivisions', type=int, default=2, help="number of subdivisions")
parser.add_argument('-thickness', type=float, default=3., help="material thickness")
parser.add_argument('-notch-size', type=float, default=3., help="notch size")
parser.add_argument('-kerf-offset', type=float, default=0, help="half the laser cutter's cutting width")

args = parser.parse_args()

kind = args.tiling
r = args.r
thickness=args.thickness
width = args.width
top_space = args.top_space
bottom_space = args.bottom_space
height = 3*thickness+top_space+bottom_space
subdivisions= args.subdivisions
notch_size = args.notch_size
kerf_offset=args.kerf_offset

if args.mid_segment != None:
    r = sphere_tilings.radius_from_segment_size(args.mid_segment, subdivisions, kind) + thickness+top_space

shapes, shape_desc = dtube_kit.double_tube(kind, r, width, top_space, bottom_space, subdivisions, thickness, notch_size)

if args.scad:
    scad.dtube(shapes, kind, r, width, top_space, bottom_space, subdivisions, thickness)
elif args.svg:
    plot.start(kerf_offset=kerf_offset)

    for points, desc in zip(shapes, shape_desc):
        plot.plot(points, desc)
 
    plot.end()


#!/usr/bin/env python3

import sys, cmath, argparse

import kit, scad, plot

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-scad', action='store_true')
group.add_argument('-svg', action='store_true')

parser.add_argument('-tiling', type=str, default='penta', choices=['tri', 'penta'], help="kind of tiling")
parser.add_argument('-r', type=float, default=250., help="outer radius, measured at the midpoint of the facet")
parser.add_argument('-width', type=float, default=22., help="tube width")
parser.add_argument('-height', type=float, default=22., help="tube height")
parser.add_argument('-subdivisions', type=int, default=1, help="number of subdivisions")
parser.add_argument('-thickness', type=float, default=3., help="material thickness")
parser.add_argument('-notch-size', type=float, default=3., help="notch size")
parser.add_argument('-cut-width', type=float, default=.3, help="laser cutter's cutting width")

args = parser.parse_args()

kind = args.tiling
r = args.r
width = args.width
height = args.height
subdivisions= args.subdivisions
notch_size = args.notch_size
thickness=args.thickness
cutwidth=args.cut_width

shapes, shape_desc = kit.tube(kind, r, width, height, subdivisions, thickness, notch_size)

if args.scad:
    scad.tube(shapes, kind, r, width, height, subdivisions, thickness)
elif args.svg:
    plot.start(cutwidth=cutwidth)

    for points, desc in zip(shapes, shape_desc):
        plot.plot([points], desc)
 
    plot.end()


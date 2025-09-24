#!/usr/bin/env python3

import sys, cmath, argparse, shlex

import kit, sphere_tilings, scad, plot

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

out_group = parser.add_mutually_exclusive_group(required=True)
out_group.add_argument('-scad', action='store_true')

parser.add_argument('-tiling', type=str, default='penta', choices=['tri', 'quad', 'penta'], help="kind of tiling")

size_group = parser.add_mutually_exclusive_group()
size_group.add_argument('-r', type=float, default=250., help="outer radius, measured at the midpoint of the facet")

parser.add_argument('-width', type=float, default=22., help="tube width")
parser.add_argument('-height', type=float, default=22., help="tube height")
parser.add_argument('-subdivisions', type=int, default=2, help="number of subdivisions")

args = parser.parse_args()

kind = args.tiling
r = args.r
width = args.width
height = args.height
subdivisions= args.subdivisions

cmdline = shlex.join(sys.argv)
comment = cmdline + f' [ r = {r:f} ]'

objects = kit.volume(kind, r, width, height, subdivisions)

scad.comment(comment)
paths = [ o[0] for o in objects ]
scad.volume(paths, kind, r, width, height, subdivisions)


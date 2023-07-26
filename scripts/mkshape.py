
import sys, math

import plot, sphere_tilings

kind = (sys.argv[1:] + ['penta'])[0]
r = 200 # inner radius
width = 22
h = 22
thickness=3
subdivisions=1

tiling = sphere_tilings.chiral_2_to_1(r, width, subdivisions, kind)

print ( tiling['dihedral'], file=sys.stderr )

plot.start()

for points in tiling['shapes']:
    plot.plot(points)

plot.end()

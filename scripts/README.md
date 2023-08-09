
## tube.py / flat.py

Generate openscad models / laser cuttable SVGs for a chiral spherical tiling
consisting of triangles and pentagons ( `-penta` ), or triangles and triangles ( `-tri` )


### tube.py



```
$ ./tube.py --help
usage: tube.py [-h] (-scad | -svg) [-tiling {tri,penta}] [-r R] [-width WIDTH]
               [-height HEIGHT] [-subdivisions SUBDIVISIONS]
               [-thickness THICKNESS] [-notch-size NOTCH_SIZE]
               [-cut-width CUT_WIDTH]

optional arguments:
  -h, --help            show this help message and exit
  -scad
  -svg
  -tiling {tri,penta}   kind of tiling (default: penta)
  -r R                  outer radius, measured at the midpoint of the facet
                        (default: 250.0)
  -width WIDTH          tube width (default: 22.0)
  -height HEIGHT        tube height (default: 22.0)
  -subdivisions SUBDIVISIONS
                        number of subdivisions (default: 2)
  -thickness THICKNESS  material thickness (default: 3.0)
  -notch-size NOTCH_SIZE
                        notch size (default: 3.0)
  -cut-width CUT_WIDTH  laser cutter's cutting width (default: 0.3)
```


### flat.py


```
$ ./flat.py --help
usage: flat.py [-h] (-scad | -svg) [-tiling {tri,penta}] [-r R] [-width WIDTH]
               [-subdivisions SUBDIVISIONS] [-thickness THICKNESS]
               [-notch-depth NOTCH_DEPTH] [-cut-width CUT_WIDTH]

optional arguments:
  -h, --help            show this help message and exit
  -scad
  -svg
  -tiling {tri,penta}   kind of tiling (default: penta)
  -r R                  outer radius, measured at the midpoint of the facet
                        (default: 250.0)
  -width WIDTH          tube width (default: 22.0)
  -subdivisions SUBDIVISIONS
                        number of subdivisions (default: 1)
  -thickness THICKNESS  material thickness (default: 3.0)
  -notch-depth NOTCH_DEPTH
                        notch depth (default: 10)
  -cut-width CUT_WIDTH  laser cutter's cutting width (default: 0.3)
```

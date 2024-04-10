
import math

import svg, pathedit

pad_x, pad_y = 3, 3
cur_x, cur_y = 0, 0
next_y = 0
max_x = 600
grow = 0
flip_y = True # in the SVG coordinate system, higher Y coordinates are lower

def box(point_list):
    x = min(x for points in point_list for x,_ in points)
    y = min(y for points in point_list for _,y in points)
    w = max(x for points in point_list for x,_ in points) - x
    h = max(y for points in point_list for _,y in points) - y
    return ( x, y, w, h )

def start(margin=3, width=600, height=400, kerf_offset=0):
    global pad_x, pad_y, max_x, grow
    pad_x, pad_y = margin, margin
    max_x = width
    grow = kerf_offset
    svg.header(width, height)

def end():
    svg.footer()

def plot(cuts=None, engravings=None, text=None):

    if cuts == None:
        cuts = []

    if engravings == None:
        engravings = []

    inside_out = [ pathedit.is_inside_out(p) for p in cuts ]

    if grow != 0:
        cuts = [ pathedit.grow(p, grow) for p in cuts ]

    if flip_y:
        cuts = [ pathedit.flip_y(p) for p in cuts ]
        engravings = [ pathedit.flip_y(p) for p in engravings ]

    x, y, w, h = box(cuts+engravings)

    global cur_x, cur_y, next_y
    if cur_x != 0 and cur_x + pad_x + w > max_x:
        cur_x, cur_y = 0, next_y

    svg.start_group(cur_x-x, cur_y-y)
    outside_cuts = [ p for i,p in enumerate(cuts) if not inside_out[i] ]
    inside_cuts  = [ p for i,p in enumerate(cuts) if     inside_out[i] ]

    for shape, color in ( (engravings,   "#00ff00"),
                          (inside_cuts,  "#0000ff"),
                          (outside_cuts, "#000000") ):
        if len(shape) > 0:
            svg.path( shape, color=color )

    if text != None:
        svg.unsafe_text(text, x=x+w/2, y=y+h/2, color='#ff0000')
    svg.end_group()
    cur_x += math.ceil(w + pad_x)
    next_y = max(next_y, math.ceil(cur_y+pad_y+h))



import math

import svg, pathedit

pad_x, pad_y = 3, 3
cur_x, cur_y = 0, 0
next_y = 0
max_x = 600
grow = .3/2

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

def plot(paths, text=None):
    if grow != 0:
        paths = [ pathedit.grow(p, grow) for p in paths ]
    x, y, w, h = box(paths)

    global cur_x, cur_y, next_y
    if cur_x != 0 and cur_x + pad_x + w > max_x:
        cur_x, cur_y = 0, next_y

    svg.start_group(cur_x-x, cur_y-y)
    svg.path(paths)
    if text != None:
        svg.unsafe_text(text, x=x+w/2, y=y+h/2, color='#ff0000')
    svg.end_group()
    cur_x += math.ceil(w + pad_x)
    next_y = max(next_y, math.ceil(cur_y+pad_y+h))


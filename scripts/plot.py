
import math

import svg

pad_x, pad_y = 3, 3
cur_x, cur_y = 0, 0
next_y = 0
max_x = 600

def box(points):
    x, y = min(x for x,_ in points), min(y for _,y in points)
    return ( x, y, max(x for x,_ in points) - x, max(y for _,y in points) - y )

def start(margin=3, width=600, height=400):
    global pad_x, pad_y, max_x
    pad_x, pad_y = margin, margin
    max_x = width
    svg.header(width, height)

def end():
    svg.footer()

def plot(points):
    global cur_x, cur_y, next_y
    x, y, w, h = box(points)
    if cur_x != 0 and cur_x + pad_x + w > max_x:
        cur_x, cur_y = 0, next_y
    svg.path(points, cur_x-x, cur_y-y)
    cur_x += math.ceil(w + pad_x)
    next_y = max(next_y, math.ceil(cur_y+pad_y+h))


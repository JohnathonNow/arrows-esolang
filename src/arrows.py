#!/usr/bin/env python3
from PIL import Image
import sys
img = Image.open(sys.argv[1])
w, h = img.size
arr = img.load()
data = [[arr[x, y][0] > 100 for x in range(w)] for y in range(h)]

DIRS = set(((0, 1), (0, -1), (-1, 0), (1, 0)))

def reo(u, v):
    return (u[0]*v[0]+u[0]*v[1], u[1]*v[0]+u[1]*v[1])

def find_start(d):
    for y in range (1, len(d)-1):
        for x in range(1, len(d[y])-1):
            if d[y-1][x-1:x+2] == [True, True, False]  and \
               d[y-0][x-1:x+2] == [True, False, False] and \
               d[y+1][x-1:x+2] == [True, True, False]:
                return (x, y)

def get_paths(d, x, y):
    return [di for di in DIRS if d[y+di[1]][x+di[0]]]

def get_turns(di):
    return [(tuple(-x for x in i[::-1]), i[::-1]) for i in di]

def is_at_arrow(d, x, y, di):
    ti = get_turns(di)
    return [d[y+t[0][1]][x+t[0][0]] and d[y+t[1][1]][x+t[1][0]] for t in ti]
        
def is_at_in(d, x, y, di):
    ti = get_turns(di)
    return [not d[y+t[0][1]][x+t[0][0]] and not d[y+t[1][1]][x+t[1][0]] for t in ti]

def is_at_out(d, x, y, di):
    ti = get_turns(di)
    x -= di[0][0]
    y -= di[0][1]
    return [not d[y+t[0][1]*2][x+t[0][0]*2] and not d[y+t[1][1]*2][x+t[1][0]*2] for t in ti]

def is_at_turn(d, x, y, di):
    ti = get_turns(di)
    return [(d[y+t[0][1]][x+t[0][0]] or d[y+t[1][1]][x+t[1][0]]) and not d[y+di[0][1]][x+di[0][0]] for t in ti]

def get_skip(x, y, di):
    return [(x + i[0]*3, y + i[1]*3) for i in di]


x, y = find_start(data)
x += 2 #skip into arrow
p = get_paths(data, x, y)
M = 'a'
while True:
    while not is_at_arrow(data, x, y, p)[0]:
        x += p[0][0]
        y += p[0][1]
    if is_at_out(data, x, y, p)[0]:
        sys.stdout.write(M)
    x, y = get_skip(x, y, p)[0]
    while data[y][x]:
        if is_at_in(data, x, y, p)[0]:
            M = sys.stdin.read(1)
        x += p[0][0]
        y += p[0][1]
    x += p[0][0]
    y += p[0][1]
    p = get_paths(data, x, y)

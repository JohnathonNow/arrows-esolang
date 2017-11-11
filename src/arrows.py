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
                return (x + 2, y)

def get_paths(d, x, y):
    return [di for di in DIRS if d[y+di[1]][x+di[0]]]

def rhr(di):
    return (di[1], -di[0])

def lhr(di):
    return (-di[1], di[0])

def get_path(di, register):
    if register == 0:
        return rhr(di)
    else:
        return lhr(di)

def get_turns(di):
    return (tuple(-x for x in di[::-1]), di[::-1])

def get_turn(di, register):
    if register == 0:
        return tuple(-x for x in di[::-1])
    else:
        return di[::-1]

def is_at_arrow(d, x, y, di):
    t = get_turns(di)
    return d[y+t[0][1]][x+t[0][0]] and d[y+t[1][1]][x+t[1][0]]
        
def is_at_in(d, x, y, di):
    t = get_turns(di)
    return not d[y+t[0][1]][x+t[0][0]] and not d[y+t[1][1]][x+t[1][0]]

def is_at_out(d, x, y, di):
    t = get_turns(di)
    x -= di[0]
    y -= di[1]
    return not d[y+t[0][1]*2][x+t[0][0]*2] and not d[y+t[1][1]*2][x+t[1][0]*2]

def is_at_turn(d, x, y, di):
    t = get_turns(di)
    return (d[y+t[0][1]][x+t[0][0]] or d[y+t[1][1]][x+t[1][0]]) and not d[y+di[1]][x+di[0]]

def get_skip(x, y, di):
    return (x + di[0]*3, y + di[1]*3)

def check_paths(d, xx, yy, di):
    out = []
    for p in di:
        x = xx
        y = yy
        pp = p
        while d[y][x]:
            x += p[0]
            y += p[1]
            if is_at_turn(d, x, y, p):
                p = get_paths(d, x, y)[0]
            if is_at_arrow(d, x, y, p):
                out.append(pp)
                break
    return out

def in_bounds(x, y, d):
    return y >= 0 and y < len(d) and x >= 0 and x < len(d[0])



x, y = find_start(data)
stack = [0]
memory = {}
register = 0
try:
    while in_bounds(x, y, data):
        pp = get_paths(data, x, y)
        pp = check_paths(data, x, y, pp)
        if len(pp) == 2:
            p = get_path(p, register)
        else:
            p = pp[0]
        pathy = 0
        while not is_at_arrow(data, x, y, p):
            x += p[0]
            y += p[1]
            pathy += 1
            if pathy == 5:
                pathy = 0
                register += 1
            if is_at_turn(data, x, y, p):
                pathy = 0
                p = get_paths(data, x, y)[0]
                if p == (0, 1):
                    register -= stack.pop()
                elif p == (0, -1):
                    stack.append(register)
                elif p == (1, 0):
                    stack.append(memory.get(register, 0))
                elif p == (-1, 0):
                    memory[register] = stack.pop()
                if len(stack) == 0:
                    stack.append(0)

        if is_at_out(data, x, y, p):
            sys.stdout.write(chr(register))
            sys.stdout.flush()
        x, y = get_skip(x, y, p)
        while data[y][x]:
            if is_at_in(data, x, y, p):
                register = ord(sys.stdin.read(1))
            x += p[0]
            y += p[1]
        x += p[0]
        y += p[1]
except Exception as E:
    print(E)
    

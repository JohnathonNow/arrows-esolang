from PIL import Image
import sys
import pkg_resources
import tempfile

#the four cardinal directions
DIRS = set(((0, 1), (0, -1), (-1, 0), (1, 0)))

def write_library():
    lib = pkg_resources.resource_string(__name__, '/library.c')
    f = tempfile.NamedTemporaryFile(suffix='.c')
    f.write(lib)
    f.flush()
    return f

def get_outfile():
    f = tempfile.NamedTemporaryFile(suffix='.s')
    return f

def instruction(out, s, *f):
    if f:
        out.write(s.format(*f).encode())
    else:
        out.write(s.encode())
    out.write(b'\n')
    out.flush()

def find_start(d):
    """finds the starting location for the program"""
    for y in range (1, len(d)-1):
        for x in range(1, len(d[y])-1):
            if d[y-1][x-1:x+2] == [True, True, False]  and \
               d[y-0][x-1:x+2] == [True, False, False] and \
               d[y+1][x-1:x+2] == [True, True, False]:
                return (x + 2, y)

def get_paths(d, x, y):
    """finds which directions we can go from our current location"""
    return [di for di in DIRS if d[y+di[1]][x+di[0]]]

def rhr(di):
    """right hand rule - finds the new vector with the same magnitude as di but rotated counter clockwise"""
    return (di[1], -di[0])

def lhr(di):
    """right hand rule - finds the new vector with the same magnitude as di but rotated clockwise"""
    return (-di[1], di[0])

def get_path_at_fork(di, register):
    """called when we are at a fork with two options, and follows the correct path based off the value of register"""
    if register == 0:
        return rhr(di)
    else:
        return lhr(di)

def get_paths_turn(d, x, y, p):
    """finds which direction we can go from a turn"""
    return [di for di in DIRS if d[y+di[1]][x+di[0]] and ((di[0] != -p[0]) and (di[1] !=  -p[1]))]

def get_turns(di):
    """get both possible turns for a given vector (left and right)"""
    return (tuple(-x for x in di[::-1]), di[::-1])

def is_at_arrow(d, x, y, di):
    """get if the location (x, y) heading in direction di is at an arrow head"""
    t = get_turns(di)
    return d[y+t[0][1]][x+t[0][0]] and d[y+t[1][1]][x+t[1][0]]
        
def is_at_in(d, x, y, di):
    """get if the location (x, y) heading in direction di is at an input arrow tail"""
    t = get_turns(di)
    return not d[y+t[0][1]][x+t[0][0]] and not d[y+t[1][1]][x+t[1][0]]

def is_at_out(d, x, y, di):
    """get if the location (x, y) heading in direction di is at an output arrow head"""
    t = get_turns(di)
    x -= di[0]
    y -= di[1]
    return not d[y+t[0][1]*2][x+t[0][0]*2] and not d[y+t[1][1]*2][x+t[1][0]*2]

def is_at_turn(d, x, y, di):
    """get if the location (x, y) heading in direction di is at a change of direction"""
    t = get_turns(di)
    return (d[y+t[0][1]][x+t[0][0]] or d[y+t[1][1]][x+t[1][0]]) and not d[y+di[1]][x+di[0]]

def get_skip(x, y, di):
    """calculates a new (x, y) pair for after an arrow head"""
    return (x + di[0]*3, y + di[1]*3)

def check_paths(d, xx, yy, di):
    """get all possible directions from (x, y) in di that we can follow to an arrow head"""
    out = []
    for p in di:
        x = xx
        y = yy
        pp = p
        while d[y][x]:
            x += p[0]
            y += p[1]
            if is_at_turn(d, x, y, p):
                p = get_paths_turn(d, x, y, p)[0]
            if is_at_arrow(d, x, y, p):
                out.append(pp)
                break
    return out

def in_bounds(x, y, d):
    """get whether (x, y) is in bounds, where d is the image data"""
    return y >= 0 and y < len(d) and x >= 0 and x < len(d[0])

def load(f):
    """loads in the data map for an arrows program"""
    img = Image.open(f)
    w, h = img.size
    arr = img.load()

    return [[arr[x, y][0] > 100 for x in range(w)] for y in range(h)]

def run(f):
    """runs an arrows program"""
    data = load(f)
    x, y = find_start(data)
    lstack = [0]
    rstack = [0]
    register = 0
    try:
        while in_bounds(x, y, data):
            pp = get_paths(data, x, y)
            pp = check_paths(data, x, y, pp)
            if len(pp) == 2:
                p = get_path_at_fork(p, register)
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
                    p = get_paths_turn(data, x, y, p)[0]
                    if p == (1, 0):
                        register -= rstack.pop()
                    elif p == (0, 1):
                        rstack.append(register)
                    elif p == (-1, 0):
                        register -= lstack.pop()
                    elif p == (0, -1):
                        lstack.append(register)
                    if len(rstack) == 0:
                        rstack.append(0)
                    if len(lstack) == 0:
                        lstack.append(0)

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
    


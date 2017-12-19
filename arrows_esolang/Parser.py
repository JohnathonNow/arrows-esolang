from arrows_esolang.util import *
from arrows_esolang.Statement import *
from arrows_esolang.Action import *

def parse(source):
    data = load(source)
    x, y = find_start(data)
    p = get_paths(data, x, y)
    p = check_paths(data, x, y, p)
    visited = {}

    def _parse(x, y, p, pp=None):
        if (x, y, p) in visited: 
            return visited[(x, y, p)]

        register = 0
        me = Statement()
        visited[(x, y, p)] = me

        if not pp:
            pp = get_paths(data, x, y)
            pp = check_paths(data, x, y, pp)

        if len(pp) == 2:
            me.kind = NodeType.CONDITIONAL
            me.if_zero = _parse(x, y, rhr(p), [rhr(p)])
            me.if_else = _parse(x, y, lhr(p), [lhr(p)])
            return me

        p = pp[0]
        me.kind = NodeType.ACTION
        register = 0
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
                    me.add_action(ActionType.SUBTRACT_RIGHT, register)
                    register = 0
                elif p == (0, -1):
                    me.add_action(ActionType.PUSH_LEFT, register)
                    register = 0
                elif p == (-1, 0):
                    me.add_action(ActionType.SUBTRACT_LEFT, register)
                    register = 0
                elif p == (0, 1):
                    me.add_action(ActionType.PUSH_RIGHT, register)
                    register = 0

        if is_at_out(data, x, y, p):
            me.add_action(ActionType.PRINT, register)
            register = 0
        x, y = get_skip(x, y, p)
        if not in_bounds(x, y, data):
            me.add_action(ActionType.END, register)
            register = 0
            return me
        while data[y][x]:
            if is_at_in(data, x, y, p):
                me.add_action(ActionType.READ, register)
                register = 0
            if not in_bounds(x, y, data):
                me.add_action(ActionType.END, register)
                register = 0
                return me
            x += p[0]
            y += p[1]
        x += p[0]
        y += p[1]
        if not in_bounds(x, y, data):
            me.add_action(ActionType.END, register)
            register = 0
            return me
        me.add_add(register)
        me.next = _parse(x, y, p)
        return me
    p = _parse(x, y, p[0])
    return (p, visited)

import arrows_esolang.Util as U
import arrows_esolang.Statement as S
import arrows_esolang.Action as A


def parse(source):
    data = U.load(source)
    x, y = U.find_start(data)
    p = U.get_paths(data, x, y)
    p = U.check_paths(data, x, y, p)
    visited = {}

    def _parse(x, y, p, pp=None):
        if (x, y, p) in visited:
            return visited[(x, y, p)]

        register = 0
        me = S.Statement()
        visited[(x, y, p)] = me

        if not pp:
            pp = U.get_paths(data, x, y)
            pp = U.check_paths(data, x, y, pp)

        if len(pp) == 2:
            me.kind = S.NodeType.CONDITIONAL
            me.if_zero = _parse(x, y, U.rhr(p), [U.rhr(p)])
            me.if_else = _parse(x, y, U.lhr(p), [U.lhr(p)])
            return me

        p = pp[0]
        me.kind = S.NodeType.ACTION
        register = 0
        pathy = 0
        while not U.is_at_arrow(data, x, y, p):
            x += p[0]
            y += p[1]
            pathy += 1
            if pathy == 5:
                pathy = 0
                register += 1
            if U.is_at_turn(data, x, y, p):
                pathy = 0
                p = U.get_paths_turn(data, x, y, p)[0]
                if p == (1, 0):
                    me.add_action(A.ActionType.SUBTRACT_RIGHT, register)
                    register = 0
                elif p == (0, -1):
                    me.add_action(A.ActionType.PUSH_LEFT, register)
                    register = 0
                elif p == (-1, 0):
                    me.add_action(A.ActionType.SUBTRACT_LEFT, register)
                    register = 0
                elif p == (0, 1):
                    me.add_action(A.ActionType.PUSH_RIGHT, register)
                    register = 0

        if U.is_at_out(data, x, y, p):
            me.add_action(A.ActionType.PRINT, register)
            register = 0
        x, y = U.get_skip(x, y, p)
        if not U.in_bounds(x, y, data):
            me.add_action(A.ActionType.END, register)
            register = 0
            return me
        while data[y][x]:
            if U.is_at_in(data, x, y, p):
                me.add_action(A.ActionType.READ, register)
                register = 0
            if not U.in_bounds(x, y, data):
                me.add_action(A.ActionType.END, register)
                register = 0
                return me
            x += p[0]
            y += p[1]
        x += p[0]
        y += p[1]
        if not U.in_bounds(x, y, data):
            me.add_action(U.ActionType.END, register)
            register = 0
            return me
        me.add_add(register)
        me.next = _parse(x, y, p)
        return me
    p = _parse(x, y, p[0])
    return (p, visited)

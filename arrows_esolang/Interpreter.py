import arrows_esolang.Util as U
import arrows_esolang.Action as A
import sys


def interpret(prog):
    register = 0
    lstack = [0]
    rstack = [0]
    while True:
        if prog.kind == A.NodeType.CONDITIONAL:
            if register == 0:
                prog = prog.if_zero
            else:
                prog = prog.if_else
        else:
            for a in prog.actions:
                if a.kind == U.ActionType.END:
                    sys.exit(register)
                elif a.kind == A.ActionType.ADD:
                    register += a.value
                elif a.kind == A.ActionType.PUSH_LEFT:
                    lstack.append(register)
                elif a.kind == A.ActionType.PUSH_RIGHT:
                    rstack.append(register)
                elif a.kind == A.ActionType.SUBTRACT_LEFT:
                    register -= lstack.pop()
                    if not lstack:
                        lstack.append(0)
                elif a.kind == A.ActionType.SUBTRACT_RIGHT:
                    register -= rstack.pop()
                    if not rstack:
                        rstack.append(0)
                elif a.kind == A.ActionType.PRINT:
                    sys.stdout.write(chr(register))
                    sys.stdout.flush()
                elif a.kind == A.ActionType.READ:
                    read = sys.stdin.read(1)
                    if read:
                        register = ord(read)
                    else:
                        register = 0
                    del read
            prog = prog.next

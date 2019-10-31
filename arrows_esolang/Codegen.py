import subprocess
import arrows_esolang.Util as U
import arrows_esolang.Statement as S
import arrows_esolang.Action as A


def codegen(visited, name):
    out = U.get_outfile()

    U.instruction(out, '.global main')
    U.instruction(out, 'main:')
    U.instruction(out, 'MOV $0, %rbx')
    U.instruction(out, 'JMP .L0')

    for key in visited:
        s = visited[key]
        label = '.L{}'.format(s.label)
        U.instruction(out, '{}:', label)
        if s.kind == S.NodeType.CONDITIONAL:
            U.instruction(out, 'CMP $0, %rbx')
            U.instruction(out, 'JE .L{}', s.if_zero.label)
            U.instruction(out, 'JMP .L{}', s.if_else.label)
        else:
            for a in s.actions:
                if a.kind == A.ActionType.END:
                    U.instruction(out, 'MOV %rbx, %rax')
                    U.instruction(out, 'JMP .END')
                elif a.kind == A.ActionType.ADD:
                    U.instruction(out, 'ADD ${}, %rbx', a.value)
                elif a.kind == A.ActionType.PUSH_LEFT:
                    U.instruction(out, 'MOV %rbx, %rdi')
                    U.instruction(out, 'CALL lpush')
                elif a.kind == A.ActionType.PUSH_RIGHT:
                    U.instruction(out, 'MOV %rbx, %rdi')
                    U.instruction(out, 'CALL rpush')
                elif a.kind == A.ActionType.SUBTRACT_LEFT:
                    U.instruction(out, 'CALL lpop')
                    U.instruction(out, 'SUB %rax, %rbx')
                elif a.kind == A.ActionType.SUBTRACT_RIGHT:
                    U.instruction(out, 'CALL rpop')
                    U.instruction(out, 'SUB %rax, %rbx')
                elif a.kind == A.ActionType.PRINT:
                    U.instruction(out, 'MOV %rbx, %rdi')
                    U.instruction(out, 'CALL putchar')
                elif a.kind == A.ActionType.READ:
                    U.instruction(out, 'CALL libgetchar')
                    U.instruction(out, 'MOV %rax, %rbx')
            if s.next:
                U.instruction(out, 'JMP .L{}', s.next.label)
    U.instruction(out, '.END:')
    U.instruction(out, 'ret')
    out.flush()

    lib = U.write_library()

    subprocess.call(['gcc', out.name, lib.name, '-static', '-o', name])

    out.close()
    lib.close()

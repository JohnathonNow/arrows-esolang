import subprocess
from arrows_esolang.util import *
from arrows_esolang.Statement import *
from arrows_esolang.Action import *

def codegen(visited, name):
    out = get_outfile()

    instruction(out, '.global main')
    instruction(out, 'main:')
    instruction(out, 'MOV $0, %rbx')
    instruction(out, 'JMP .L0')

    for key in visited:
        s = visited[key]
        label = '.L{}'.format(s.label)
        instruction(out, '{}:', label)
        if s.kind == NodeType.CONDITIONAL:
            instruction(out, 'CMP $0, %rbx')
            instruction(out, 'JE .L{}', s.if_zero.label)
            instruction(out, 'JMP .L{}', s.if_else.label)
        else:
            for a in s.actions:
                if a.kind == ActionType.END:
                    instruction(out, 'MOV %rbx, %rax')
                    instruction(out, 'JMP .END')
                elif a.kind == ActionType.ADD:
                    instruction(out, 'ADD ${}, %rbx', a.value)
                elif a.kind == ActionType.PUSH_LEFT:
                    instruction(out, 'MOV %rbx, %rdi')
                    instruction(out, 'CALL lpush')
                elif a.kind == ActionType.PUSH_RIGHT:
                    instruction(out, 'MOV %rbx, %rdi')
                    instruction(out, 'CALL rpush')
                elif a.kind == ActionType.SUBTRACT_LEFT:
                    instruction(out, 'CALL lpop')
                    instruction(out, 'SUB %rax, %rbx')
                elif a.kind == ActionType.SUBTRACT_RIGHT:
                    instruction(out, 'CALL rpop')
                    instruction(out, 'SUB %rax, %rbx')
                elif a.kind == ActionType.PRINT:
                    instruction(out, 'MOV %rbx, %rdi')
                    instruction(out, 'CALL putchar')
                elif a.kind == ActionType.READ:
                    instruction(out, 'CALL libgetchar')
                    instruction(out, 'MOV %rax, %rbx')
            if s.next:
                instruction(out, 'JMP .L{}', s.next.label)
    instruction(out, '.END:')
    instruction(out, 'ret')
    out.flush()

    lib = write_library()

    subprocess.call(['gcc', out.name, lib.name, '-static', '-o', name])

    out.close()
    lib.close()

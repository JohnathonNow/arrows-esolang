import subprocess
import shutil
import arrows_esolang.Util as U
import arrows_esolang.Statement as S
import arrows_esolang.Action as A


def optimize(insts):
    changed = True
    while changed:
        changed = False

        # 1. Resolve jumps to jumps
        labels = {}
        for i, inst in enumerate(insts):
            if inst.endswith(':'):
                labels[inst[:-1]] = i

        for i in range(len(insts)):
            if insts[i].startswith('JMP '):
                target = insts[i][4:]
                if target in labels:
                    target_idx = labels[target]
                    # Check if target is just a label to another jump
                    next_inst_idx = target_idx + 1
                    while next_inst_idx < len(insts) and insts[next_inst_idx].endswith(':'):
                        next_inst_idx += 1
                    if next_inst_idx < len(insts) and insts[next_inst_idx].startswith('JMP '):
                        new_target = insts[next_inst_idx][4:]
                        if new_target != target:
                            insts[i] = 'JMP ' + new_target
                            changed = True

        # 2. Remove useless jumps
        labels = {}
        for i, inst in enumerate(insts):
            if inst.endswith(':'):
                labels[inst[:-1]] = i

        i = 0
        while i < len(insts) - 1:
            if insts[i].startswith('JMP '):
                target = insts[i][4:]
                if target in labels:
                    target_idx = labels[target]
                    # If the jump points to the very next instruction
                    if target_idx > i:
                        all_labels = True
                        for j in range(i + 1, target_idx + 1):
                            if not insts[j].endswith(':'):
                                all_labels = False
                                break
                        if all_labels:
                            insts.pop(i)
                            changed = True
                            continue
            i += 1

        # 3. Combine ADD instructions
        i = 0
        while i < len(insts) - 1:
            if insts[i].startswith('ADD $') and insts[i].endswith(', %rbx'):
                if insts[i+1].startswith('ADD $') and insts[i+1].endswith(', %rbx'):
                    val1 = int(insts[i][5:-6])
                    val2 = int(insts[i+1][5:-6])
                    insts[i] = f'ADD ${val1+val2}, %rbx'
                    insts.pop(i+1)
                    changed = True
                    continue
            i += 1

        # 4. Remove ADD $0, %rbx
        i = 0
        while i < len(insts):
            if insts[i] == 'ADD $0, %rbx':
                insts.pop(i)
                changed = True
                continue
            i += 1

        # 5. Combine MOV and ADD
        i = 0
        while i < len(insts) - 1:
            if insts[i].startswith('MOV $') and insts[i].endswith(', %rbx'):
                if insts[i+1].startswith('ADD $') and insts[i+1].endswith(', %rbx'):
                    val1 = int(insts[i][5:-6])
                    val2 = int(insts[i+1][5:-6])
                    insts[i] = f'MOV ${val1+val2}, %rbx'
                    insts.pop(i+1)
                    changed = True
                    continue
            i += 1

        # 6. Optimize stack push/pop
        # MOV %rbx, %rdi; CALL lpush; CALL lpop; SUB %rax, %rbx
        # rpush / rpop
        i = 0
        while i < len(insts) - 3:
            if insts[i] == 'MOV %rbx, %rdi' and insts[i+1] == 'CALL lpush' and insts[i+2] == 'CALL lpop' and insts[i+3] == 'SUB %rax, %rbx':
                insts[i] = 'MOV $0, %rbx'
                insts.pop(i+1)
                insts.pop(i+1)
                insts.pop(i+1)
                changed = True
                continue
            if insts[i] == 'MOV %rbx, %rdi' and insts[i+1] == 'CALL rpush' and insts[i+2] == 'CALL rpop' and insts[i+3] == 'SUB %rax, %rbx':
                insts[i] = 'MOV $0, %rbx'
                insts.pop(i+1)
                insts.pop(i+1)
                insts.pop(i+1)
                changed = True
                continue
            i += 1

        # 7. Remove unused labels
        used_labels = set()
        for inst in insts:
            if inst.startswith('JMP '):
                used_labels.add(inst[4:])
            elif inst.startswith('JE '):
                used_labels.add(inst[3:])

        # main is always used, though it doesn't have a JMP to it
        used_labels.add('main')

        i = 0
        while i < len(insts):
            if insts[i].endswith(':'):
                label = insts[i][:-1]
                if label not in used_labels and label != '.END':
                    insts.pop(i)
                    changed = True
                    continue
            i += 1

    return insts

def codegen(visited):
    out = U.get_outfile()
    insts = []

    def inst(s, *f):
        if f:
            insts.append(s.format(*f))
        else:
            insts.append(s)

    inst('.global main')
    inst('main:')
    inst('MOV $0, %rbx')
    inst('JMP .L0')

    for key in visited:
        s = visited[key]
        label = '.L{}'.format(s.label)
        inst('{}:', label)
        if s.kind == S.NodeType.CONDITIONAL:
            inst('CMP $0, %rbx')
            inst('JE .L{}', s.if_zero.label)
            inst('JMP .L{}', s.if_else.label)
        else:
            for a in s.actions:
                if a.kind == A.ActionType.END:
                    inst('MOV %rbx, %rax')
                    inst('JMP .END')
                elif a.kind == A.ActionType.ADD:
                    inst('ADD ${}, %rbx', a.value)
                elif a.kind == A.ActionType.PUSH_LEFT:
                    inst('MOV %rbx, %rdi')
                    inst('CALL lpush')
                elif a.kind == A.ActionType.PUSH_RIGHT:
                    inst('MOV %rbx, %rdi')
                    inst('CALL rpush')
                elif a.kind == A.ActionType.SUBTRACT_LEFT:
                    inst('CALL lpop')
                    inst('SUB %rax, %rbx')
                elif a.kind == A.ActionType.SUBTRACT_RIGHT:
                    inst('CALL rpop')
                    inst('SUB %rax, %rbx')
                elif a.kind == A.ActionType.PRINT:
                    inst('MOV %rbx, %rdi')
                    inst('CALL putchar')
                elif a.kind == A.ActionType.READ:
                    inst('CALL libgetchar')
                    inst('MOV %rax, %rbx')
            if s.next:
                inst('JMP .L{}', s.next.label)
    inst('.END:')
    inst('ret')

    insts = optimize(insts)

    for i in insts:
        U.instruction(out, i)

    out.flush()
    return out


def compile(visited, name):
    out = codegen(visited)
    lib = U.write_library()
    subprocess.call(['gcc', out.name, lib.name, '-static', '-o', name])
    out.close()
    lib.close()


def asm(visited, name):
    out = codegen(visited)
    shutil.copyfile(out.name, name)
    out.close()

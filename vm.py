from dataclasses import dataclass
from sys import stdin, stdout
import struct

INC = '+'
DEC = '-'
LEFT = '<'
RIGHT = '>'
WRITE = '.'
READ = ','
JMP_ZERO = '['
JMP_NZERO = ']'

data = [0] * (2 << 20)
dc: int = 0

program = []
pc: int = 0

@dataclass
class Op:
    op: int
    arg: int | None = None

    def encode(self):
        if self.op in [ord(c) for c in [INC, DEC, LEFT, RIGHT, WRITE, READ]]:
            return struct.pack('>B', self.op)
        elif self.op in [ord(c) for c in [JMP_ZERO, JMP_NZERO]]:
            return struct.pack('>BQ', self.op, self.arg)


def step():
    global data
    global dc
    global program
    global pc

    assert pc < len(program)

    # fetch
    inst = program[pc]
    pc += 1

    # execute
    if inst.op == ord(INC):
        data[dc] += 1
        data[dc] %= 0xff
    elif inst.op == ord(DEC):
        data[dc] -= 1
        data[dc] %= 0xff
    elif inst.op == ord(LEFT):
        dc -= 1
        dc %= len(data)
    elif inst.op == ord(RIGHT):
        dc += 1
        dc %= len(data)
    elif inst.op == ord(WRITE):
        stdout.write(chr(data[dc]))
    elif inst.op == ord(READ):
        data[dc] = ord(stdin.read(1)) % 0xff
    elif inst.op == ord(JMP_ZERO):
        if data[dc] == 0:
            pc = inst.arg
    elif inst.op == ord(JMP_NZERO):
        if data[dc] != 0:
            pc = inst.arg
    else:
        raise ValueError(f"invalid intruction {inst}")

def run():
    while pc < len(program):
        step()

def compile(source: str) -> list[Op]:
    tokens = [ c for c in source if c in '+-<>,.[]' ] # tokenizer

    back_patch_stack = []
    result: list[Op] = []

    for addr, char in enumerate(tokens):
        match char:
            case '+' | '-' | '<' | '>' | '.' | ',':
                result.append(Op(op=ord(char)))
            case '[':
                back_patch_stack.append(addr)
                result.append(Op(op=ord(JMP_ZERO)))
            case ']':
                pair = back_patch_stack.pop()
                result[pair].arg = addr
                result.append(Op(op=ord(JMP_NZERO), arg=pair))

    return result

def compile_file(path: str) -> list[Op]:
    with open(path, 'r') as f:
        return compile_bf(f.read())

def encode(source: str) -> bytes:
    ops = compile_bf(source)

    return b''.join([op.encode() for op in ops])

hello = '''
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
'''

program = compile(hello)
run()

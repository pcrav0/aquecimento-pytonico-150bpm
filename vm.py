from dataclasses import dataclass
from sys import stdin, stdout

INC = '+'
DEC = '-'
LEFT = '<'
RIGHT = '>'
WRITE = '.'
READ = ','
JMP_ZERO = '['
JMP_NZERO = ']'

@dataclass
class Op:
    op: int
    arg: int | None = None

@dataclass
class Machine:
    data = [0] * (2 << 20)
    dc: int = 0

    program = []
    pc: int = 0

    def step(self):
        assert self.pc < len(self.program)

        # fetch
        inst = self.program[self.pc]
        self.pc += 1

        # execute
        if inst.op == ord(INC):
            self.data[self.dc] += 1
            self.data[self.dc] %= 0xff
        elif inst.op == ord(DEC):
            self.data[self.dc] -= 1
            self.data[self.dc] %= 0xff
        elif inst.op == ord(LEFT):
            self.dc -= 1
            self.dc %= len(self.data)
        elif inst.op == ord(RIGHT):
            self.dc += 1
            self.dc %= len(self.data)
        elif inst.op == ord(WRITE):
            stdout.write(chr(self.data[self.dc]))
        elif inst.op == ord(READ):
            self.data[self.dc] = ord(stdin.read(1)) % 0xff
        elif inst.op == ord(JMP_ZERO):
            if self.data[self.dc] == 0:
                self.pc = inst.arg
        elif inst.op == ord(JMP_NZERO):
            if self.data[self.dc] != 0:
                self.pc = inst.arg
        else:
            raise ValueError(f"invalid intruction {inst}")

    def run(self):
        while self.pc < len(self.program):
            self.step()

def compile_bf(source: str) -> list[Op]:
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

hello = '''
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
'''

# with open('life.b') as f:
#     program = compile_bf(f.read())

program = compile_bf(hello)

machine = Machine()
machine.program = program
machine.run()

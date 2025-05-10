from enum import Enum, auto
from dataclasses import dataclass

@dataclass
class Machine:
    program = []
    memory = [0] * 1024 * 1024
    stack = [0] * 1024 * 1024
    sp = 0 # stack pointer

    # regs
    dc = 0 # data counter
    pc = 0 # program counter

    # flag
    halt = 0

    def push(self, n):
        self.stack[self.sp] = n
        self.sp += 1

    def pop(self):
        self.sp -= 1
        return self.stack[self.sp]

    def step(self): # cpu cycle
        inst = self.program[self.pc]

        if inst == ins('halt'):
            self.halt = True
        elif inst == ins('left'):
            self.dc -= 1
            self.dc %= len(self.memory)
            self.pc += 1
        elif inst == ins('right'):
            self.dc += 1
            self.dc %= len(self.memory)
            self.pc += 1
        elif inst == ins('inc'):
            self.memory[self.dc] += 1
            self.memory[self.dc] %= 0xff
            self.pc += 1
        elif inst == ins('dec'):
            self.memory[self.dc] -= 1
            self.memory[self.dc] %= 0xff
            self.pc += 1
        elif inst == ins('int_input'):
            self.memory[self.dc] = int(input())
            self.pc += 1
        elif inst == ins('int_output'):
            n = self.memory[self.dc]
            print(f"{chr(n)}", end='')
            self.pc += 1
        elif inst == ins('int_output_int'):
            n = self.memory[self.dc]
            print(f"{n}")
            self.pc += 1
        elif inst == ins('block_start'):
            self.push(self.pc)
            self.pc += 1
        elif inst == ins('block_end'):
            if self.memory[self.dc] != 0:
                self.pc = self.pop()
            else:
                self.pc += 1
        else:
            raise ValueError(f"undefined instruction {Insts_Type(inst).name}")

        self.pc %= len(self.program)

class Insts_Type(Enum):
    halt = 0

    left = auto()
    right = auto()

    inc = auto()
    dec = auto()

    block_start = auto()
    block_end = auto()

    int_input = auto()
    int_output = auto()
    int_output_int = auto()

def ins(name):
    return Insts_Type[name].value


def compile_bf(program: str):
    result = []

    for c in program:
        match c:
            case '+':
                result.append(ins('inc'))
            case '-':
                result.append(ins('dec'))
            case '>':
                result.append(ins('left'))
            case '<':
                result.append(ins('right'))
            case '[':
                result.append(ins('block_start'))
            case ']':
                result.append(ins('block_end'))
            case '.':
                result.append(ins('int_output'))
            case ':':
                result.append(ins('int_output_int'))
            case ',':
                result.append(ins('int_input'))
            case '!':
                result.append(ins('halt'))
            case _:
                raise ValueError(f"malformed program, invalid instruction '{c}'")

    return result

machine = Machine()
counter = '++++++++++++++++++++++++++++++++++>+++++++++++++++++++++++++++++++++++[<+>-]<:!'

def l2bf(c):
    return ord(c) * '+'

hello = l2bf('h') + '.>' + l2bf('e') + '.!'
bf = hello
program = compile_bf(bf)

with open('bf.bin', 'wb') as f:
    f.write(bytes(program))

def main():
    with open('bf.bin', 'rb') as f:
        machine.program = list(f.read())

    while not machine.halt:
        machine.step()
    print()

if __name__ == '__main__':
    main()

from dataclasses import dataclass
from enum import Enum, auto

class Inst(Enum):
    inc = auto()
    dec = auto()
    left = auto()
    right = auto()
    byte_get = auto()
    byte_put = auto()
    block_start = auto()
    block_end = auto()

@dataclass
class State:
    stack = []

    memory = [0] * 1024
    pointer = 0

    program = ''
    pc = 0

    def inc(self): # +
        self.memory[self.pointer] += 1
        self.memory[self.pointer] %= 0xff
        self.next()

    def dec(self): # -
        self.memory[self.pointer] -= 1
        self.memory[self.pointer] %= 0xff
        self.next()

    def right(self): # >
        self.pointer += 1
        self.pointer %= len(self.memory)
        self.next()

    def left(self): # <
        self.pointer -= 1
        self.pointer %= len(self.memory)
        self.next()

    def get_byte(self): # .
        self.memory[self.pointer] = ord(input())
        self.next()

    def put_byte(self): # ,
        print(chr(self.memory[self.pointer]), end='')
        self.next()

    def block_start(self): # [
        self.push()
        self.next()

    def block_end(self): # ]
        if self.memory[self.pointer] != 0:
            self.pop()
        else:
            self.next()

    def push(self):
        self.stack.append(self.pc)

    def pop(self):
        self.pc = self.stack.pop()

    def next(self):
        self.pc += 1

    def step(self):
        match self.program[self.pc]:
            case '+': self.inc()
            case '-': self.dec()
            case '<': self.left()
            case '>': self.right()
            case '.': self.put_byte()
            case ',': self.get_byte()
            case '[': self.block_start()
            case ']': self.block_end()
            case _: self.next()

    def run(self):
        while self.pc < len(self.program):
            self.step()

state = State()
state.program = '''
++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
'''
state.run()
print()

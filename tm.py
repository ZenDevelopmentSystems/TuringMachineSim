#!/usr/bin/env python
from enum import Enum
from typing import List, Callable, Tuple
from copy import copy

class TMDirection(Enum):
    Left = -1
    Stay = 0
    Right = 1

class TMCrash(Exception):
    pass

class TuringMachine:

    special_states = ["accept", "reject"]

    def __init__(self, states: List[str],
             input_alphabet: List[str],
             tape_alphabet: List[str],
             initial_state: str,
             delta: Callable[[str, str], Tuple[str, str, TMDirection]]):
        self.states = states
        self.input_alphabet = input_alphabet
        self.tabe_alphabet = tape_alphabet
        self.initial_state = initial_state
        self.delta = delta

        # Check consistent
        if any(item not in tape_alphabet for item in input_alphabet):
            raise Exception("Input alphabet must be subset of tape alphabet")
        if '' not in tape_alphabet:
            raise Exception("Tape alphabet must include empty string")
        if '' in input_alphabet:
            raise Exception("Input alphabet must not include empty string")
        if any(required_state not in states for required_state in TuringMachine.special_states):
            raise Exception("States must include these: %s" % (TuringMachine.special_states))
        if initial_state in TuringMachine.special_states:
            raise Exception("Initial state cannot be any of these: %s" % (TuringMachine.special_states))

    def print_tape(self, tape: List[str], pos: int):
        my_tape = [s if s != "" else u"\u0394" for s in tape]
        lens = [len(s) for s in my_tape]
        sep = "|"
        print(sep.join(my_tape))
        cpos = sum(lens[0:pos]) + (pos * len(sep))
        print((" " * cpos) + "^")

    def run(self, input_sequence: List[str]) -> str:
        if any(symbol not in self.input_alphabet for symbol in input_sequence):
            raise Exception("Invalid input, unexpected symbols.")
        tape = copy(input_sequence)
        tape.insert(0, "")
        pos = 0
        state = self.initial_state
        try:
            while state not in TuringMachine.special_states:
                print("#" * 20)
                print("State: %s" % (state))
                self.print_tape(tape, pos)
                while pos >= len(tape):
                    # Tape is inifinite rightwards
                    tape.append('')
                new_state, new_val, step = self.delta(state, tape[pos])
                print("Replace symbol: %s" % (new_val))
                print("New state: %s" % (new_state))
                tape[pos] = new_val
                state = new_state
                pos += step.value
                if pos < 0:
                    # Tape is not inifinte leftwards
                    raise TMCrash
        except TMCrash:
            print("Tape head crashed")
            return state
        return state


# An example definition of a Turing Machine:
# will accept any input consisting of 'a' and 'b' that contains 'aa'

def delta(state: str, tape_symbol: str) -> Tuple[str, str, TMDirection]:
    if state == 'q0':
        if tape_symbol == '':
           return 'q1', '', TMDirection.Right
    if state == 'q1':
        if tape_symbol == 'b':
            return 'q1', 'b', TMDirection.Right
        if tape_symbol == 'a':
            return 'q2', 'a', TMDirection.Right
    if state == 'q2':
        if tape_symbol == 'b':
            return 'q1', 'b', TMDirection.Right
        if tape_symbol == 'a':
            return 'accept', 'a', TMDirection.Right
    return 'reject', tape_symbol, TMDirection.Stay

states = ["accept", "reject", "q0", "q1", "q2"]
input_alphabet = ["a", "b"]
tape_alphabet = [*input_alphabet, ""]
tm = TuringMachine(states, input_alphabet, tape_alphabet, "q0", delta)

print(tm.run(["b", "b", "a", "b", "a", "a"]))


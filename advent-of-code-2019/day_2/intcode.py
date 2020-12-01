#!/usr/bin/env python3
from copy import deepcopy
from typing import List

DEBUG = False
def print_log(msg):
    if DEBUG:
        print(msg)


class UnexpectedOpcode(Exception):
    
    def __init__(self, code: int, index: int):
        super().__init__(f"Non halt code exception encountered! Code: {code} at position: {index}")


class HaltCode(Exception):
    pass


class IntCode:
    CONTINUE_INSTRUCTION = [1, 2]  # these expect 4 params, 1st = opcode, 2-4th = params
    HALT_INSTRUCTION = [99]

    OPCODE_TO_METHOD = {
        1: lambda x, y: x + y,
        2: lambda x, y: x * y,
        99: UnexpectedOpcode,
    }

    INSTRUCTION_INCREMENT = {
            1: 4,
            2: 4,
            99: 1,
    }

    def __init__(self, memory: List[int]):
        self.memory = deepcopy(memory)
    
    def __process_instruction(self, opcode: int, op_index: int, *_, **__):
        param_1 = self.memory[op_index + 1]
        param_2 = self.memory[op_index + 2]
        param_3 = self.memory[op_index + 3]

        op_method = self.OPCODE_TO_METHOD[opcode]
        
        store_result = op_method(self.memory[param_1], self.memory[param_2])
        print_log(f"{param_1} {'+' if opcode == 1 else '*'} {param_2} = {store_result}\tin\t{param_3}")
        self.memory[param_3] = store_result

    def _process_code(self, index: int):
        code = self.memory[index]
        if code in self.CONTINUE_INSTRUCTION:
            self.__process_instruction(code, index)
        elif code in self.HALT_INSTRUCTION:
            raise HaltCode() 
        else:
            raise UnexpectedOpcode(code, index)

        return index + self.INSTRUCTION_INCREMENT[code]

    def read(self):
        instruction_pointer = 0
        finish = len(self.memory)
        while instruction_pointer < finish:
            try:
                instruction_pointer = self._process_code(instruction_pointer) 
            except HaltCode:
                return self.memory
        return self.memory


def get_puzzle_inputs():
    with open('input.txt' ,'r') as f:
        RAW_PUZZLE_INPUT = f.read()
    return [int(x) for x in RAW_PUZZLE_INPUT.split(",")]


PUZZLE_INPUTS = get_puzzle_inputs()


def io(noun, verb, puzzle_code):
    puzzle_code[1] = noun
    puzzle_code[2] = verb

    calculator = IntCode(puzzle_code)
    final_state = calculator.read()
    
    output = final_state[0]
    return output

def part_1():
    # restore to "1202 program alarm" state
    output = io(12, 2, PUZZLE_INPUTS)
    return output


def part_2():
    """What pair of inputs produces the output `19690720`"""
    desired_output = 19690720
    outputs = []
    possible_inputs = []
    for i in range(100):
        for j in range(100):
            if (j, i) not in possible_inputs:
                possible_inputs.append((i, j))

    for attempt_noun, attempt_verb in possible_inputs:
        output = io(attempt_noun, attempt_verb, PUZZLE_INPUTS)
        if output == desired_output:
            outputs.append((attempt_noun, attempt_verb))   

    return outputs

if __name__ == '__main__':
    output_1202 = part_1()
    print("Part 1 answer: ", output_1202)

    found_outputs = part_2()
    noun, verb = found_outputs[0]
    print(f"Part 2 answer: 100*{noun} + {verb} = {100*noun + verb}")




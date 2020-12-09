from re import findall

from operator import add, sub

from typing import NamedTuple, List, Union, Type


class OperationInput(NamedTuple):
    instruction: 'Instruction'
    accumulator: int
    current_operation_index: int
    total_num_instructions: int


class OperationResult(NamedTuple):
    accumulator: int
    next_operation_index: int


class Op:
    name: str

    impacts_accumulator = False
    impacts_index = False

    def accumulator(self, _input: OperationInput) -> int:
        if self.impacts_accumulator:
            return _input.instruction.direction(_input.accumulator, _input.instruction.value)

        # otherwise do not touch accumulator's value!
        return _input.accumulator

    def next_operation_index(self, _input: OperationInput) -> int:
        if self.impacts_index:
            return _input.instruction.direction(_input.current_operation_index, _input.instruction.value)

        # otherwise go to next instruction
        return _input.current_operation_index + 1

    def apply(self, _input: OperationInput) -> OperationResult:
        return OperationResult(
            accumulator=self.accumulator(_input),
            # % to make sure we do not get index out of range error TODO I this even correct?
            next_operation_index=self.next_operation_index(_input)  # % _input.total_num_instructions,

        )


class ACC(Op):
    name = "acc"
    impacts_accumulator = True


class JMP(Op):
    name = "jmp"
    impacts_index = True


class NOP(Op):
    name = "nop"


operations = {
    "acc": ACC(),
    "jmp": JMP(),
    "nop": NOP(),
}

directions = {
    "+": add,
    "-": sub,
}


class Instruction(NamedTuple):
    operation: Union[ACC, JMP, NOP]
    direction: Union[add, sub]  # "+" or "-"
    value: int

    def __repr__(self):
        return f"{self.operation.name} {self.direction.__name__} {self.value}"


def load_instructions(filename: str) -> List[Instruction]:
    with open(f"day_8/{filename}", "r") as f:
        raw_instructions = findall(r"(([a-z]{3}) (\+|-)(\d+)\n)", f.read()[:-1])
    return [
        Instruction(
            operation=operations[raw_operation],
            direction=directions[direction],
            value=int(value),
        )
        for _, raw_operation, direction, value in raw_instructions
    ]


def run_instructions(instructions: List[Instruction]):
    accumulator = 0
    record_of_run_instructions = {
        (i, instruction): []
        for i, instruction in enumerate(instructions)
    }
    total_num_instructions = len(instructions)
    current_operation_index = 0
    live = True
    count = 1

    while live:
        # first thing in while loop should be getting next instruction
        current_instruction = instructions[current_operation_index]
        instruction_uid = (current_operation_index, current_instruction)
        print(f"{current_instruction} \t\t (acc={accumulator}, index={current_operation_index})")

        if len(record_of_run_instructions[instruction_uid]) > 0:
            # i.e. end process as we have reached infinite loop!
            live = False
            break

        record_of_run_instructions[instruction_uid].append(count)

        operation_output = current_instruction.operation.apply(OperationInput(
            accumulator=accumulator,
            current_operation_index=current_operation_index,
            instruction=current_instruction,
            total_num_instructions=total_num_instructions,
        ))
        accumulator = operation_output.accumulator

        # last thing in while loop should be incrementing index
        current_operation_index = operation_output.next_operation_index
        count += 1

    return record_of_run_instructions, accumulator


if __name__ == "__main__":
    _, final_accumulator = run_instructions(load_instructions("input.txt"))
    print(final_accumulator)

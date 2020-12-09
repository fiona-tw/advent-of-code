from copy import deepcopy
from operator import add, sub
from re import findall
from typing import Dict, List, NamedTuple, Tuple, Union


class OperationInput(NamedTuple):
    instruction: 'Instruction'
    accumulator: int
    operation_index: int
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
            return _input.instruction.direction(_input.operation_index, _input.instruction.value)

        # otherwise go to next instruction
        return _input.operation_index + 1

    def execute(self, _input: OperationInput) -> OperationResult:
        return OperationResult(
            accumulator=self.accumulator(_input),
            next_operation_index=self.next_operation_index(_input)
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

    @classmethod
    def replace_operation(cls, other: 'Instruction', operation: Op):
        return cls(
            operation=operation,
            direction=other.direction,
            value=other.value,
        )


def load_instructions(filename: str) -> List[Instruction]:
    with open(f"day_8/{filename}", "r") as f:
        raw_instructions = findall(r"(([a-z]{3}) (\+|-)(\d+)\n)", f.read())
    return [
        Instruction(
            operation=operations[raw_operation],
            direction=directions[direction],
            value=int(value),
        )
        for _, raw_operation, direction, value in raw_instructions
    ]


class ProgramResult(NamedTuple):
    running_order: Dict[int, Instruction]
    accumulator: int
    has_terminated: bool
    infinite_loop: bool


def get_running_order(record_of_run_instructions: Dict[Tuple[int, Instruction], List[int]]) -> Dict[int, Instruction]:
    return {
        run_count: instruction
        for (index, instruction), run_counts in record_of_run_instructions.items()
        for run_count in run_counts
    }


def run_program_with_instructions(instructions: List[Instruction], debug: bool = False):
    accumulator = 0
    record_of_run_instructions = {
        (i, instruction): []
        for i, instruction in enumerate(instructions)
    }
    total_num_instructions = len(instructions)
    current_operation_index = 0
    current_instruction = instructions[current_operation_index]
    instruction_uid = (current_operation_index, current_instruction)
    has_terminated = False
    infinite_loop = False
    run_count = 0

    while not has_terminated and not infinite_loop:
        # ########################### LOG CURRENT STATE ###########################
        if debug:
            print(f"{current_instruction} \t\t (acc={accumulator}, index={current_operation_index})")
        run_count += 1
        record_of_run_instructions[instruction_uid].append(run_count)

        # ############################ RUN INSTRUCTION ############################
        operation_output = current_instruction.operation.execute(OperationInput(
            accumulator=accumulator,
            operation_index=current_operation_index,
            instruction=current_instruction,
            total_num_instructions=total_num_instructions,
        ))

        # ############################ INCREMENT STATE ############################
        accumulator = operation_output.accumulator

        if operation_output.next_operation_index == total_num_instructions:
            # i.e. program will attempt to run instruction below last instruction --> termination
            has_terminated = True
        elif operation_output.next_operation_index > total_num_instructions:
            raise ValueError("Program attempting to execute unknown instruction past termination")
        else:
            current_operation_index = operation_output.next_operation_index
            current_instruction = instructions[current_operation_index]
            instruction_uid = (current_operation_index, current_instruction)
            if len(record_of_run_instructions[(current_operation_index, current_instruction)]) > 0:
                # we have encountered the same instruction uid --> must break process to avoid an infinite loop!
                infinite_loop = True

    return ProgramResult(
        get_running_order(record_of_run_instructions),
        accumulator,
        has_terminated,
        infinite_loop,
    )


def part_1():
    result = run_program_with_instructions(load_instructions("input.txt"))
    print(f"The broken program's accumulator has value \033[1m__{result.accumulator}__\033[0m when it terminates")


def part_2():
    possible_errs = {
        "jmp": "nop",
        "nop": "jmp",
    }
    broken_instructions = load_instructions("input.txt")

    # idea here is to loop through these and check if program terminates by applying flip to operation type
    record_of_attempted_fixes = {
        (i, instruction): False
        for i, instruction in enumerate(broken_instructions)
        if instruction.operation.name in possible_errs
    }

    for index, instruction_to_swap_out in record_of_attempted_fixes.keys():
        test_instructions = deepcopy(broken_instructions)
        new_operation = operations[possible_errs[instruction_to_swap_out.operation.name]]
        test_instructions[index] = Instruction.replace_operation(instruction_to_swap_out, new_operation)

        result = run_program_with_instructions(test_instructions)
        if result.has_terminated:
            break

    print(f"The program is fixed by swapping instruction at index {index}: {instruction_to_swap_out}")
    print(f"At the end of the fixed program, \033[1maccumulator = {result.accumulator}\033[0m")


if __name__ == "__main__":
    part_1()
    part_2()

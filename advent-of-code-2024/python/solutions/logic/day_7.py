import operator
from itertools import product
from typing import Callable


def concatenate(a: int, b: int) -> int:
    return int(f"{a}{b}")


def get_operators(third_operator: bool) -> list[Callable[[int, int], int]]:
    operators = [operator.add, operator.mul]
    if third_operator:
        operators.append(concatenate)
    return operators


def is_true_equation(equation, third_operator: bool) -> bool:
    # equation = [3267, [81, 40, 27]]
    test_value = equation[0]
    values = equation[1]
    operator_permutations = list(
        product(get_operators(third_operator), repeat=len(values) - 1)
    )
    for operator_permutation in operator_permutations:
        total = values[0]
        for i, value in enumerate(values[1:]):
            total = operator_permutation[i](total, value)
        if total == test_value:
            return True

    return False


def get_calibration_result(puzzle_input: str, third_operator: bool = False) -> int:
    """
    sum of equation totals which can be made true by inserting any combination of + or *
    if third_operator, also uses `||` `concatenate`
    """

    def format_equation(equation):
        # equation = "3267: 81 40 27"
        test_value, values = equation.split(":")
        return [int(test_value), [int(value) for value in values.strip(" ").split(" ")]]

    equations = [format_equation(equation) for equation in puzzle_input.split("\n")]
    return sum(
        equation[0]
        for equation in equations
        if is_true_equation(equation, third_operator)
    )

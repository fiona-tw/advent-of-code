from solutions.logic.day_3 import (
    scan_corrupted_memory,
    scan_corrupted_memory_without_instructions,
)


def test():
    puzzle_input = (
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    assert scan_corrupted_memory_without_instructions(puzzle_input) == 161


def test_using_do_and_dont_instructions():
    puzzle_input = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    assert scan_corrupted_memory(puzzle_input) == 48

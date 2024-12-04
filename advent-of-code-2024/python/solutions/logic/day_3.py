import re


def scan_corrupted_memory_without_instructions(puzzle_input: str) -> int:
    matches = re.findall(
        r"mul\((?P<first_digit>\d{1,3}),(?P<second_digit>\d{1,3})\)", puzzle_input
    )

    total = 0
    for first_digit, second_digit in matches:
        total += int(first_digit) * int(second_digit)

    return total


def scan_corrupted_memory(puzzle_input: str) -> int:
    mul_regex = r"mul\((?P<first_digit>\d{1,3}),(?P<second_digit>\d{1,3})\)"
    do_regex = r"do\(\)"
    dont_regex = r"don't\(\)"
    matches = re.finditer(rf"{mul_regex}|{do_regex}|{dont_regex}", puzzle_input)

    total = 0
    mul_enabled = True
    for re_match in matches:
        match re_match.group():
            case "do()":
                mul_enabled = True
            case "don't()":
                mul_enabled = False
            case _:
                if mul_enabled:
                    first_digit, second_digit = re_match.groups()
                    total += int(first_digit) * int(second_digit)

    return total

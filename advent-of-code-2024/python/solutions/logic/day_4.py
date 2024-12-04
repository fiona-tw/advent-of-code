def get_char(lines, i, j):
    max_i = len(lines[0])
    max_j = len(lines)
    return lines[i][j] if 0 <= i < max_i and 0 <= j < max_j else ""


def print_board(lines, i, j):
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if x == i and y == j:
                print(char, end=" ")
            else:
                print(".", end=" ")
        print()
    print()


def xmas_count(lines, i, j):
    # could probably improve this by using range but keeping things simple
    found = 0
    # Look right
    if get_char(lines, i, j + 1) == "M":
        if get_char(lines, i, j + 2) == "A":
            if get_char(lines, i, j + 3) == "S":
                found += 1
    # Look up
    if get_char(lines, i - 1, j) == "M":
        if get_char(lines, i - 2, j) == "A":
            if get_char(lines, i - 3, j) == "S":
                found += 1
    # Look left
    if get_char(lines, i, j - 1) == "M":
        if get_char(lines, i, j - 2) == "A":
            if get_char(lines, i, j - 3) == "S":
                found += 1
    # Look down
    if get_char(lines, i + 1, j) == "M":
        if get_char(lines, i + 2, j) == "A":
            if get_char(lines, i + 3, j) == "S":
                found += 1
    # Look up left
    if get_char(lines, i - 1, j - 1) == "M":
        if get_char(lines, i - 2, j - 2) == "A":
            if get_char(lines, i - 3, j - 3) == "S":
                found += 1
    # Look up right
    if get_char(lines, i - 1, j + 1) == "M":
        if get_char(lines, i - 2, j + 2) == "A":
            if get_char(lines, i - 3, j + 3) == "S":
                found += 1
    # Look down left
    if get_char(lines, i + 1, j - 1) == "M":
        if get_char(lines, i + 2, j - 2) == "A":
            if get_char(lines, i + 3, j - 3) == "S":
                found += 1
    # Look down right
    if get_char(lines, i + 1, j + 1) == "M":
        if get_char(lines, i + 2, j + 2) == "A":
            if get_char(lines, i + 3, j + 3) == "S":
                found += 1

    return found


def left_diag(lines, i, j, rev=False):
    if get_char(lines, i - 1, j - 1) == ("S" if rev else "M"):
        if get_char(lines, i + 1, j + 1) == ("M" if rev else "S"):
            return True
    return False


def right_diag(lines, i, j, rev=False):
    if get_char(lines, i - 1, j + 1) == ("S" if rev else "M"):
        if get_char(lines, i + 1, j - 1) == ("M" if rev else "S"):
            return True
    return False


def x_mas_count(lines, i, j) -> int:
    if left_diag(lines, i, j) or left_diag(lines, i, j, rev=True):
        if right_diag(lines, i, j) or right_diag(lines, i, j, rev=True):
            return True
    return False


def get_xmas_count(puzzle_input: str) -> int:
    # Part 1
    found = 0
    lines = [[char for char in line] for line in puzzle_input.split("\n")]
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "X":
                found += xmas_count(lines, i, j)

    return found


def get_x_mas_count(puzzle_input: str) -> int:
    # Part 2
    found = 0
    lines = [[char for char in line] for line in puzzle_input.split("\n")]
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "A":
                found += x_mas_count(lines, i, j)

    return found

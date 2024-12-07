from dataclasses import dataclass
from enum import Enum


class GuardHeading(Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def rotate(self) -> "GuardHeading":
        match self.value:
            case "^":
                return GuardHeading.RIGHT
            case "v":
                return GuardHeading.LEFT
            case "<":
                return GuardHeading.UP
            case ">":
                return GuardHeading.DOWN

        raise ValueError(f"Don't know how to rotate {self.value}")


GUARD_HEADINGS = [guard.value for guard in GuardHeading]


@dataclass
class Position:
    """
    x: index of position in the line
    y: index of the line
    0, 0 means top left
    """
    x: int
    y: int


@dataclass
class GuardPosition(Position):
    heading: GuardHeading


class Map:

    def __init__(self, puzzle_input: str) -> None:
        self.raw_input = puzzle_input
        self.visited_positions = set()
        self.lines = [list(line) for line in puzzle_input.split("\n")]

    def print_map(self):
        print()
        for i, line in enumerate(self.lines):
            for j, position in enumerate(line):
                print(position, end="")
            print()

    def get_position_value(self, x, y):
        return self.lines[y][x]

    def set_position_value(self, x: int, y: int, new_char: str):
        self.lines[y][x] = new_char

    def rotate_guard(self):
        guard_position = self.get_guard_position()
        self.set_position_value(
            guard_position.x,
            guard_position.y,
            guard_position.heading.rotate().value,
        )

    def get_guard_position(self) -> GuardPosition:
        for i, line in enumerate(self.lines):
            for j, position in enumerate(line):
                if position in GUARD_HEADINGS:
                    return GuardPosition(
                        x=j,
                        y=i,
                        heading=GuardHeading(position),
                    )

        raise ValueError("Guard not found!")

    def move_up(self, guard_position: GuardPosition) -> None:
        for y in range(guard_position.y - 1, -1, -1):
            if self.get_position_value(guard_position.x, y) in [".", "X"]:
                # Path is clear, mark previous guard position
                # and move guard to new position
                self.set_position_value(guard_position.x, y + 1, "X")
                self.set_position_value(guard_position.x, y, guard_position.heading.value)
            else:
                break

        if self.guard_moves_out_of_map():
            return None

        self.rotate_guard()

    def move_down(self, guard_position: GuardPosition) -> None:
        for y in range(guard_position.y + 1, len(self.lines), 1):
            if self.get_position_value(guard_position.x, y) in [".", "X"]:
                # Path is clear, mark previous guard position
                # and move guard to new position
                self.set_position_value(guard_position.x, y - 1, "X")
                self.set_position_value(guard_position.x, y, guard_position.heading.value)
            else:
                break

        if self.guard_moves_out_of_map():
            return None

        self.rotate_guard()

    def move_right(self, guard_position: GuardPosition) -> None:
        for x in range(guard_position.x + 1, len(self.lines[0]), 1):
            if self.get_position_value(x, guard_position.y) in [".", "X"]:
                # Path is clear, mark previous guard position
                # and move guard to new position
                self.set_position_value(x - 1, guard_position.y, "X")
                self.set_position_value(x, guard_position.y, guard_position.heading.value)
            else:
                break

        if self.guard_moves_out_of_map():
            return None

        self.rotate_guard()

    def move_left(self, guard_position: GuardPosition) -> None:
        for x in range(guard_position.x - 1, -1, -1):
            if self.get_position_value(x, guard_position.y) in [".", "X"]:
                # Path is clear, mark previous guard position
                # and move guard to new position
                self.set_position_value(x + 1, guard_position.y, "X")
                self.set_position_value(x, guard_position.y, guard_position.heading.value)
            else:
                break

        if self.guard_moves_out_of_map():
            return None

        self.rotate_guard()

    def guard_moves_out_of_map(self) -> bool:
        guard_position = self.get_guard_position()
        if guard_position.x == 0:
            return guard_position.heading == GuardHeading.LEFT
        if guard_position.x == len(self.lines[0]) - 1:
            return guard_position.heading == GuardHeading.RIGHT
        if guard_position.y == 0:
            return guard_position.heading == GuardHeading.UP
        if guard_position.y == len(self.lines) - 1:
            return guard_position.heading == GuardHeading.DOWN

        return False

    def move(self):
        guard_position = self.get_guard_position()
        match guard_position.heading:
            case GuardHeading.UP:
                print("move_up: ", guard_position)
                self.move_up(guard_position)
            case GuardHeading.DOWN:
                print("move_down: ", guard_position)
                self.move_down(guard_position)
            case GuardHeading.LEFT:
                print("move_left: ", guard_position)
                self.move_left(guard_position)
            case GuardHeading.RIGHT:
                print("move_right: ", guard_position)
                self.move_right(guard_position)
            case _:
                raise ValueError(f"Don't know how to move guard in heading {guard_position.heading}")

        if self.guard_moves_out_of_map():
            self.print_map()
            return

        self.move()

    def start_patrol(self):
        self.move()

    def count_positions(self):
        total = 0
        for line in self.lines:
            for position in line:
                if position == "X":
                    total += 1
        return total + 1


def count_guard_positions(puzzle_input: str) -> int:
    mapped_area = Map(puzzle_input)
    mapped_area.start_patrol()
    return mapped_area.count_positions()

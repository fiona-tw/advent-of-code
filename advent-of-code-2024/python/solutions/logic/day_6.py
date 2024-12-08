from copy import deepcopy
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
class GuardPosition:
    """
    x: index of position in the line
    y: index of the line
    0, 0 means top left
    """

    x: int
    y: int
    heading: GuardHeading


class LoopDetected(Exception):
    pass


class Map:
    def __init__(self, puzzle_input: str) -> None:
        self.raw_input = puzzle_input
        self.lines = [list(line) for line in self.raw_input.split("\n")]
        self.guard_rotations = []
        self.original_path = []  # to be used for part 2

    def reset(self):
        self.lines = [list(line) for line in self.raw_input.split("\n")]
        self.guard_rotations = []

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

    def pattern_repeated(self, guard_position) -> bool:
        """
        self.guard_rotations = [(4, 1, '>'), (8, 1, 'v'), (8, 6, '<'), (4, 6, '^'), (4, 1, '>'), (8, 1, 'v'), (8, 6, '<'), (4, 6, '^')]
        """
        if guard_position not in self.guard_rotations:
            return False

        pattern = self.guard_rotations[-4:]
        previous_rotations = self.guard_rotations[:-4]
        for i in range(len(previous_rotations)):
            if previous_rotations[i : i + 4] == pattern:
                return True

    def rotate_guard(self):
        guard_position = self.get_guard_position()
        new_heading = guard_position.heading.rotate()
        self.set_position_value(
            guard_position.x,
            guard_position.y,
            new_heading.value,
        )
        new_position = GuardPosition(
            x=guard_position.x,
            y=guard_position.y,
            heading=new_heading,
        )
        if self.pattern_repeated(new_position):
            raise LoopDetected

        self.guard_rotations.append(new_position)

    def get_guard_position(self) -> GuardPosition:
        # solution could be more efficient if we kept track of the guard rather than calling this method each time...
        for i, line in enumerate(self.lines):
            for j, position in enumerate(line):
                if position in GUARD_HEADINGS:
                    return GuardPosition(
                        x=j,
                        y=i,
                        heading=GuardHeading(position),
                    )

        raise ValueError("Guard not found!")

    def guard_moves_out_of_map(self) -> bool:
        moves_out_of_map = False
        guard_position = self.get_guard_position()
        if guard_position.x == 0:
            moves_out_of_map = guard_position.heading == GuardHeading.LEFT
        if guard_position.x == len(self.lines[0]) - 1:
            moves_out_of_map = guard_position.heading == GuardHeading.RIGHT
        if guard_position.y == 0:
            moves_out_of_map = guard_position.heading == GuardHeading.UP
        if guard_position.y == len(self.lines) - 1:
            moves_out_of_map = guard_position.heading == GuardHeading.DOWN

        if moves_out_of_map:
            self.set_position_value(guard_position.x, guard_position.y, "X")
            return True

        return False

    def move_up(self, guard_position: GuardPosition) -> None:
        for y in range(guard_position.y - 1, -1, -1):
            if self.get_position_value(guard_position.x, y) not in [".", "X"]:
                # Path is obstructed, stop moving
                break
            # Path is clear, mark previous guard position and move guard to new position
            self.set_position_value(guard_position.x, y + 1, "X")
            self.set_position_value(guard_position.x, y, guard_position.heading.value)

    def move_down(self, guard_position: GuardPosition) -> None:
        for y in range(guard_position.y + 1, len(self.lines), 1):
            if self.get_position_value(guard_position.x, y) not in [".", "X"]:
                # Path is obstructed, stop moving
                break
            # Path is clear, mark previous guard position and move guard to new position
            self.set_position_value(guard_position.x, y - 1, "X")
            self.set_position_value(guard_position.x, y, guard_position.heading.value)

    def move_right(self, guard_position: GuardPosition) -> None:
        for x in range(guard_position.x + 1, len(self.lines[0]), 1):
            if self.get_position_value(x, guard_position.y) not in [".", "X"]:
                # Path is obstructed, stop moving
                break
            # Path is clear, mark previous guard position and move guard to new position
            self.set_position_value(x - 1, guard_position.y, "X")
            self.set_position_value(x, guard_position.y, guard_position.heading.value)

    def move_left(self, guard_position: GuardPosition) -> None:
        for x in range(guard_position.x - 1, -1, -1):
            if self.get_position_value(x, guard_position.y) not in [".", "X"]:
                # Path is obstructed, stop moving
                break
            # Path is clear, mark previous guard position and move guard to new position
            self.set_position_value(x + 1, guard_position.y, "X")
            self.set_position_value(x, guard_position.y, guard_position.heading.value)

    def move(self):
        guard_position = self.get_guard_position()
        match guard_position.heading:
            case GuardHeading.UP:
                self.move_up(guard_position)
            case GuardHeading.DOWN:
                self.move_down(guard_position)
            case GuardHeading.LEFT:
                self.move_left(guard_position)
            case GuardHeading.RIGHT:
                self.move_right(guard_position)
            case _:
                raise ValueError(
                    f"Don't know how to move guard in heading {guard_position.heading}"
                )

        if self.guard_moves_out_of_map():
            return

        self.rotate_guard()
        self.move()

    def start_patrol(self):
        self.move()

    def count_positions(self):
        total = 0
        for line in self.lines:
            for position in line:
                if position == "X":
                    total += 1
        return total

    def guard_visited_adjacent_position(self, x: int, y: int) -> bool:
        return self.original_path[y][x] == "X"

    def obstruction_leads_to_loop(self, x: int, y: int) -> bool:
        if not self.guard_visited_adjacent_position(x, y):
            # No point in checking if the guard didn't visit this position in original route
            return False

        self.set_position_value(x, y, "O")
        try:
            self.start_patrol()
        except LoopDetected:
            return True

        return False


def count_guard_positions(puzzle_input: str) -> int:
    mapped_area = Map(puzzle_input)
    mapped_area.start_patrol()
    return mapped_area.count_positions()


def count_number_of_places_for_obstruction(puzzle_input: str) -> int:
    total = 0
    mapped_area = Map(puzzle_input)
    mapped_area.move()
    mapped_area.original_path = deepcopy(mapped_area.lines)

    for i, line in enumerate(mapped_area.lines):
        for j, position in enumerate(line):
            if mapped_area.get_position_value(j, i) == ".":
                if mapped_area.obstruction_leads_to_loop(x=j, y=i):
                    total += 1
            mapped_area.reset()

    return total

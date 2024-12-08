from solutions.logic.day_6 import (
    count_guard_positions,
    count_number_of_places_for_obstruction,
)


def test():
    puzzle_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    end = """
    ....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X.."""
    assert count_guard_positions(puzzle_input) == 41


def test_part_2():
    puzzle_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    end = """
    ....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X.."""
    assert count_number_of_places_for_obstruction(puzzle_input) == 6

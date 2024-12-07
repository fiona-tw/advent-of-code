from solutions.logic.day_6 import count_guard_positions

def test():
    puzzle_input =  """....#.....
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
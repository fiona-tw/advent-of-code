from solutions.logic.day_4 import get_xmas_count, get_x_mas_count


def test():
    puzzle_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    assert get_xmas_count(puzzle_input) == 18


def test_part_2():
    puzzle_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    assert get_x_mas_count(puzzle_input) == 9

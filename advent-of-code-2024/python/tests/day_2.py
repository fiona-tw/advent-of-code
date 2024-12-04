from solutions.logic.day_2 import get_count_of_safe_reports


def test():
    puzzle_input = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    assert get_count_of_safe_reports(puzzle_input) == 4

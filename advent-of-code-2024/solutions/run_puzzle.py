import sys

from logic.day_1 import get_similarity_score
from logic.day_2 import get_count_of_safe_reports


def _get_input_for_day(day: int) -> str:
    with open(f"puzzle_inputs/day_{day}.txt") as file:
        return file.read()


def run_day_1():
    """
    Answers:
        Part 1: 1938424
        Part 2: 22014209
    """
    # return get_distance_sum(_get_input_for_day(1))
    return get_similarity_score(_get_input_for_day(1))

def run_day_2():
    """
    Answers:
        Part 1: 246
        Part 2: 318
    """
    return get_count_of_safe_reports(_get_input_for_day(2))


def run_for_day_x(day: int):
    try:
        return globals()[f"run_day_{day}"]()
    except KeyError:
        print(
            f"No solution implemented for day {day}.\t(`run_day_{day}` does not exist!)"
        )


if __name__ == "__main__":
    day = sys.argv[1]  # i.e. 1 or 2 etc.
    try:
        day = int(day)
    except ValueError:
        print(
            f"Please supply the day as a number for the puzzle you want to run\n\t('{day}' is not an integer!)"
        )
    else:
        print(f"\nDay {day} solution:\n")
        print(run_for_day_x(day))

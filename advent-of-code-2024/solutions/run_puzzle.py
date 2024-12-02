import sys

from logic_day_1 import sum_of_calibration_values
from logic_day_2 import (
    sum_of_game_ids_that_are_possible_with_config,
    sum_of_power_of_minimum_set_of_cubes_by_brute_force,
)


def _get_input_for_day(day: int) -> str:
    with open(f"puzzle_inputs/day_{day}.txt") as file:
        return file.read()


def run_day_1():
    ...


def run_for_day_x(day: int):
    try:
        globals()[f"run_day_{day}"]()
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
        run_for_day_x(day)

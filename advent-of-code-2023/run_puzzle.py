import sys

from logic_day_1 import sum_of_calibration_values
from logic_day_2 import sum_of_game_ids_that_are_possible_with_config, sum_of_power_of_minimum_set_of_cubes_by_brute_force


def run_day_1():
    with open(sys.argv[1]) as file:
        raw_calibration_document = file.read()

    print(sum_of_calibration_values(raw_calibration_document))


def run_day_2():
    with open(sys.argv[1]) as file:
        raw_games = file.read()

    print("Part 1: ", sum_of_game_ids_that_are_possible_with_config(raw_games))
    print("Part 2: ", sum_of_power_of_minimum_set_of_cubes_by_brute_force(raw_games))


if __name__ == "__main__":
    run_day_2()

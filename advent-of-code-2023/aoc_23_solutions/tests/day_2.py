from unittest import TestCase

from aoc_23_solutions.logic.day_2 import (
    Game,
    parse_puzzle_input,
    sum_of_game_ids_that_are_possible_with_config,
    sum_of_power_of_minimum_set_of_cubes_by_brute_force,
)


class DayTwoTests(TestCase):
    TEST_INPUT = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    # 12 red cubes, 13 green cubes, and 14 blue cubes?
    def test_parsing_input(self):
        expected_games = [
            Game("1", "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"),
            Game("2", "1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"),
            Game("3", "8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"),
            Game("4", "1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"),
            Game("5", "6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"),
        ]

        games = parse_puzzle_input(self.TEST_INPUT)
        self.assertEqual(
            games,
            expected_games
        )

    def test_puzzle_1(self):
        self.assertEqual(
            sum_of_game_ids_that_are_possible_with_config(self.TEST_INPUT),
            8
        )

    def test_puzzle_2(self):
        self.assertEqual(
            sum_of_power_of_minimum_set_of_cubes_by_brute_force(self.TEST_INPUT),
            2286
        )

    def test_day_1_puzzle_1(self):
        with open("puzzle_inputs/day_2.txt") as input_file:
            raw_doc = input_file.read()

        self.assertEqual(
            sum_of_game_ids_that_are_possible_with_config(raw_doc),
            2085,
        )

    def test_day_2_puzzle_2(self):
        with open("puzzle_inputs/day_2.txt") as input_file:
            raw_doc = input_file.read()

        self.assertEqual(
            sum_of_power_of_minimum_set_of_cubes_by_brute_force(raw_doc),
            79315,
        )

from unittest import TestCase

from logic_day_1 import CalibrationDocument, CalibrationValue, sum_of_calibration_values
from logic_day_2 import parse_puzzle_input, Game, sum_of_game_ids_that_are_possible_with_config, \
    sum_of_power_of_minimum_set_of_cubes_by_brute_force


class DayOneTests(TestCase):
    TEST_INPUT = """1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet"""

    def test_parsing_document(self):
        document = CalibrationDocument(self.TEST_INPUT)

        # our lines are 12, 38, 15, and 77. Adding these together produces 142.
        self.assertEqual(
            document.lines,
            [
                CalibrationValue("1abc2"),
                CalibrationValue("pqr3stu8vwx"),
                CalibrationValue("a1b2c3d4e5f"),
                CalibrationValue("treb7uchet"),
            ]
        )

    def test_calibration_values(self):
        self.assertEqual(
            [
                CalibrationValue("1abc2").value,
                CalibrationValue("pqr3stu8vwx").value,
                CalibrationValue("a1b2c3d4e5f").value,
                CalibrationValue("treb7uchet").value,
                CalibrationValue("87mmlvfr4").value,
            ],
            [
                12,
                38,
                15,
                77,
                84,
            ]
        )

    def test_calibration_values_containing_spelt_number(self):
        self.assertEqual(
            [
                CalibrationValue("two1nine").value,
                CalibrationValue("eightwothree").value,
                CalibrationValue("abcone2threexyz").value,
                CalibrationValue("xtwone3four").value,
                CalibrationValue("4nineeightseven2").value,
                CalibrationValue("zoneight234").value,
                CalibrationValue("7pqrstsixteen").value,
            ],
            [
                29,
                83,
                13,
                24,
                42,
                14,
                76,
            ]
        )

    def test_sum_of_calibration_values(self):
        self.assertEqual(
            sum_of_calibration_values(self.TEST_INPUT),
            142,
        )

    def test_day_1_puzzle_1(self):
        with open("puzzle_inputs/day_1.txt") as input_file:
            raw_doc = input_file.read()

        self.assertEqual(
            sum_of_calibration_values(raw_doc),
            54_875,  # day 1 - puzzle 2
            55_538,  # day 1 - puzzle 1
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

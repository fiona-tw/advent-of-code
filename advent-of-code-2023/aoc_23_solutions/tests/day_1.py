from unittest import TestCase

from aoc_23_solutions.logic.day_1 import CalibrationDocument, CalibrationValue, sum_of_calibration_values


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

    def test_day_1_puzzle(self):
        with open("puzzle_inputs/day_1.txt") as input_file:
            raw_doc = input_file.read()

        self.assertEqual(
            sum_of_calibration_values(raw_doc),
            54_875,  # day 1 - puzzle 2
            55_538,  # day 1 - puzzle 1
        )

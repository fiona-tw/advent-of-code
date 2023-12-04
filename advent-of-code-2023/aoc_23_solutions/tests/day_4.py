from unittest import TestCase

from aoc_23_solutions.logic.day_4 import OldScratchcard, get_value_of_old_scratchcards, Scratchcard, \
    get_final_count_of_scratchcards


class DayFourTests(TestCase):
    TEST_INPUT = """
    Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14 1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58 5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """

    def test_scratchcard_cls_initialisation(self):
        card = OldScratchcard("Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53")
        self.assertEqual(
            card.winning_numbers,
            [41, 48, 83, 86, 17]
        )
        self.assertEqual(
            card.my_numbers,
            [83, 86, 6, 31, 17, 9, 48, 53]
        )

    def test_other_values(self):
        self.assertEqual(
            OldScratchcard("Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53").value,
            8,
        )
        self.assertEqual(
            OldScratchcard("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19").value,
            2,
        )
        self.assertEqual(
            OldScratchcard("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14 1").value,
            2,
        )
        self.assertEqual(
            OldScratchcard("Card 4: 41 92 73 84 69 | 59 84 76 51 58 5 54 83").value,
            1,
        )
        self.assertEqual(
            OldScratchcard("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36").value,
            0,
        )
        self.assertEqual(
            OldScratchcard("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11").value,
            0,
        )

    def test_puzzle_1(self):
        self.assertEqual(
            get_value_of_old_scratchcards(self.TEST_INPUT),
            13
        )

    def test_day_1_puzzle_1(self):
        with open("puzzle_inputs/day_4.txt") as input_file:
            raw_scratchcards = input_file.read()

        self.assertEqual(
            get_value_of_old_scratchcards(raw_scratchcards),
            22488,
        )

    def test_card_number(self):
        card = Scratchcard("Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53")
        self.assertEqual(
            card.card_number,
            1
        )

    def test_puzzle_2(self):
        """
        Once all the originals and copies have been processed, you end up with:
        - 1 instance of card 1
        - 2 instances of card 2
        - 4 instances of card 3
        - 8 instances of card 4
        - 14 instances of card 5
        - 1 instance of card 6
        In total, this example pile of scratchcards causes you to ultimately have 30 scratchcards!
        """
        self.assertEqual(
            get_final_count_of_scratchcards(self.TEST_INPUT),
            30
        )

    def test_day_1_puzzle_2(self):
        with open("puzzle_inputs/day_4.txt") as input_file:
            raw_scratchcards = input_file.read()

        self.assertEqual(
            get_final_count_of_scratchcards(raw_scratchcards),
            7013204,
        )

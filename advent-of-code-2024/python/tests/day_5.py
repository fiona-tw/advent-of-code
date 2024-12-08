from solutions.logic.day_5 import (
    get_relevant_rules,
    get_sum_of_middle_pages_from_correctly_ordered_updates,
    get_sum_of_middle_pages_from_correctly_ordered_incorrect_updates,
)


def test_get_relevant_rules():
    rules = [
        ["47", "53"],
        ["97", "13"],
        ["97", "61"],
        ["97", "47"],
        ["75", "29"],
        ["61", "13"],
        ["75", "53"],
        ["29", "13"],
        ["97", "29"],
        ["53", "29"],
        ["61", "53"],
        ["97", "53"],
        ["61", "29"],
        ["47", "13"],
        ["75", "47"],
        ["97", "75"],
        ["47", "61"],
        ["75", "61"],
        ["47", "29"],
        ["75", "13"],
        ["53", "13"],
    ]
    first_update = ["75", "47", "61", "53", "29"]
    assert get_relevant_rules(rules, first_update) == [
        ["47", "53"],
        ["75", "29"],
        ["75", "53"],
        ["53", "29"],
        ["61", "53"],
        ["61", "29"],
        ["75", "47"],
        ["47", "61"],
        ["75", "61"],
        ["47", "29"],
    ]


def test():
    puzzle_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    assert get_sum_of_middle_pages_from_correctly_ordered_updates(puzzle_input) == 143


def test_part_2_example():
    puzzle_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    assert (
        get_sum_of_middle_pages_from_correctly_ordered_incorrect_updates(puzzle_input)
        == 123
    )


def test_part_2_real_input():
    with open("solutions/puzzle_inputs/day_5.txt") as f:
        puzzle_input = f.read()
    assert (
        get_sum_of_middle_pages_from_correctly_ordered_incorrect_updates(puzzle_input)
        == 5353
    )

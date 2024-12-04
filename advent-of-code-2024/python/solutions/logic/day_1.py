def get_lists(puzzle_input):
    first_list = []
    second_list = []
    for row in puzzle_input.split("\n"):
        str_value_1, str_value_2 = row.split("   ")
        first_list.append(int(str_value_1))
        second_list.append(int(str_value_2))
    return first_list, second_list


def get_distance_sum(puzzle_input: str):
    first_list, second_list = get_lists(puzzle_input)

    total = 0
    for value_in_first_list, value_in_second_list in zip(
        sorted(first_list), sorted(second_list)
    ):
        total += abs(value_in_first_list - value_in_second_list)

    return total


def get_similarity_score(puzzle_input: str):
    similarity_score = 0
    first_list, second_list = get_lists(puzzle_input)
    from collections import Counter

    second_list_counter = dict(Counter(second_list).most_common())
    for value in first_list:
        similarity_score += value * second_list_counter.get(value, 0)
    return similarity_score

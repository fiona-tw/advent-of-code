def get_distance_sum(puzzle_input: str):
    first_list = []
    second_list = []
    for row in puzzle_input.split("\n")[:-1]:
        str_value_1, str_value_2 = row.split("   ")
        first_list.append(int(str_value_1))
        second_list.append(int(str_value_2))
        print(str_value_1, str_value_2)

    total = 0
    for value_in_first_list, value_in_second_list in zip(sorted(first_list), sorted(second_list)):
        total += abs(value_in_first_list - value_in_second_list)

    return total

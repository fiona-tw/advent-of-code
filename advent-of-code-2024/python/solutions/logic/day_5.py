def get_relevant_rules(rules: list[list[str]], update: list[str]):
    relevant_rules = []
    for rule in rules:
        if set(rule) - set(update):
            continue

        relevant_rules.append(rule)

    return relevant_rules


def get_valid_updates(rules: list[list[str]], updates: list[list[str]]):
    """
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

    ['75', '47', '61', '53', '29'],
    """
    valid_updates = []
    for update in updates:
        is_valid = True
        for rule in get_relevant_rules(rules, update):
            index_first_page = update.index(rule[0])
            index_second_page = update.index(rule[1])
            if index_first_page > index_second_page:
                # this update breaks the rule so is not valid, no point checking remaining rules
                is_valid = False
                break
        if is_valid:
            valid_updates.append(update)

    return valid_updates


def get_sum_of_middle_pages_from_correctly_ordered_updates(puzzle_input):
    rules_str, updates_str = puzzle_input.split("\n\n")

    rules = [rule.split("|") for rule in rules_str.split("\n")]
    updates = [update.split(",") for update in updates_str.split("\n")]

    page_sum = 0
    for valid_update in get_valid_updates(rules, updates):
        print(valid_update)
        page_sum += int(valid_update[int((len(valid_update) - 1 )/ 2)])

    return page_sum

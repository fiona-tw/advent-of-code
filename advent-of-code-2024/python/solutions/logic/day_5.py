from collections import defaultdict


def get_relevant_rules(rules: list[list[str]], update: list[str]):
    relevant_rules = []
    for rule in rules:
        if set(rule) - set(update):
            continue

        relevant_rules.append(rule)

    return relevant_rules


def get_valid_updates(rules: list[list[str]], updates: list[list[str]]):
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
    """Part 1"""
    rules_str, updates_str = puzzle_input.split("\n\n")

    rules = [rule.split("|") for rule in rules_str.split("\n")]
    updates = [update.split(",") for update in updates_str.split("\n")]

    page_sum = 0
    for valid_update in get_valid_updates(rules, updates):
        page_sum += int(valid_update[int((len(valid_update) - 1) / 2)])

    return page_sum


def swap_values(update, page, index_to_swap_with):
    """moves the value of `page` to the index given and replace the value at its current index with the value there."""
    page_index = update.index(page)
    swap_with = update[index_to_swap_with]
    update[index_to_swap_with] = page
    update[page_index] = swap_with


def get_earliest_page(update, page, pages_must_come_after) -> str | None:
    if pages_to_follow := pages_must_come_after.get(page):
        if common_pages := set.intersection(set(update), set(pages_to_follow)):
            closest_page_to_follow_index = min(update.index(page_to_follow) for page_to_follow in common_pages)
            if closest_page_to_follow_index < update.index(page):
                # only swap if needed, if page comes after the closest page to follow
                return closest_page_to_follow_index
    return None


def sort_recursive(update, page, pages_must_come_after, i: int = 0):
    if page not in update:
        return update

    index_to_swap_with = get_earliest_page(update, page, pages_must_come_after)
    if index_to_swap_with is not None:
        value_swapped = update[index_to_swap_with]
        swap_values(update, page, index_to_swap_with)

        if next_page := get_earliest_page(update, value_swapped, pages_must_come_after):
            sort_recursive(update, next_page, pages_must_come_after, i + 1)

    return update


def get_corrected_update(update: list[str], rules: list[list[str]], i: int = 0) -> list[
    str]:
    pages_must_come_after = defaultdict(set)
    pages_must_come_before = defaultdict(set)
    for rule in rules:
        pages_must_come_after[rule[0]].add(rule[1])
        pages_must_come_before[rule[1]].add(rule[0])

    print()
    while violations := get_violations(rules, update):
        print(f"{len(violations)}", end=".")
        for page, pages_to_follow in pages_must_come_after.items():
            sort_recursive(update, page, pages_must_come_after)

    return update


def get_violations(rules: list[list[str]], update: list[str]):
    violations = []
    for rule in get_relevant_rules(rules, update):
        index_first_page = update.index(rule[0])
        index_second_page = update.index(rule[1])
        if index_first_page > index_second_page:
            violations.append(rule)

    return violations


def get_corrected_invalid_updates(rules: list[list[str]], updates: list[list[str]]) -> list[list[str]]:
    corrected_invalid_updates = []
    for update in updates:
        if get_violations(rules, update):
            corrected_invalid_updates.append(
                get_corrected_update(update, rules)
            )

    return corrected_invalid_updates


def get_sum_of_middle_pages_from_correctly_ordered_incorrect_updates(puzzle_input):
    """Part 2"""
    rules_str, updates_str = puzzle_input.split("\n\n")

    rules = [rule.split("|") for rule in rules_str.split("\n")]
    updates = [update.split(",") for update in updates_str.split("\n")]

    page_sum = 0
    for valid_update in get_corrected_invalid_updates(rules, updates):
        page_sum += int(valid_update[int((len(valid_update) - 1) / 2)])

    return page_sum

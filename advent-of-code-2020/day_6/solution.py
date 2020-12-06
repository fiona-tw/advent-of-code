from collections import Callable
from string import ascii_lowercase

QUESTIONS = set(ascii_lowercase)


def process_response(raw_response: str, set_operator: Callable[[set, set], set]) -> int:
    individual_responses = raw_response.split("\n")

    common_response = set(individual_responses[0])
    for response in individual_responses[1:]:
        common_response = set_operator(set(response), set(common_response))
    return len(common_response)


def process_group_responses(set_operator):
    with open("input.txt", "r") as f:
        responses = f.read()[:-1].split("\n\n")

    return sum(
        process_response(group_response, set_operator)
        for group_response in responses
    )


# Part 1
print(process_group_responses(set.union))  # 6714

# Part 2
print(process_group_responses(set.intersection))  # 3435

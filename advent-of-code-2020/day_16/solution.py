import re

from numpy import prod
from typing import List, Dict, Tuple

example = [
    (7, 1, 14),
    (7, 3, 47),
    (40, 4, 50),
    (55, 2, 20),
    (38, 6, 12),
]


class Scanner:

    def __init__(self, filename: str) -> None:
        with open(f"day_16/{filename}", "r") as f:
            tickets_pattern = r"((?:\d+|,|\n)+)"

            rules, my_ticket, nearby_tickets = re.match(
                rf"((?:(?:\w|\s)+: \d+-\d+ or \d+-\d+\n)+)\n"
                rf"your ticket:\n{tickets_pattern}\n"
                rf"nearby tickets:{tickets_pattern}\n",
                f.read()
            ).groups()

            raw_rules = re.findall(r"((?:\w|\s)+): (\d+)-(\d+) or (\d+)-(\d+)", rules)

            rules = {}
            for raw_rule in raw_rules:
                rule_name, r1, r2, r3, r4 = raw_rule
                rules[rule_name] = list(
                    range(int(r1), int(r2) + 1)
                ) + list(
                    range(int(r3), int(r4) + 1)
                )
            self.rule_mapping = rules
            # self.rule_mapping = {
            #   "class": [1, 2, 3, 5, 6, 7],
            #   "row": [6, 7, .. , 10, 11, 33, 34, ..., 43, 44],
            #   "seat": [13, 14, ..., 39, 40, 45, 46, ..., 49, 50],
            # }

            self.my_ticket = [int(x) for x in re.findall(r"(\d+)(?:,|)", my_ticket)]

            self.nearby_tickets = [
                [int(y) for y in x.split(",")]
                for x in nearby_tickets[1:].split("\n")
            ]

    def invalid_values(self, ticket: List[int]) -> List[int]:
        invalid_values = ticket
        for rule_name, acceptable_values in self.rule_mapping.items():
            invalid_values = list(set(invalid_values) - set(acceptable_values))
        return invalid_values

    def is_valid(self, ticket: List[int]) -> bool:
        return not self.invalid_values(ticket)

    def get_ticket_scanning_error_rate(self) -> int:
        invalid_values = sum([
            self.invalid_values(ticket) for ticket in self.nearby_tickets
        ], [])
        return sum(invalid_values)

    def get_valid_tickets(self) -> List[List[int]]:
        return [ticket for ticket in self.nearby_tickets if self.is_valid(ticket)]

    def get_rules_matching_column(self, column: Tuple[int]) -> List[str]:
        return [
            rule_name for rule_name, valid_values in self.rule_mapping.items()
            if not set(column) - set(valid_values)
        ]

    def get_column_to_matching_rules(self) -> Dict[int, List[str]]:
        zipped_tickets = list(zip(*self.get_valid_tickets()))
        # zipped_tickets = [
        #     (3, 15, 5),
        #     (9, 1, 14),
        #     (18, 5, 9),
        # ]
        column_to_valid_rules = {}
        for i, column_i_values in enumerate(zipped_tickets):
            column_to_valid_rules[i] = self.get_rules_matching_column(column_i_values)
        return column_to_valid_rules

    def determine_columns(self) -> Dict[int, str]:
        column_to_possible_rules = self.get_column_to_matching_rules()
        # column_to_matching_rules = {
        #     0: ['row'],
        #     1: ['class', 'row'],
        #     2: ['class', 'row', 'seat']
        # }

        sorted_choices = sorted(
            column_to_possible_rules.items(),
            key=lambda x: len(x[1])
        )
        column_to_rule = {}
        for col_num, possible_rules in sorted_choices:
            valid_rules = set(possible_rules) - set(column_to_rule.values())
            assert len(valid_rules) == 1
            column_to_rule[col_num] = valid_rules.pop()
        return column_to_rule

    def get_departure_values(self) -> List[int]:
        cols = [
            i for i, rule_name in self.determine_columns().items()
            if "departure" in rule_name
        ]
        return [self.my_ticket[i] for i in cols]


def part_1(filename: str) -> None:
    scanner = Scanner(filename)
    print(scanner.get_ticket_scanning_error_rate())


def part_2(filename: str) -> None:
    scanner = Scanner(filename)
    departure_values = scanner.get_departure_values()
    print(prod(departure_values))


if __name__ == "__main__":
    part_1("input.txt")
    part_2("input.txt")

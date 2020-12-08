import re
from typing import Dict, List, Tuple, NamedTuple

BagColourType = str


class Contents(NamedTuple):
    colour: BagColourType
    count: int


class Bag:
    colour: BagColourType
    contents: List[Contents]

    def __init__(self, colour: BagColourType, contents: List[Tuple[BagColourType, int]]):
        self.colour = colour
        self.contents = [Contents(bag_colour, bag_count) for bag_colour, bag_count in contents]

    def __str__(self):
        return f"Bag({self.colour})"

    def __repr__(self):
        contents = [(content.colour, content.count) for content in self.contents]
        return f'Bag("{self.colour}", {contents})'


def load_and_process_bags(filename: str) -> Dict[BagColourType, Contents]:
    with open(filename, "r") as f:
        raw_bags = f.read()[:-1].split("\n")

    pattern = "(.*) bags contain (.*)"
    bag_colour_to_raw_contents = {
        re.match(pattern, raw_bag).group(1): re.match(pattern, raw_bag).group(2)
        for raw_bag in raw_bags
    }

    processed_bags = []

    all_colours = "|".join(bag_colour_to_raw_contents.keys())
    bags_content_pattern = rf"(?: |)(\d+) ({all_colours}) (?:bags|bag)(?:.|,)"

    for colour, raw_contents in bag_colour_to_raw_contents.items():
        contents = []
        if not bag_is_empty(raw_contents):
            contents = get_bag_contents(raw_contents, bags_content_pattern)
        processed_bags.append(Bag(colour=colour, contents=contents))

    return {
        processed_bag.colour: processed_bag.contents
        for processed_bag in processed_bags
    }


def bag_is_empty(raw_bag_str: str) -> bool:
    return bool(re.findall("no other bags.", raw_bag_str))


def get_bag_contents(raw_contents: str, bags_content_pattern: str) -> List[Tuple[BagColourType, int]]:
    return [
        (bag_colour, int(bag_count))
        for bag_count, bag_colour in re.findall(bags_content_pattern, raw_contents)
    ]


def search_individual_bag_getter(bag_colour_to_contents: Dict[BagColourType, Contents], process_count: bool = False):
    def search_bag(
            bag_colour: BagColourType,
            containing_factor: int = 1,
    ) -> Tuple[BagColourType, ...]:
        _bags = []
        for bag_contents in bag_colour_to_contents[bag_colour]:
            this_bag_colour = bag_contents.colour
            this_bag_count = bag_contents.count

            new_factor = containing_factor
            if process_count:
                new_factor = this_bag_count * containing_factor
                # print(new_factor, end=" ", flush=True)

            _bags.extend([this_bag_colour] * new_factor)
            _bags.extend(search_bag(this_bag_colour, new_factor))
        return tuple(_bags)

    return search_bag


def search_bags(filename: str) -> Dict[BagColourType, Tuple[BagColourType]]:
    """Returns a mapping of bag colour to a tuple of it's expanded contents"""
    bag_colour_to_contents = load_and_process_bags(filename)
    _search = search_individual_bag_getter(bag_colour_to_contents)
    return {bag: _search(bag) for bag in bag_colour_to_contents.keys()}


def search_for_bag_and_count(filename: str, bag_colour: BagColourType) -> Tuple[BagColourType, ...]:
    """Returns a mapping of bag colour to a tuple of it's expanded contents"""
    bag_colour_to_contents = load_and_process_bags(filename)
    assert bag_colour in bag_colour_to_contents
    _search = search_individual_bag_getter(bag_colour_to_contents, process_count=True)
    return _search(bag_colour)


GOLD = "shiny gold"

EXAMPLE_1_FLATTENED_BAGS = search_bags("example_input.txt")
REAL_FLATTENED_BAGS = search_bags("input.txt")
EXAMPLE_2_GOLD_BAG_COUNT = search_for_bag_and_count("example_2_input.txt", bag_colour=GOLD)
REAL_GOLD_BAG_COUNT = search_for_bag_and_count("input.txt", bag_colour=GOLD)


def count_bags_that_contain(search_for_colour: str, flatted_bags: Dict[BagColourType, Tuple[BagColourType]]) -> int:
    bags_that_contain_colour = []
    for bag_colour, flattened_contents in flatted_bags.items():
        if search_for_colour in flattened_contents:
            bags_that_contain_colour.append(bag_colour)
    return len(bags_that_contain_colour)


print(
    f"[PART 1 EXAMPLE INPUT]:\t\t\033[1m{count_bags_that_contain(GOLD, EXAMPLE_1_FLATTENED_BAGS)}\033[0m "
    f"bags contain at least one {GOLD} bag"
)

print(
    f"[PART 1 INPUT]:\t\t\t\033[1m{count_bags_that_contain(GOLD, REAL_FLATTENED_BAGS)}\033[0m bags "
    f"contain at least one {GOLD} bag"
)

print(
    f"[PART 2 EXAMPLE 2 INPUT]:\t{GOLD} bag contains "
    f"\033[1m{len(EXAMPLE_2_GOLD_BAG_COUNT)}\033[0m bags"
)
print(
    f"[PART 2 INPUT]:\t{GOLD} bag contains "
    f"\033[1m{len(REAL_GOLD_BAG_COUNT)}\033[0m bags"
)

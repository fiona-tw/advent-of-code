import re
from dataclasses import dataclass
from math import prod

RED = "red"
BLUE = "blue"
GREEN = "green"


@dataclass(init=False)
class CubeCount:
    colour: str
    count: int

    def __init__(self, raw_colour: str, raw_count: str):
        self.colour = raw_colour
        self.count = int(raw_count)

    def __gt__(self, other):
        if self.colour != other.colour:
            raise ValueError(f"Cannot compare cube counts of different colours: {self.colour} != {other.colour}!")
        return self.count > other.colour


class CubeSet:
    cube_counts: tuple[CubeCount, ...]

    def __init__(self, raw_cubes: str) -> None:
        self._raw_str = raw_cubes
        cube_set_pattern = r"(\d+) (red|green|blue)"
        self.cube_counts = tuple(
            CubeCount(cube_colour, cube_count) for cube_count, cube_colour in re.findall(cube_set_pattern, raw_cubes)
        )

    def __eq__(self, other: "CubeSet") -> bool:
        return self._raw_str == other._raw_str

    def __repr__(self):
        """
        Example:
            >>> CubeSet("3 blue, 4 red")
        """
        return f'CubeSet("{self._raw_str}")'

    def count(self, colour: str) -> int:
        for cube in self.cube_counts:
            if cube.colour == colour:
                return cube.count
        return 0


@dataclass(init=False)
class BagOfCubes:
    """Class to represent the bag the games are being played with"""
    cube_set: CubeSet

    def __init__(self, raw_bag_cube_set: str):
        self._raw_str = raw_bag_cube_set
        self.cube_set = CubeSet(raw_cubes=raw_bag_cube_set)

    def __repr__(self):
        """
        Example:
            >>> BagOfCubes("12 red, 13 green, 14 blue")
        """
        return f'BagOfCubes("{self._raw_str}")'

    def is_possible_subset(self, cube_set: CubeSet) -> bool:
        """Returns whether the given set of cubes is possible to be picked out of this bag
        Example:
            >>> BagOfCubes("12 red, 13 green, 14 blue").is_possible_subset(CubeSet("1 green, 3 red, 6 blue"))
            True
            >>> BagOfCubes("12 red, 13 green, 14 blue").is_possible_subset(CubeSet("13 green, 12 red, 60 blue")
            False
        """
        for cube in self.cube_set.cube_counts:
            if cube_set.count(cube.colour) > cube.count:
                return False
        return True


class Game:
    id_number: int
    cube_subsets: tuple[CubeSet, ...]

    def __init__(self, game_number_str: str, subsets_raw_str: str):
        self._raw_str = subsets_raw_str
        self.id_number = int(game_number_str)

        subsets_pattern = r"([^;|$]+)(?:;|$){1}"
        self.cube_subsets = tuple(
            CubeSet(subset_str) for subset_str in re.findall(subsets_pattern, subsets_raw_str)
        )

    def __repr__(self):
        """

        Example:
            >>> Game("1", "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
        """
        return f'Game("{self.id_number}", "{self._raw_str}")'

    def __eq__(self, other: "Game") -> bool:
        return self._raw_str == other._raw_str

    def is_possible_with_bag_of_cubes(self, bag_of_cubes: BagOfCubes) -> bool:
        """Returns whether this game would have been possible with the configuration of cubes in given bag"""
        for cube_subset in self.cube_subsets:
            if not bag_of_cubes.is_possible_subset(cube_subset):
                return False

        return True

    def max_colour_count(self) -> tuple[int, int, int]:
        """Returns the max count of each colour throughout all cube subsets"""
        max_red = 0
        max_blue = 0
        max_green = 0
        for cube_set in self.cube_subsets:
            for cube in cube_set.cube_counts:
                match cube.colour:
                    case "red":
                        max_red = max(max_red, cube.count)
                    case "blue":
                        max_blue = max(max_blue, cube.count)
                    case "green":
                        max_green = max(max_green, cube.count)
        return (max_red, max_blue, max_green)


def parse_puzzle_input(input_raw_str: str) -> list[Game]:
    games = []
    GAME_REGEX = r"Game (\d+): (.*)"
    for game_raw_str in input_raw_str.split("\n"):
        # e.g. `game_raw_str = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"`
        for game_number_str, subsets_raw_str in re.findall(GAME_REGEX, game_raw_str):
            # e.g. game_number_str, subsets_raw_str = ('1', '3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green')

            games.append(
                Game(
                    game_number_str, subsets_raw_str
                )
            )
    return games


def games_possible_with_bag(games: list[Game], bag: BagOfCubes) -> list[Game]:
    possible_games = []
    for game in games:
        if game.is_possible_with_bag_of_cubes(bag):
            possible_games.append(game)
    return possible_games


def sum_of_game_ids_that_are_possible_with_config(raw_games: str) -> int:
    """Determine which games would have been possible if the bag had been loaded with only
    config = 12 red cubes, 13 green cubes, and 14 blue cubes.
    What is the sum of the IDs of those games?"""
    games = parse_puzzle_input(raw_games)

    bag = BagOfCubes("12 red, 13 green, 14 blue")

    possible_games = games_possible_with_bag(games, bag)

    return sum(game.id_number for game in possible_games)


def sum_of_power_of_minimum_set_of_cubes_by_brute_force(raw_games: str) -> int:
    games = parse_puzzle_input(raw_games)

    total = 0
    for game in games:
        total += prod(game.max_colour_count())

    return total

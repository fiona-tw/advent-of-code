from itertools import combinations


class Map:
    def __init__(self, puzzle_input: str, include_harmonics: bool) -> None:
        self.raw_map = puzzle_input
        self.lines = [list(line) for line in self.raw_map.split("\n")]
        self.max_i = len(self.lines) - 1
        self.max_j = len(self.lines[0]) - 1
        self.antenna_positions = self.get_frequency_positions()
        self.antinodes_positions = {
            antenna: set() for antenna in self.antenna_positions
        }
        self.include_harmonics = include_harmonics

    def get_frequency_positions(self) -> dict[str, list[tuple[int, int]]]:
        """Returns the coordinates of all antennas on the map in format (i, j)
            i: index of the line
            j: index of position in the line
        Example:
            {'A': [(5, 6), (8, 8), (9, 9)],
             '0': [(1, 8), (2, 5), (3, 7), (4, 4)]}
        """
        unique_frequencies = set(self.raw_map) - {".", "\n"}
        out = {}
        for frequency in unique_frequencies:
            positions = []
            for i, line in enumerate(self.lines):
                for j, position in enumerate(line):
                    if position == frequency:
                        positions.append((i, j))
            out[frequency] = positions
        return out

    def print_map(self):
        print()
        for i, line in enumerate(self.lines):
            for j, position in enumerate(line):
                print(position, end="")
            print()

    def is_position_on_the_map(self, position: tuple[int, int]) -> bool:
        return 0 <= position[0] <= self.max_i and 0 <= position[1] <= self.max_j

    def set_antinodes_for_antenna_pair(
        self, antenna: str, pair: tuple[tuple[int, int], tuple[int, int]]
    ) -> None:
        distance_x = pair[1][0] - pair[0][0]
        distance_y = pair[1][1] - pair[0][1]

        number_of_antinodes = 2
        if self.include_harmonics:
            number_of_antinodes = max(
                int(self.max_j / distance_x), int(self.max_i / distance_y)
            )

        for harmonic in range(1, number_of_antinodes):
            antinode_one = (
                pair[0][0] - distance_x * harmonic,
                pair[0][1] - distance_y * harmonic,
            )
            antinode_two = (
                pair[1][0] + distance_x * harmonic,
                pair[1][1] + distance_y * harmonic,
            )
            if self.is_position_on_the_map(antinode_one):
                self.antinodes_positions[antenna].add(antinode_one)

            if self.is_position_on_the_map(antinode_two):
                self.antinodes_positions[antenna].add(antinode_two)

        if self.include_harmonics:
            # The antenna positions themselves also count as antinodes when considering harmonics
            self.antinodes_positions[antenna].update(pair)

    def set_antinodes_for_frequency(
        self, antenna: str, positions: list[tuple[int, int]]
    ) -> None:
        for antenna_pair in combinations(positions, 2):
            self.set_antinodes_for_antenna_pair(antenna, antenna_pair)

    def count_antinodes(self) -> int:
        """
        Split map per frequency, for each unique frequency
            look at distance to each other frequency of same type
            check if 2 antinodes are on the map
        """
        for antenna, positions in self.antenna_positions.items():
            self.set_antinodes_for_frequency(antenna, positions)
        unique_antinode_positions = set()
        for frequency_antinode_positions in self.antinodes_positions.values():
            for frequency_antinode_position in frequency_antinode_positions:
                unique_antinode_positions.add(frequency_antinode_position)
        return len(unique_antinode_positions)


def get_number_of_antinodes(puzzle_inputs: str, include_harmonics: bool = False) -> int:
    return Map(puzzle_inputs, include_harmonics).count_antinodes()

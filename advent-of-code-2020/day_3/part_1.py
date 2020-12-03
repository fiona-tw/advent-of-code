from typing import Dict, List, NamedTuple


def load_map(file_name: str):
    with open(file_name, "r") as f:
        raw_map = f.read()
    return Map(raw_map)


TREE = "#"
CLEAR = "."


class Slope(NamedTuple):
    right: int
    down: int


class Map:

    def __init__(self, raw_map) -> None:
        self.map = self.decode_raw_map(raw_map)
        self.unique_len = len(self.map[0])

    def decode_raw_map(self, raw_map: str) -> Dict[int, List[str]]:
        return {
                level_no: list(level_info)
                for level_no, level_info in enumerate(raw_map.split("\n")[:-1])
        }

    def get_route(self, slope: Slope) -> Dict[int, str]:
        start = (0, 0)
        route = {0: CLEAR}
        prev_position = start
        for level_no, level_info in self.map.items():
            if level_no == prev_position[0] + slope.down:
                current_row = level_no
                current_col = prev_position[1] + slope.right
                route[current_row] = level_info[current_col % self.unique_len] 
                prev_position = (current_row, current_col)
        return route


def analyse_route(route: Dict[int, str]) ->  str:
    flattened_route = list(route.values())
    return {
        TREE: flattened_route.count(TREE),
        CLEAR: flattened_route.count(CLEAR),
    }


if __name__ == "__main__":
    example_map = load_map("example_input.txt")
    example_slope = Slope(right=3, down=1)

    route = example_map.get_route(example_slope)
    result = analyse_route(route)

    print(f"Route: {result}")

    real_map = load_map("input.txt")
    real_slope = example_slope
    real_route = real_map.get_route(real_slope)
    result = analyse_route(real_route)

    print(f"Route: {result}")


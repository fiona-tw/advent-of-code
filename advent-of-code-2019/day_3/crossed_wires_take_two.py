# /usr/bin/env python3
import math
from typing import List, NamedTuple, Union


DIR_MAPPING = {
    "U": lambda dist, coord: Coord(x=coord.x, y=coord.y + dist),
    "D": lambda dist, coord: Coord(x=coord.x, y=coord.y - dist),
    "L": lambda dist, coord: Coord(x=coord.x - dist, y=coord.y),
    "R": lambda dist, coord: Coord(x=coord.x + dist, y=coord.y),
}


class Coord(NamedTuple):
    x: int
    y: int

    @property
    def length(self):
        return round(math.sqrt(self.x ^ 2, self.y ^ 2), 2)

    def __add__(self, other_coord):
        return Coord(
            x = self.x + other_coord.x,
            y = self.y + other_corrd.y,
        )

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Coord({self.x}, {self.y})"


class Move:
    dist: int
    direction: Union["U", "D", "L", "R"]

    def __init__(self, move_str):
        self.direction = move_str[0]
        if self.direction not in ["U", "D", "L", "R"]:
            raise ValueError(f"A move must have a valid direction, {self.direction} is not one of them!")
        self.dist = int(move_str[1:])

    def from_coord(self, coord):
        new_coord = DIR_MAPPING[self.direction](self.dist, coord)
        return new_coord


class Path(NamedTuple):
    path_str: str
    delim: str = ","

    def coords(self):
        moves = [Move(move) for move in self.path_str.split(self.delim)]
        out = [Coord(0, 0)]
        for move in moves:
            next_coord = move.from_coord(out[-1])
            out.append(next_coord)
        return out


class Board:

    def __init__(self, paths):
        self.paths = paths
        self.coords = {p: p.coords() for p in self.paths}
        self.setup_dimentions()
        self.setup_board()

    def setup_board(self):
        board = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(".")
            board.append(row)
        self.board = board

    def setup_dimentions(self):
        all_coords = [coord for c_list in self.coords.values() for coord in c_list]
        max_x = sorted(all_coords, key=lambda c: c.x)[-1].x
        min_x = sorted(all_coords, key=lambda c: c.x)[0].x
        max_y = sorted(all_coords, key=lambda c: c.y)[-1].y
        min_y = sorted(all_coords, key=lambda c: c.y)[0].y
        self.centre = Coord(
            x=int((max_x - min_x) / 2),
            y=int((max_y - min_y) / 2),
        )
        self.width = int(max_x - min_x) + 1
        self.height = int(max_y - min_y) + 1

    def mark(self, coord, prev_edge, symbol="X"):
        print(coord, prev_edge)
        if coord.x == prev_edge.x:
            for i in range(1, coord.y - prev_edge.y):
                self.board[prev_edge.y + i][coord.x] = "|"
            self.board[coord.y][coord.x] = symbol
        elif coord.y == prev_edge.y:
            for i in range(1, coord.x - prev_edge.x):
                self.board[coord.y][prev_edge.x + i] = "|"
            self.board[coord.y][coord.x] = symbol
        else:
            raise ValueError("Can only lay straight lines!")

    
    def __lay(self, path):
        edges = path.coords()
        prev_edge = edges[0]
        for edge in edges[1:]:
            self.mark(edge, prev_edge)
            prev_edge = edge
    
    def lay_paths(self):
        for path in self.paths:
            self.__lay(path)


    def __str__(self):
        row_strs = ["".join(row) for row in self.board]
        return "\n".join(row_strs)

if __name__ == '__main__':
    print("👋")
    p1 = Path("R75,D30,R83,U83,L12,D49,R71,U7,L72")
    p2 = Path("U62,R66,U55,R34,D71,R55,D58,R83")
    
    board = Board(paths=[p1, p1])
    
    board.lay_paths()

    print(board)

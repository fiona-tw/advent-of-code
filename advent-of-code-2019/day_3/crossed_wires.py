#!/usr/bin/env python
import math
from collections import defaultdict
from copy import deepcopy
from typing import List, NamedTuple


class DuplicateWire(Exception):
    pass


class InvalidOperation(Exception):
    pass


class InvalidCoordinate(InvalidOperation):
    pass


class InvalidMove(InvalidOperation):
    pass


class Coord:
    x: int
    y: int

    def __init__(self, x, y):
        #if x < 0 or y < 0:
        #    raise InvalidCoordinate(f"({x}, {y})")
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coord({self.x}, {self.y})"

    @property
    def length(self):
        if float(self.x) == 0.0 and float(self.y) == 0.0:
            return 0.0
        return round(math.sqrt(self.x * self.x + self.y * self.y), 2)

    def __gt__(self, other):
        self_length = self.length 
        other_length = other.length
        if self_length > other_length:
            return self
        return other

class Move(NamedTuple):
    direction: str
    dist: int


OP = {
    'L': lambda from_coord, step: Coord(from_coord.x - step, from_coord.y),
    'R': lambda from_coord, step: Coord(from_coord.x + step, from_coord.y),
    'U': lambda from_coord, step: Coord(from_coord.x, from_coord.y - step),
    'D': lambda from_coord, step: Coord(from_coord.x, from_coord.y + step),
}

class Path(NamedTuple):
    path: str
    delim: str = ","

    @property
    def directions(self) -> List[Move]:
        out = []
        raw_directions = self.path.split(self.delim)
        for raw_dir in raw_directions:
            turn = raw_dir[0]
            dist = int(raw_dir[1:])
            out.append(Move(turn, dist))
        return out
    
    @property
    def edges(self):
        out = [Coord(0,0)]
        for direction in self.directions:
            prev = out[-1]
            next_coord  = OP[direction.direction](prev, direction.dist)
            out.append(next_coord)
        return out
        

    @property
    def size(self):
        dirs = self.directions
        up = sum([move.dist for move in dirs if move.direction == "U"])
        down = sum([move.dist for move in dirs if move.direction == "D"])
        left = sum([move.dist for move in dirs if move.direction == "L"])
        right = sum([move.dist for move in dirs if move.direction == "R"])
        return Size(
            centre=Coord(x=round((left + right) / 2.0), y=round((up + down) / 2.0)),
            height = max(up, down),
            width = max(left, right),
        )


class Size(NamedTuple):
    centre: Coord
    width: int
    height: int


class Board:

    SYMBOL = {
        'L': '-',
        'R': '-',
        'U': '|',
        'D': '|',
    }

    OP = {
        'L': lambda from_coord, step: Coord(from_coord.x - step, from_coord.y), 
        'R': lambda from_coord, step: Coord(from_coord.x + step, from_coord.y), 
        'U': lambda from_coord, step: Coord(from_coord.x, from_coord.y - step), 
        'D': lambda from_coord, step: Coord(from_coord.x, from_coord.y + step), 
        }

    def __init__(self, size: Size):
        self.x = size.width
        self.y = size.height
        self.port = size.centre
        self.board = [['.' for _ in range(width)] for _ in range(height)]
        self.wire_pos = defaultdict(Coord)
        self.draw("o", self.port)


    def draw(self, symbol: str, coord: Coord):
        self.board[coord.y][coord.x] = symbol

    def __str__(self):
        out = []
        for row_num, row in enumerate(self.board):
            out.append(f"{row_num:2} ")
            for cell in row:
                out.append(cell)
            out.append('\n')
        return "".join(out)

    def lay_wire(self, id_: int, path: Path):
        if id_ in self.wire_pos:
            raise DuplicateWire(f"You have already defined a wire with id: {id_}")
    
        self.__lay(id_, path)
        print()

    def __move(self, start: Coord, move: Move) -> Coord:
        sym = self.SYMBOL[move.direction]
        # incase there is an error in move and we want to discard these changes to board
        board = deepcopy(self.board)
        try:
            for step in range(1, move.dist + 1):
                step_method = self.OP[move.direction]
                step_pos = step_method(start, step)
                board[step_pos.y][step_pos.x] = sym
        except IndexError:
            raise InvalidMove()
        self.board = board
        return Coord(step_pos.x, step_pos.y)

    def __evaluate(self, id_, move: Move):
        """writing first assuming right is direction"""
        print(move)
        start = self.wire_pos[id_]
        if self.board[start.y][start.x] != 'o':
            self.board[start.y][start.x] = '+'
        try:
            end = self.__move(start, move)
        except InvalidOperation:
            print(self)
            print(f"Invalid move: {move}")
        else:
            self.wire_pos[id_] = end

    def __lay(self, id_: int, path: Path):
        self.wire_pos[id_] = self.port
        for move in path.directions:
            self.__evaluate(id_, move)
    

def build(board: Board, paths: List[Path]):
    for i,path in enumerate(paths):
        board.lay_wire(i + 1, path)

    if 1 in board.wire_pos and 2 in board.wire_pos:
        print(board)


def get_max_size(paths: List[Path]) -> Size:
    max_width = max([p.size.width for p in paths])
    max_height = max([p.size.height for p in paths])
    first_guess =  Size(
        width=max_width,
        height=max_height,
        #centre=Coord(round(max_width/2), round(max_height/2))
        centre=Coord(0, 0)
    )
    import ipdb; ipdb.set_trace()

    return first_guess

def part_1(width, height):
    puzzle_paths = [
        Path("R75,D30,R83,U83,L12,D49,R71,U7,L72"),
        Path("U62,R66,U55,R34,D71,R55,D58,R83"),
    ]

    board_paths = [Path("R2,U2,L2"), Path("R2,R2,R2,R2")]
    board_paths = puzzle_paths
    
    board_size = get_max_size(board_paths)
    print(board_size)
    board = Board(board_size)
    build(board, board_paths)

if __name__ == '__main__':
    import sys
    inputs = sys.argv[1:]
    width = int(inputs[0]) if inputs else 20
    height = int(inputs[1]) if len(inputs) > 1 else 12
    part_1(width, height)
    


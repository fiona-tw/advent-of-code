from copy import deepcopy

EMPTY = "L"
FLOOR = "."
OCCUPIED = "#"


class SeatModel:
    def __init__(self, filename: str, part_no: int) -> None:
        with open(f"day_11/{filename}", "r") as f:
            raw_layout = f.read()[:-1].split("\n")

        self.seat_layout = [
            [char for char in row]
            for row in raw_layout
        ]
        self.prev_layout = self.seat_layout

        self.num_rows = len(self.seat_layout)
        self.num_cols = len(self.seat_layout[0])

        self.all_coords = [
            (x, y)
            for y in range(self.num_cols)
            for x in range(self.num_rows)
        ]

        # list of all FLOOR coordinates (i.e. which are always stable / never change)
        self.stable_coords = [
            coord for coord in self.all_coords
            if self.seat_layout[coord[0]][coord[1]] == FLOOR
        ]
        # list of all non-floor coordinates
        self.seat_coords = list(set(self.all_coords) - set(self.stable_coords))

        self.count_method = {
            1: self.num_occupied_adjacent_seats,
            2: self.num_occupied_visible_seats,
        }[part_no]

    def num_occupied_adjacent_seats(self, row: int, col: int) -> int:
        counter = 0
        if self.prev_layout[row][col] == OCCUPIED:
            # as we will double count this below!
            counter = -1

        min_row = max(0, row - 1)
        min_col = max(0, col - 1)
        max_row = min(row + 1, self.num_rows - 1)
        max_col = min(col + 1, self.num_cols - 1)

        for check_row in range(min_row, max_row + 1):
            for check_col in range(min_col, max_col + 1):
                value = self.prev_layout[check_row][check_col]
                if value == OCCUPIED:
                    counter += 1
        return counter

    def num_occupied_visible_seats(self, row: int, col: int) -> int:
        counter = 0

        left = lambda i: col - i
        right = lambda i: col + i
        up = lambda i: row - i
        down = lambda i: row + i

        left_lim = col + 1
        right_lim = self.num_cols - col + 1
        up_lim = row + 1
        down_lim = self.num_rows - row + 1

        directions = [
            (
                ("UL", up(i), left(i))
                for i in range(1, max(up_lim, left_lim))
            ), (
                ("U_", up(i), col)
                for i in range(1, up_lim)
            ), (
                ("UR", up(i), right(i))
                for i in range(1, max(up_lim, right_lim))
            ), (
                ("_R", row, right(i))
                for i in range(1, right_lim)
            ), (
                ("DR", down(i), right(i))
                for i in range(1, max(down_lim, right_lim))
            ), (
                ("D_", down(i), col)
                for i in range(1, down_lim)
            ), (
                ("DL", down(i), left(i))
                for i in range(1, max(down_lim, left_lim))
            ), (
                ("_L", row, left(i))
                for i in range(1, left_lim)
            )]

        for direction in directions:
            for direction_name, check_row, check_col in direction:
                assert (check_row, check_col) != (row, col)

                if check_row < 0 or check_col < 0:
                    # negative indexing is supported and NOT wanted here!
                    break

                try:
                    value = self.prev_layout[check_row][check_col]
                except IndexError:
                    # this means we've fallen off grid so stop
                    # looking in this direction
                    break

                if value == FLOOR:
                    continue

                if value == OCCUPIED:
                    counter += 1

                # stop counting in this direction once non-floor reached
                break

        return counter

    def next_state(self, row: int, col: int) -> str:
        """
        - If a seat is empty (L) and there are no occupied
          seats adjacent to it, the seat becomes occupied.
        - If a seat is occupied (#) and four or more seats
          adjacent to it are also occupied, the seat becomes empty.
        - Otherwise, the seat's state does not change.
        - Floor (.) never changes; seats don't move, and nobody sits on the floor.
        """
        current_state = self.prev_layout[row][col]
        occupied_adjacent_seats = self.count_method(row, col)

        if current_state == EMPTY and occupied_adjacent_seats == 0:
            return OCCUPIED
        if current_state == OCCUPIED and occupied_adjacent_seats >= 5:
            return EMPTY
        return current_state

    def next(self) -> None:
        self.prev_layout = deepcopy(self.seat_layout)
        for row, col in self.seat_coords:
            self.seat_layout[row][col] = self.next_state(row, col)

    def print(self):
        print("=" * (self.num_cols + 10))
        for row in self.seat_layout:
            print("     ", "".join([
                # self.decode[x] for x in row
                x for x in row
            ]))
        print(self.prev_layout == self.seat_layout)
        print("=" * (self.num_cols + 10))

    def print_iterations(self, i: int) -> None:
        for _ in range(i):
            self.next()
            self.print()

    def stabilise_layout(self) -> None:
        while True:
            self.next()
            # self.print()
            if self.prev_layout == self.seat_layout:
                break

    def get_stable_count(self) -> int:
        self.stabilise_layout()
        return sum(self.seat_layout, []).count(OCCUPIED)


if __name__ == "__main__":
    model_part_1 = SeatModel("input.txt", part_no=1)
    print(model_part_1.get_stable_count())
    model_part_2 = SeatModel("input.txt", part_no=2)
    print(model_part_2.get_stable_count())

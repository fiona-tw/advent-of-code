from collections import defaultdict
from math import ceil
from operator import itemgetter
from typing import Tuple, Dict, Callable, List

NO_ROWS = 127  # starting from 0
NO_COLS = 7  # starting from 0


def sub_from_max(min_val: int, max_val: int, width: int) -> Tuple[int, int]:
    return min_val, max_val - ceil(width / 2)


def add_to_min(min_val: int, max_val: int, width: int) -> Tuple[int, int]:
    return min_val + ceil(width / 2), max_val


ROW_MAPPING = {
    "F": sub_from_max,
    "B": add_to_min,
}

COL_MAPPING = {
    "L": sub_from_max,
    "R": add_to_min,
}


def get_seat_id(row: int, col: int) -> int:
    return 8 * row + col


def decode(min_val: int, max_val: int, mapping: Dict[str, Callable], value: str) -> int:
    width = max_val - min_val
    for char in value:
        min_val, max_val = mapping[char](min_val, max_val, width)
        width = max_val - min_val
    if width != 0:
        raise AssertionError("Something's gone wrong!")
    return min_val


def decode_boarding_pass(boarding_pass: str) -> Tuple[int, int]:
    raw_row = boarding_pass[:7]
    raw_col = boarding_pass[-3:]
    assert raw_row + raw_col == boarding_pass

    row = decode(0, NO_ROWS, ROW_MAPPING, raw_row)
    col = decode(0, NO_COLS, COL_MAPPING, raw_col)
    return row, col


def scan_boarding_passes(boarding_pass_file_name: str) -> Dict[str, Tuple[int, int]]:
    with open(boarding_pass_file_name, "r") as f:
        passes = f.read()[:-1].split("\n")
    return {
        boarding_pass: decode_boarding_pass(boarding_pass)
        for boarding_pass in passes
    }


def get_max_seat_id(boarding_pass_file_name: str) -> int:
    decoded_passes = scan_boarding_passes(boarding_pass_file_name)
    return max(get_seat_id(row, col) for row, col in decoded_passes.values())


print(get_max_seat_id("input.txt"))


def find_missing_seat_id(boarding_pass_file_name: str) -> List[int]:
    decoded_passes = scan_boarding_passes(boarding_pass_file_name)
    sorted_by_col = sorted(decoded_passes.values(), key=itemgetter(1))

    """# Build up the dict repr of plane with key=row and value=list of filled seat indices
    e.g.
    {
        100: [0, 1, 2, 3, 4, 5, 6, 7],  # i.e. row 100 has __all__ seats occupied 
        ...
    }
    """
    row_to_col = defaultdict(list)
    for row, col in sorted_by_col:
        row_to_col[row].append(col)

    """# Loops through each row to find the rows that contain unoccupied seats
        e.g.
        {
            100: [0, 1, 2, 3, 4, 5, 6, 7],  # i.e. row 100 has __all__ seats occupied 
            ...
        }
        """
    for row, cols_occupied in row_to_col.items():

        if len(cols_occupied) == NO_COLS + 1:
            # this row is fully occupied so my seat cannot be in this row!
            continue

        # note: seat ids is sorted as cols_occupied is sorted [and seat_id per row is ascending in col]
        seat_ids = [get_seat_id(row, col) for col in cols_occupied]

        # probs better way of doing this bit...
        incrementing_rows = [seat_ids[0] + i for i in range(len(seat_ids))]
        if seat_ids == incrementing_rows:
            # This row does not contain a seat with filled seats +/-1 next to it
            continue
        return seat_ids

    raise AssertionError("Something's gone wrong...")


found_ids = find_missing_seat_id("input.txt")

print(f"Missing seat ID is in {found_ids}")


def better_find_missing_seat_id(boarding_pass_file_name: str) -> int:
    seat_ids = sorted([
        get_seat_id(row, col)
        for row, col in scan_boarding_passes(boarding_pass_file_name).values()
    ])
    min_id = min(seat_ids)
    missing_ids = []
    for seat_id in range(min_id, min_id + len(seat_ids)):
        if seat_id not in seat_ids:
            missing_ids.append(seat_id)
    if len(missing_ids) != 1:
        raise AssertionError("Something's gone wrong...")
    return missing_ids[0]


print(better_find_missing_seat_id("input.txt"))

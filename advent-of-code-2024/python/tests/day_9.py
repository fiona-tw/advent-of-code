from solutions.logic.day_9 import get_checksum, get_ordered_diskmap, get_expanded_diskmap

def test_get_ordered_diskmap():
    assert get_ordered_diskmap("12345") == "022111222......"
    assert get_ordered_diskmap("01234") == "211222...."


def test_simple_case():
    puzzle_input = "12345"
    assert get_expanded_diskmap(puzzle_input) == "0..111....22222"
    assert get_ordered_diskmap(puzzle_input) == "022111222......"
    assert get_checksum(puzzle_input) == 60

def test_no_empty_space():
    puzzle_input = "90909"
    assert get_expanded_diskmap(puzzle_input) == "000000000111111111222222222"
    assert get_ordered_diskmap(puzzle_input) == "000000000111111111222222222"
    assert get_checksum(puzzle_input) == 513


def test_file_id_gt_9():
    puzzle_input = "1010101010101010101020101"
    assert get_expanded_diskmap(puzzle_input) == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "10", "11", "12"]
    assert get_ordered_diskmap(puzzle_input) == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "10", "11", "12"]
    assert get_checksum(puzzle_input) == 783


def test_example():
    puzzle_input = "2333133121414131402"
    assert get_expanded_diskmap(puzzle_input) == "00...111...2...333.44.5555.6666.777.888899"
    assert get_ordered_diskmap(puzzle_input) == "0099811188827773336446555566.............."
    assert get_checksum(puzzle_input) == 1928

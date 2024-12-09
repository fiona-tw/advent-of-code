def get_expanded_diskmap(puzzle_input: str) -> list[str]:
    ordered_block = []
    for i, file_id in enumerate(puzzle_input):
        if i % 2 == 0:
            # file block
            ordered_block += [str(round(i / 2))] * int(file_id)
        else:
            # free space
            ordered_block += ["."] * int(file_id)

    return ordered_block


def find_rightmost_file_from_index(diskmap, start_at_index) -> int:
    for j in range(start_at_index, -1, -1):
        if diskmap[j] != ".":
            return j


def get_ordered_diskmap(puzzle_input: str) -> list[str]:
    ordered_block = []
    diskmap = get_expanded_diskmap(puzzle_input)
    moved = []
    # The first file to move will be the right most file, so start with this index
    last_moved_index = find_rightmost_file_from_index(diskmap, start_at_index=len(diskmap) - 1)
    for i, file_id in enumerate(diskmap):
        if last_moved_index < i:
            # then we've moved past all chars to move, the rest will be free spaces we will add on outside the loop
            break
        elif file_id == ".":
            ordered_block += diskmap[last_moved_index]
            moved.append(last_moved_index)

            # Keep track of indices that have been moved so they can be replaced with "."
            # start from the position to the left of the last moved char
            last_moved_index = find_rightmost_file_from_index(diskmap, start_at_index=last_moved_index - 1)

        elif i in moved:
            ordered_block.append(".")
        else:
            ordered_block.append(file_id)

    return ordered_block + ["."] * (len(diskmap) - len(ordered_block))


def get_checksum(puzzle_input: str) -> int:
    ordered_diskmap = get_ordered_diskmap(puzzle_input)
    checksum = 0
    for i, file_id in enumerate(ordered_diskmap):
        if file_id == ".":
            break
        checksum += i * int(file_id)
    return checksum

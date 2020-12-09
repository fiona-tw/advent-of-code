from math import prod
from time import time
from typing import Iterator, List, Tuple


class SubsetDoesNotExist(Exception):
    pass


class PairDoesNotExist(SubsetDoesNotExist):
    pass


def get_pair_that_sums_to(report: List[int], total: int) -> Tuple[int, int]:
    """Returns a pair of ints in `report` that sum to `total`

    Raises:
        PairDoesNotExist: if no pair in `report` sums to `total`
    """
    report_length = len(report)
    sorted_report = sorted(report, reverse=True)

    for index, current_value in enumerate(sorted_report):
        if index < report_length - 1:
            looking_for_value = total - current_value

            if looking_for_value in sorted_report[index:]:
                return current_value, looking_for_value

            # if the next value in __sorted__ list is lower than required --> no pair exists
            if looking_for_value > sorted_report[index + 1]:
                break

    # if we have reached the end of the report without returning then no pair exists in given report!
    raise PairDoesNotExist(f"Report does not contain a pair that sums to {total}!")


def get_subset_that_sums_to(report: Iterator[int], total: int, size: int, depth: int = 0) -> Tuple[int, ...]:
    """Returns a tuple with len `size` of ints in `report` that sum to given `total`

    Raises:
        SubsetDoesNotExist: if `report` does not contain exactly `size` ints that sum to `total`
    """
    sorted_report = sorted(report, reverse=True)

    for index, current_value in enumerate(sorted_report):

        # for given current_value (decreasing in size) we want to find size-1 that sums to remaining total
        sub_report = sorted_report[index + 1:]
        sub_total = total - current_value
        sub_size = size - 1

        # if we're looking for a total that is larger than sum of the highest next ints --> SubsetDoesNotExist
        if sub_total > sum(sub_report[:sub_size]):
            raise SubsetDoesNotExist(
                f"Sub-report {sub_report} does not contain a subset of size {sub_size} that sums to {sub_total}!"
            )

        # if we're down to the final pair use above method to find the pair
        if size == 2:
            try:
                return get_pair_that_sums_to(list(sub_report), total)
            except PairDoesNotExist:
                continue

        # assuming we are dealing with positive ints!
        elif sub_total < 0:
            continue

        elif sub_size == 2:
            try:
                val1, val2 = get_pair_that_sums_to(sub_report, sub_total)
            except PairDoesNotExist:
                continue
            else:
                return current_value, val1, val2

        elif size > 2:
            try:
                get_subset_that_sums_to(sub_report, sub_total, sub_size, depth + 1)
            except SubsetDoesNotExist:
                continue
            else:
                others = get_subset_that_sums_to(sub_report, sub_total, sub_size, depth + 1)
                return tuple([current_value] + list(others))
    raise SubsetDoesNotExist("")


def read_report(file_name: str) -> List[int]:
    raw_report = open(file_name, "r").read()
    # remove last element as that is always empty str
    return [int(row) for row in raw_report.split("\n")[:-1]]


def part_1():
    report_name = "input.txt"
    report = read_report(report_name)
    try:
        val1, val2 = get_pair_that_sums_to(report, 2020)
    except PairDoesNotExist as err:
        print(f"ERROR: {err}")
        return None
    result = val1 * val2
    print(f"Part 1: result={result}")


def part_2(report_name: str, total: int, size: int) -> None:
    start = time()

    report = read_report(report_name)
    values = get_subset_that_sums_to(report, total, size)

    end = time()

    print(f"found values: {values}")
    print(f"time take (s): {end - start}")
    print(f"Part 2: result={prod(values)}")


part_1()
part_2("input.txt", 2020, 3)  # 292093004

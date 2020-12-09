from copy import deepcopy
from typing import List, Tuple


class PairDoesNotExist(Exception):
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


# ############################################## DAY 1 CODE COPIED ABOVE ##############################################


class NotFound(Exception):
    pass


def load_data(filename: str) -> List[int]:
    with open(f"day_9/{filename}", "r") as f:
        return [int(num) for num in f.read()[:-1].split("\n")]


def find_invalid_value(data: List[int], preamble_length: int) -> int:
    """Returns the first invalid value of data with given preamble length"""
    data_copy = deepcopy(data)

    for i, value in enumerate(data_copy[preamble_length:]):
        preamble = data_copy[i:i + 25]
        try:
            get_pair_that_sums_to(preamble, value)
        except PairDoesNotExist:
            return value

    raise NotFound(f"Given data set does not contain any invalid values for preamble length of {preamble_length}!")


def find_weakness(data: List[int], total: int) -> int:
    data_len = len(data)
    for index in range(data_len):
        # starting at data[index] scan upwards until the sum of that contiguous set equals or exceeds `total`
        for sub_width in range(data_len - index - 1):
            contiguous_set = data[index:sub_width]
            running_total = sum(contiguous_set)
            if running_total > total:
                # no need to continue adding numbers starting at `index` as sum will only increase further past `total`!
                break  # i.e. go to next index and re-scan
            elif running_total == total:
                return min(contiguous_set) + max(contiguous_set)

    raise NotFound(f"No contiguous set exists in given data that sums to {total}!")


if __name__ == "__main__":
    invalid_value = find_invalid_value(load_data("input.txt"), preamble_length=25)
    weakness = find_weakness(load_data("input.txt"), total=invalid_value)

    print(f"[PART 1]  invalid value = {invalid_value}")
    print(f"[PART 2]  encryption weakness = {weakness}")

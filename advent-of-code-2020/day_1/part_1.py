from time import sleep
from typing import List, Optional, Tuple


class PairDoesNotExist(Exception):
    pass


def get_pair_that_sums_to(report: List[int], total: int) -> Tuple[int, int]:
    report_length = len(report)
    sorted_report = sorted(report, reverse=True)
    for index, current_value in enumerate(sorted_report):
        print(".", end="", flush=True)
        if index < report_length - 1:
            looking_for_value = total - current_value
            if looking_for_value in sorted_report[index:]:
                return (current_value, looking_for_value)
            if looking_for_value > report[index + 1]:
                break  # the next value in __sorted__ list is lower than required --> no pair exists
        sleep(0.005)
    raise PairDoesNotExist(f"Report does not contain a pair that sums to {total}")
        

def analyse_report(report: List[int], total: int) -> Optional[int]:
    try:
        val1, val2 = get_pair_that_sums_to(report, total)
    except PairDoesNotExist as err:
        print(f"ERROR: {err}")
        return None
    return val1 * val2


def read_report(file_name: str) -> List[int]:
    raw_report = open(file_name, "r").read()
    return [
            int(row) for row in raw_report.split("\n")[:-1]
    ]

if __name__ == "__main__":
    report_name = "input.txt"
    print(f"analysing report {report_name}")
    report = read_report(report_name)
    result = analyse_report(report, total=2020)
    print(f"\nresult = {result}")
    

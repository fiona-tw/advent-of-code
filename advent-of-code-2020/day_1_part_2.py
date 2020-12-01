from math import prod
from time import sleep, time
from typing import List, Optional, Tuple


DEBUG = False


class PairDoesNotExist(Exception):
    pass

class SubsetDoesNotExist(Exception):
    pass


def get_pair_that_sums_to(report: List[int], total: int) -> Tuple[int, int]:
    report_length = len(report)
    sorted_report = sorted(report, reverse=True)
    
    for index, current_value in enumerate(sorted_report):
        if index < report_length - 1:
            looking_for_value = total - current_value
            if looking_for_value in sorted_report[index:]:
                return (current_value, looking_for_value)
            if looking_for_value > report[index + 1]:
                break  # the next value in __sorted__ list is lower than required --> no pair exists
    raise PairDoesNotExist(f"Report does not contain a pair that sums to {total}!")


def log(depth, msg):
    if DEBUG == True:
        pad = "\t" * depth if depth else ""
        print(pad, msg)


def test(report, total, size, depth=0):
    sorted_report = sorted(report, reverse=True)
    
    log(depth, f"Problem is to find {size} values that sum to {total} in {report}.")
    log(depth, "------------------------------------------------------------------\n")
    
    for index, current_value in enumerate(sorted_report):
        subreport = sorted_report[index + 1:]
        subtotal = total - current_value
        subsize = size - 1
        log(depth, f"Looking at: {current_value}")
        log(depth, f"sub-report: {subreport}")
        log(depth, f"sub-total: {subtotal}")
        log(depth, f"sub-size: {subsize}")

        # TODO: Clean up nasty logic below!

        if subtotal > sum(subreport[:subsize]):
            raise SubsetDoesNotExist(f"Subreport {subreport} does not contain a subset of size {subsize} that sums to {subtotal}!")
        
        if size == 2 and subtotal > 0:
            try:
                log(depth, f"finding pair with total {total} in {subreport}")
                return get_pair_that_sums_to(subreport, total)
            except PairDoesNotExist:
                continue
        if subsize == 1 and subtotal in subreport:
            return subtotal
        elif subsize == 1 and subtotal == 0:
            log(depth, f"FOUND: {current_value} returned")
            return current_value
        elif subsize == 1:
            continue  # ??

        elif subtotal < 0:
            print(f"CONTINUE: current value ({current_value}) too large")
            continue
        elif subsize == 2:
            log(depth, f"running pair method")
            try:
                val1, val2 = get_pair_that_sums_to(subreport, subtotal)
            except PairDoesNotExist:
                log(depth, f"could not find pair to sum to {subtotal} to use alongside {current_value} for total {total}")
                continue
            else:
                return current_value, val1, val2
        elif size > 2:
            log(depth, f"running sub test method")
            try:
                remaining_values = test(subreport, subtotal, subsize, depth+1)
            except SubsetDoesNotExist:
                continue
            else:
                log(depth, f"RETURN: {current_value} with result from ' test({subreport}, {subtotal}, {subsize}, {depth+1})'")
                return current_value, test(subreport, subtotal, subsize, depth+1)


def read_report(file_name: str) -> List[int]:
    raw_report = open(file_name, "r").read()
    # remove last element as that is always empty str
    return [int(row) for row in raw_report.split("\n")[:-1]]


def run_analysis():
    report_name = "day_1_input.txt"
    
    start = time()

    report = read_report(report_name)
    triplet = test(report, 2020, 3)
    
    end = time()
    
    print(f"found triplet: {triplet}")
    print(f"time take (s): {end - start}")
    print(f"result: {prod(triplet)}")


if __name__ == "__main__":
    run_analysis()


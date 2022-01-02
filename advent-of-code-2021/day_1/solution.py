from typing import List, Optional


def clean_input(measurements: str) -> List[int]:
    return [int(measurement) for measurement in measurements.split("\n")[:-1]]


def count_increases(measurements: str) -> int:
    cleaned_measurements = clean_input(measurements)
    out = 0
    last_measurement = cleaned_measurements[0]
    for measurement in cleaned_measurements[1:]:
        if measurement > last_measurement:
            out += 1
        last_measurement = measurement
    return out


def count_rolling_increases(measurements: str, window: Optional[int] = 3) -> int:
    """This method counts how many times the rolling sum of the given window size is
    larger than the window before it.

    The window sum is calculated by subtracting the first measurement in the last window
    and adding the last measurement in the current window, this is done by enumerated
    over the array, accessing another element once per iteration
    """
    cleaned_measurements = clean_input(measurements)
    out = 0

    first_measurement_in_last_window = cleaned_measurements[0]
    last_window_sum = sum(cleaned_measurements[:window])
    for i, last_measurement_in_this_window in enumerate(
        cleaned_measurements[window:], 1
    ):
        window_sum = (
            last_window_sum
            - first_measurement_in_last_window
            + last_measurement_in_this_window
        )
        if window_sum > last_window_sum:
            out += 1
        first_measurement_in_last_window = cleaned_measurements[i]
        last_window_sum = window_sum

    return out


def count_rolling_increases_2(measurements: str, window: Optional[int] = 3) -> int:
    """As above, instead of altering the rolling sum, keeps track of what indicies need
    accessing and calculating the sum on the fly"""
    cleaned_measurements = clean_input(measurements)
    out = 0

    last_window_sum = sum(cleaned_measurements[0: window - 1])
    for i in range(0, len(cleaned_measurements) - window):
        window_sum = sum(cleaned_measurements[i: i + window])
        if window_sum > last_window_sum:
            out += 1
        last_window_sum = window_sum

    return out


if __name__ == "__main__":
    example = input("Run for example? [y/n] ")
    filename = "example_input.txt" if example == "y" else "input.txt"
    with open(filename, "r") as f:
        raw_measurements = f.read()
    print("No. of simple increases: \t\t", count_increases(raw_measurements))
    print(
        "No. of increases in sliding window: \t",
        count_rolling_increases(raw_measurements),
    )

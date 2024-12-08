import sys

from solutions.logic.day_1 import get_similarity_score
from solutions.logic.day_2 import get_count_of_safe_reports
from solutions.logic.day_3 import scan_corrupted_memory
from solutions.logic.day_4 import get_x_mas_count
from solutions.logic.day_5 import get_sum_of_middle_pages_from_correctly_ordered_incorrect_updates
from solutions.logic.day_6 import count_number_of_places_for_obstruction
from solutions.logic.day_7 import get_calibration_result


def _get_input_for_day(day: int) -> str:
    with open(f"solutions/puzzle_inputs/day_{day}.txt") as file:
        return file.read()


def run_day_1():
    """
    Answers:
        Part 1: 1938424
        Part 2: 22014209
    """
    # return get_distance_sum(_get_input_for_day(1))
    return get_similarity_score(_get_input_for_day(1))


def run_day_2():
    """
    Answers:
        Part 1: 246
        Part 2: 318
    """
    return get_count_of_safe_reports(_get_input_for_day(2))


def run_day_3():
    """
    Answers:
        Part 1: 166905464
        Part 2: 72948684
    """
    return scan_corrupted_memory(_get_input_for_day(3))


def run_day_4():
    """
    Answers:
        Part 1: 2530
        Part 2: 1921
    """
    # return get_xmas_count(_get_input_for_day(4))
    return get_x_mas_count(_get_input_for_day(4))


def run_day_5():
    """
    Answers:
        Part 1: 6384
        Part 2: 5353
    """
    return get_sum_of_middle_pages_from_correctly_ordered_incorrect_updates(_get_input_for_day(5))


def run_day_6():
    """
    Answers:
        Part 1: 4977
        Part 2: 1729
    """
    return count_number_of_places_for_obstruction(_get_input_for_day(6))


def run_day_7():
    """
    Answers:
        Part 1: 20281182715321
        Part 2:
    """
    return get_calibration_result(_get_input_for_day(7))


def run_for_day_x(day: int):
    try:
        return globals()[f"run_day_{day}"]()
    except KeyError:
        print(
            f"No solution implemented for day {day}.\t(`run_day_{day}` does not exist!)"
        )


def run():
    day = sys.argv[1]  # i.e. 1 or 2 etc.
    try:
        day = int(day)
    except ValueError:
        print(
            f"Please supply the day as a number for the puzzle you want to run\n\t('{day}' is not an integer!)"
        )
    else:
        print(f"\nDay {day} solution:\n")
        print(run_for_day_x(day))


if __name__ == "__main__":
    run()

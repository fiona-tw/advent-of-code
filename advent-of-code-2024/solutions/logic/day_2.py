def diff_is_safe(elem_1, elem_0: int, increasing: bool) -> bool:
    diff = elem_1 - elem_0
    if increasing:
        return 1 <= diff <= 3
    return -3 <= diff <= -1

def remove_element(report, i):
    copied_report = report.copy()
    copied_report.pop(i)
    return copied_report

def report_is_safe(report: list[int], problem_dampener: bool = False) -> bool:
    """Returns whether an individual report is considered safe

    Note:
        The problem dampener is turned OFF by default
        If turned on, it will deem a report safe if one level can be removed and still produce a safe report
    """
    increasing = report[1] > report[0]
    for i, level in enumerate(report[:-1]):
        if not diff_is_safe(report[i + 1], level, increasing=increasing):
            if problem_dampener:
                return (
                    report_is_safe(remove_element(report, i - 1)) or
                    report_is_safe(remove_element(report, i)) or
                    report_is_safe(remove_element(report, i + 1))
                )
            return False
    return True

def get_count_of_safe_reports(puzzle_input: str) -> int:
    """A report is considered safe when:

        - The levels are either all increasing or all decreasing.
        - Any two adjacent levels differ by at least one and at most three.
    """
    reports = []
    for report_str in puzzle_input.split("\n"):
        report = [int(level) for level in report_str.split(" ")]
        if report_is_safe(report, problem_dampener=True):
            reports.append(report)

    return len(reports)

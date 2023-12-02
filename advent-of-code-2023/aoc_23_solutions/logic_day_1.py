import re

from copy import deepcopy

CHAR_TO_INT = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}
CHAR_TO_INT.update({
    str(i): i for i in range(1, 10)
})

NUMBERS_PATTERN = "|".join(CHAR_TO_INT.keys())

FIRST_NUMBER = re.compile(rf"^({NUMBERS_PATTERN}).*")
LAST_NUMBER = re.compile(rf".*({NUMBERS_PATTERN})$")


def match_first_number(raw_line: str) -> int:
    line = deepcopy(raw_line)
    while line:
        matches = re.match(FIRST_NUMBER, line)
        if matches:
            return CHAR_TO_INT[matches.groups()[0]]
        else:
            line = line[1:]


def match_last_number(raw_line: str) -> int:
    line = deepcopy(raw_line)
    while line:
        matches = re.match(LAST_NUMBER, line)
        if matches:
            return CHAR_TO_INT[matches.groups()[0]]
        else:
            line = line[:-1]


class CalibrationValue:
    first_digit: int
    last_digit: int

    def __init__(self, raw_line: str) -> None:
        self.raw_line = raw_line
        self.first_digit = match_first_number(raw_line)
        self.last_digit = match_last_number(raw_line)

    def __repr__(self) -> str:
        return f"CalibrationValue('{self.raw_line}')"

    def __eq__(self, other) -> bool:
        return self.first_digit == other.first_digit and self.last_digit == other.last_digit

    @property
    def value(self) -> int:
        return int(f"{self.first_digit}{self.last_digit}")


class CalibrationDocument:
    lines: list[CalibrationValue]

    def __init__(self, raw_doc: str) -> None:
        self.raw_doc = raw_doc
        self.lines = [CalibrationValue(line) for line in self.raw_doc.split("\n")]

    def sum(self) -> int:
        return sum(line.value for line in self.lines)


def sum_of_calibration_values(raw_calibration_document: str) -> int:
    return CalibrationDocument(raw_calibration_document).sum()

import re
from typing import Callable, Dict, Tuple


class BasicValidator:

    def __init__(self):
        self.field_to_rules = {
            "byr": lambda value: True,  # (Birth Year)
            "iyr": lambda value: True,  # (Issue Year)
            "eyr": lambda value: True,  # (Expiration Year)
            "hgt": lambda value: True,  # (Height)
            "hcl": lambda value: True,  # (Hair Color)
            "ecl": lambda value: True,  # (Eye Color)
            "pid": lambda value: True,  # (Passport ID)
            "cid": lambda value: True,  # (Country ID)
        }

    def validate(self, field_name: str, field_value: str) -> bool:
        try:
            return self.field_to_rules[field_name](field_value)
        except KeyError:
            return False


class PassportDataValidator:

    def __init__(self):
        self.field_to_rules = {
            "byr": self.validate_four_digits(1920, 2002),  # (Birth Year)
            "iyr": self.validate_four_digits(2010, 2020),  # (Issue Year)
            "eyr": self.validate_four_digits(2020, 2030),  # (Expiration Year)
            "hgt": self.validate_number_followed_by({'cm': (150, 193), 'in': (59, 76)}),  # (Height)
            "hcl": self.validate_hair_colour,  # (Hair Color)
            "ecl": self.validate_eye_colour,  # (Eye Color)
            "pid": self.validate_passport_id,  # (Passport ID)
            "cid": lambda value: True,  # (Country ID)
        }

    def validate(self, field_name: str, field_value: str) -> bool:
        try:
            return self.field_to_rules[field_name](field_value)
        except KeyError:
            return False

    def match_regex(self, reg_str: str, value: str):
        try:
            return re.search(reg_str, value).groups()
        except AttributeError:
            return "something that will bever be matched!"

    def validate_four_digits(self, min_val: int, max_val: int) -> Callable[[str], bool]:
        def _validate(value: str) -> bool:
            matched_value = self.match_regex("^[0-9]{4}$", value)
            try:
                matched_value = re.search("^[0-9]{4}$", value).group()
            except AttributeError:
                return False
            return min_val <= int(matched_value) <= max_val

        return _validate

    @staticmethod
    def validate_number_followed_by(valid_values: Dict[str, Tuple[int, int]]) -> Callable[[str], bool]:
        def _validate(value: str) -> bool:
            try:
                number, matched_str = re.search("^([0-9]+)([a-z]+)$", value).groups()
            except AttributeError:
                return False
            if matched_str not in valid_values:
                return False
            min_val, max_val = valid_values[matched_str]
            return min_val <= int(number) <= max_val

        return _validate

    @staticmethod
    def validate_hair_colour(value: str) -> bool:
        try:
            matched = re.search("^#([0-9]|[a-f]){6}$", value).groups()
        except AttributeError:
            return False
        return True

    @staticmethod
    def validate_eye_colour(value: str) -> bool:
        return value in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

    @staticmethod
    def validate_passport_id(value: str) -> bool:
        if len(value) != 9:
            return False
        try:
            matched = re.search("^0*\d{9}$", value).group()
        except AttributeError:
            return False
        return True


class PassportProcessor:

    def __init__(self, batch_file_name: str, data_validator):
        with open(batch_file_name, "r") as f:
            raw_contents = f.read()[:-1]  # -1 to stripe trailing new line
        self.passports = [
            re.split(r' |\n', passport)
            for passport in raw_contents.split("\n\n")
        ]
        self.validator = data_validator()

    expected_fields = [
        "byr",  # (Birth Year)
        "iyr",  # (Issue Year)
        "eyr",  # (Expiration Year)
        "hgt",  # (Height)
        "hcl",  # (Hair Color)
        "ecl",  # (Eye Color)
        "pid",  # (Passport ID)
        "cid",  # (Country ID)
    ]

    ok_to_miss = [
        "cid",
    ]

    def is_valid(self, passport) -> bool:
        passport_fields = set()
        for field in passport:
            try:
                field_name, field_value = re.search("(.*):(.*)", field).groups()
            except IndexError:
                # field in wrong format!
                return False
            if field_name not in self.expected_fields:
                return False
            if not self.validator.validate(field_name, field_value):
                return False
            passport_fields.add(field_name)

        missing_fields = set(self.expected_fields) - passport_fields
        return not missing_fields or missing_fields == set(self.ok_to_miss)

    def process(self) -> int:
        valid_passports = 0
        for passport in self.passports:
            if self.is_valid(passport):
                valid_passports += 1
        return valid_passports


def part_1():
    processor = PassportProcessor("input.txt", BasicValidator)
    print(f"Part 1: no. of valid passports={processor.process()}")


def part_2():
    processor = PassportProcessor("input.txt", PassportDataValidator)
    print(f"Part 2: no. of valid passports={processor.process()}")


part_1()
part_2()

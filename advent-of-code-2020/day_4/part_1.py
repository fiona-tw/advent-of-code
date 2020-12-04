import re

class PassportProcessor:

    def __init__(self, batch_file_name: str):
        with open(batch_file_name, "r") as f:
            raw_contents = f.read()[:-1]  # -1 to stripe trailing new line
        self.passports = [
            re.split(' |\n', passport)
            for passport in raw_contents.split("\n\n")
        ]

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
                field_name = re.search("(.*):.*", field).group(1)
            except IndexError:
                # field in wrong format!
                return False
            if field_name not in self.expected_fields:
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


if __name__ == "__main__":
    example_processor = PassportProcessor("example_input.txt")
    # print(f"Valid example passports: {example_processor.process()}")
    
    processor = PassportProcessor("input.txt")
    print(f"Valid passports: {processor.process()}")

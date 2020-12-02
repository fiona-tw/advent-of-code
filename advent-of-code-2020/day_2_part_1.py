def decode_input(input_file):
    return[
            comb.split(": ") for comb in input_file.split("\n")[:-1]
    ]


class PasswordPolicy:
    def __init__(self, raw_policy: str):
        raw_policy.split("-")[1].split(" ")[0]
        self.min = int(raw_policy.split("-")[0]) 
        self.max = int(raw_policy.split("-")[1].split(" ")[0])
        self.required_char = raw_policy.split("-")[1].split(" ")[1]

    def is_valid(self, password: str) -> bool:
        char_count = password.count(self.required_char)
        return (self.min <= char_count <= self.max)

def analyse_passwords(input_file_name: str):
    with open(input_file_name, "r") as f:
        file_contents = decode_input(f.read())
    
    analysis = {
        True: [],  # To contain valid passwords
        False: [],  # To contain invalid passwords
    }

    for raw_policy, password in file_contents:
        password_is_valid = PasswordPolicy(raw_policy).is_valid(password)
        analysis[password_is_valid].append( (raw_policy, password) )

    return analysis


if __name__ == "__main__":
    file_name = "day_2_example_input.txt"
    file_name = "day_2_input.txt"
    results = analyse_passwords(file_name)
    print(f"Results: {results}")
    print()
    total_no_passwords = len(results[True]) + len(results[False])
    no_valid_passwords = len(results[True])
    print(f"No. of valid passwords: {no_valid_passwords}")
    print(f"Total no. of passwords: {total_no_passwords}")




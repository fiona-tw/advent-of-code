from typing import List


class AdaptorSequenceGetter:
    def __init__(self, filename: str) -> None:
        with open(f"day_10/{filename}", "r") as f:
            self.adaptors = sorted([
                int(x) for x in
                f.read().split("\n")[:-1]
            ])

        self.last_adaptor = max(self.adaptors)

        # build mapping of adaptor (including outlet!) to a list of valid next choices
        adaptor_to_next_valid_adaptors = {}
        for adaptor in [0] + self.adaptors:
            _choices = set.intersection(
                set(adaptor + x for x in range(1, 4)),
                self.adaptors
            )
            adaptor_to_next_valid_adaptors[adaptor] = list(_choices)
        self._valid_next_adaptors = adaptor_to_next_valid_adaptors

        # used to make counting more efficient, we will store the result for
        # each input to avoid duplicate recursion
        self._cached_count = {}

    def valid_next_adaptors(self, adaptor: int) -> List[int]:
        """Returns a list of valid next adaptors to choose after given adaptor"""
        return self._valid_next_adaptors[adaptor]

    def count_from(self, adaptor: int) -> int:
        cached_count = self._cached_count.get(adaptor)
        if cached_count:
            return cached_count

        _counter = 0
        consider_adaptor = adaptor

        while True:
            next_adaptor_choices = self.valid_next_adaptors(consider_adaptor)

            # if only 1 adaptor is valid next continue until either
            #   1. termination condition has been reached
            #      - increment counter
            #      - break out of while loop
            #      - return final count
            #   2. there is more than 1 valid choice for next adaptor
            #      - recurse through each valid choice
            #      - adding each result to counter
            #   3. we've finished 2. and have final count which is returned

            if len(next_adaptor_choices) == 1:
                # skip to next valid adaptor
                consider_adaptor = next_adaptor_choices[0]
                print("_", end="", flush=True)
                continue

            # 1. termination condition (we've reached device with valid adaptors)
            if consider_adaptor == self.last_adaptor:
                _counter += 1
                print(".", end="", flush=True)
                break

            # 2. more than one choice for next valid index -> count each branch
            for next_adaptor in next_adaptor_choices:
                _counter += self.count_from(next_adaptor)

            # 3. everything has been counted so break out of loop!
            break

        self._cached_count[adaptor] = _counter
        return _counter

    def part_1(self) -> None:
        # we get this for free simply but just sorting the list of adaptors
        # which has already been done for us in self.__init__!

        # prepending outlet joltage of 0
        # appending device joltage == 3 more than highest adaptor
        all_adaptors = [0] + self.adaptors + [max(self.adaptors) + 3]
        diffs = [
            all_adaptors[i + 1] - adaptor
            for i, adaptor in enumerate(all_adaptors[:-1])
        ]
        print(f"Count 1 == {diffs.count(1)}")
        print(f"Count 2 == {diffs.count(2)}")
        print(f"Count 3 == {diffs.count(3)}")

    def part_2(self, expected_count: int):
        # important to count from 0 as example 2 data shows that there is more
        # than 1 valid choice for the 1st adaptor (used directly from outlet)!
        final_count = self.count_from(0)
        print(
            f"\nfinal_count: {final_count}",
            end=f"!= {expected_count} as expected!" if final_count != expected_count else "\n"
        )


if __name__ == "__main__":
    for file, expected in [
        ("example_input.txt", 8),
        ("example_input_2.txt", 19208),
        ("input.txt", 338510590509056),
    ]:
        print(f"FILE: {file}")
        getter = AdaptorSequenceGetter(file)
        getter.part_1()
        getter.part_2(expected)

from typing import List, Dict


class IncompatibleAdaptorSeq(Exception):
    pass


class Adaptors:

    def __init__(self, filename: str):
        with open(f"day_10/{filename}", "r") as f:
            # does sorting this improve efficiency?
            self.adaptors = [int(x) for x in f.read().split("\n")[:-1]]

        self.target_joltage = sum(self.adaptors)
        self.adaptor_tolerance = 3
        # device joltage being max + 3 implicitly states the last adaptor must be highest! (as adaptors tolerance is 3)
        self.device_joltage = max(self.adaptors) + 3
        self.last_adaptor = max(self.adaptors)

    def is_compatible(self, a1, a2):
        return a2 - self.adaptor_tolerance <= a1 <= a2 - 1

    def get_ordered_adaptors(self, used_adaptors: List[int]) -> List[int]:
        # if we are down to the final adaptor - well we know this must be the max of all adaptors
        if len(used_adaptors) == len(self.adaptors) - 1:
            missing_adaptor = list(set(self.adaptors) - set(used_adaptors))[0]
            if missing_adaptor == self.last_adaptor:
                return used_adaptors + [self.last_adaptor]
            raise IncompatibleAdaptorSeq(f"Last adaptor must be __{self.last_adaptor}__ not __{missing_adaptor}__!")

        # consider all unused adaptors
        for this_adaptor in set(self.adaptors) - set(used_adaptors):
            # can only consider this adaptor if it is compatible with the previous one
            if used_adaptors and not self.is_compatible(used_adaptors[-1], this_adaptor):
                continue

            try:
                return self.get_ordered_adaptors(used_adaptors=used_adaptors + [this_adaptor])
            except IncompatibleAdaptorSeq:
                # i.e. a terminating sequence could not be found using this_adaptor (along with existing used_adaptors)
                continue

        raise IncompatibleAdaptorSeq(f"Given used adaptors are incompatible with device! {used_adaptors}")

    def get_joltage_differences(self):
        ordered_adaptors = self.get_ordered_adaptors([])
        all_adaptors = [0] + ordered_adaptors + [self.device_joltage]
        joltage_diffs = [all_adaptors[i + 1] - all_adaptors[i] for i in range(len(all_adaptors) - 1)]
        return {
            diff: joltage_diffs.count(diff)
            for diff in range(1, 4)
        }


def part_1():
    adaptors = Adaptors("example_input_2.txt")
    diffs = adaptors.get_joltage_differences()
    one_diff = diffs[1]
    three_diff = diffs[3]
    print(f"Result: {one_diff * three_diff}")


if __name__ == "__main__":
    part_1()

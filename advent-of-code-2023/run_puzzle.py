import sys

from logic import sum_of_calibration_values

if __name__ == "__main__":
    file_name = sys.argv[1]
    with open(sys.argv[1]) as file:
        raw_calibration_document = file.read()

    print(sum_of_calibration_values(raw_calibration_document))
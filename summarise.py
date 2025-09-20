import re
import sys
from collections import defaultdict
import argparse


def parse_options():
    parser = argparse.ArgumentParser(description="Summarise one of more log files. Normalises lines to remove numbers. Provides a count of each instance of a normalised line in reverse order.")
    parser.add_argument(
        "-f",
        "--files",
        dest="files_list",
        nargs="+",
        help="One or more files to summarise.",
    )
    args = parser.parse_args()
    if not args.files_list:
        sys.exit("Error: You need to supply a filename using the -f argument")
    return args


def normalise_line(line):
    normalised_line = line.strip()
    pattern = r"\d+"
    normalised_line = re.sub(pattern, ".", normalised_line)
    pattern = r"\[.\]"
    normalised_line = re.sub(pattern, "", normalised_line)
    pattern = r"\[.-.-. .:.:... \+.\]"
    normalised_line = re.sub(pattern, "", normalised_line)
    return normalised_line


line_count = 0
log_counts = defaultdict(int)


def process_a_file(filename):
    global line_count
    global log_counts
    with open(filename, "r") as fh:
        for line in fh:
            line_count += 1
            normalised_line = normalise_line(line)
            log_counts[normalised_line] += 1


def print_summary():
    global line_count
    global log_counts
    print(f"processed {line_count} lines")

    sorted_items = sorted(log_counts.items(), key=lambda item: item[1])
    for key, value in sorted_items:
        print(f"{value}: {key}")


#   for log_line in log_counts:
#       print(f"{log_counts[log_line]}    --> {log_line}")


if __name__ == "__main__":
    args = parse_options()

    processed_files = []
    error_files = []
    for file in args.files_list:
        try:
            process_a_file(file)
            processed_files.append(file)
        except (UnicodeDecodeError, IsADirectoryError):
            print("error with {file}")
            error_files.append(file)
    print_summary()
    print(f"summary of {processed_files} error files {error_files}")

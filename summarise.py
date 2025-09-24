#!/usr/bin/env python3

import re
import sys
from collections import defaultdict
import argparse


def parse_options():
    parser = argparse.ArgumentParser(
        description="Summarise one of more log files. Normalises lines to remove numbers. Provides a count of each instance of a normalised line in reverse order."
    )
    parser.add_argument(
        "-f",
        "--files",
        dest="files_list",
        nargs="+",
        help="One or more files to summarise.",
    )
    parser.add_argument(
        "-r",
        "--reverse-order",
        dest="reverse_order",
        action="store_true",
        help="List lines in reverse order",
    )
    parser.add_argument(
        "--do-not-normalise",
        dest="do_not_normalise",
        action="store_true",
        help="Do not normalise lines before summarising",
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


def process_a_file(filename, normalise_lines=True):
    global line_count
    global log_counts
    with open(filename, "r") as fh:
        for line in fh:
            line_count += 1
            if normalise_lines:
                normalised_line = normalise_line(line)
            else:
                normalised_line = line.strip()
            log_counts[normalised_line] += 1


def print_summary(reverse_order=False):
    global line_count
    global log_counts
    print(f"processed {line_count} lines")

    sorted_items = sorted(
        log_counts.items(), key=lambda item: item[1], reverse=reverse_order
    )
    for key, value in sorted_items:
        print(f"{value}: {key}")


#   for log_line in log_counts:
#       print(f"{log_counts[log_line]}    --> {log_line}")


if __name__ == "__main__":
    args = parse_options()
    if args.do_not_normalise:
        normalise = False
    else:
        normalise = True

    processed_files = []
    error_files = []
    for file in args.files_list:
        try:
            process_a_file(file, normalise)
            processed_files.append(file)
        except (UnicodeDecodeError, IsADirectoryError):
            print("error with {file}")
            error_files.append(file)
    print_summary(args.reverse_order)
    print(f"summary of {processed_files} error files {error_files}")

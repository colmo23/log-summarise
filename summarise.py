from optparse import OptionParser
import re
import sys
from collections import defaultdict


def parse_options():
    parser = OptionParser()
    parser.add_option(
        "-f",
        "--file",
        dest="filename",
        default=None,
        type="string",
        help="Log filename",
    )
    opt, args = parser.parse_args()
    if not opt.filename:
        sys.exit("Error: You need to supply a filename using the -f argument")
    return opt


def normalise_line(line):
    normalised_line = line.strip()
    pattern = r"\d+"
    normalised_line = re.sub(pattern, ".", normalised_line)
    pattern = r"\[.\]"
    normalised_line = re.sub(pattern, "", normalised_line)
    pattern = r"\[.-.-. .:.:... \+.\]"
    normalised_line = re.sub(pattern, "", normalised_line)
    return normalised_line


def process_a_file(filename):
    line_count = 0
    log_counts = defaultdict(int)
    with open(filename, "r") as fh:
        for line in fh:
            line_count += 1
            normalised_line = normalise_line(line)
            log_counts[normalised_line] += 1

    print(f"processed {line_count} lines")

    sorted_items = sorted(log_counts.items(), key=lambda item: item[1])
    for key, value in sorted_items:
        print(f"{value}: {key}")

#   for log_line in log_counts:
#       print(f"{log_counts[log_line]}    --> {log_line}")


if __name__ == "__main__":
    opt = parse_options()
    process_a_file(opt.filename)

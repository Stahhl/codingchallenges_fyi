#!/usr/bin/env python3
"""CLI entry point for uniq - filter adjacent duplicate lines."""

import argparse
import sys

from lib import uniq


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Filter adjacent matching lines from INPUT, writing to OUTPUT."
    )
    parser.add_argument(
        "-c", "--count",
        action="store_true",
        help="prefix lines by the number of occurrences"
    )
    parser.add_argument(
        "-d", "--repeated",
        action="store_true",
        help="only print duplicate lines, one for each group"
    )
    parser.add_argument(
        "-u", "--unique",
        action="store_true",
        help="only print unique lines"
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=argparse.FileType("rb"),
        default=sys.stdin,
        help="input file (default: stdin, use '-' for stdin)"
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output file (default: stdout)"
    )

    args = parser.parse_args()

    # Read input
    if args.input == sys.stdin:
        data = sys.stdin.buffer.read()
    else:
        data = args.input.read()
        args.input.close()

    content = data.decode("utf-8")

    # Process
    result = uniq(
        content,
        count=args.count,
        repeated=args.repeated,
        unique=args.unique,
    )

    # Write output
    args.output.write(result)
    if args.output != sys.stdout:
        args.output.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())

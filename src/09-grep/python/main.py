import argparse
import sys
import os
from lib import grep_content, grep_file, grep_recursive


parser = argparse.ArgumentParser(
    prog='ccgrep',
    description='Search for PATTERN in each FILE or standard input'
)

parser.add_argument('pattern', help='Pattern to search for')
parser.add_argument('files', nargs='*', help='Files or directories to search')
parser.add_argument('-r', '--recursive', action='store_true',
                    help='Recursively search directories')
parser.add_argument('-v', '--invert-match', action='store_true',
                    help='Select non-matching lines')
parser.add_argument('-i', '--ignore-case', action='store_true',
                    help='Ignore case distinctions')

args = parser.parse_args()

found_match = False
multiple_files = len(args.files) > 1 or args.recursive

# No files provided - read from stdin
if not args.files:
    content = sys.stdin.read()
    results = grep_content(content, args.pattern, args.invert_match, args.ignore_case)
    for line in results:
        print(line)
        found_match = True
else:
    for path in args.files:
        if args.recursive and os.path.isdir(path):
            for filepath, line in grep_recursive(path, args.pattern,
                                                  args.invert_match, args.ignore_case):
                print(f"{filepath}:{line}")
                found_match = True
        elif os.path.isfile(path):
            try:
                results = grep_file(path, args.pattern, args.invert_match,
                                    args.ignore_case)
                for filepath, line in results:
                    if multiple_files:
                        print(f"{filepath}:{line}")
                    else:
                        print(line)
                    found_match = True
            except (UnicodeDecodeError, PermissionError) as e:
                print(f"ccgrep: {path}: {e}", file=sys.stderr)
        elif os.path.isdir(path):
            if args.recursive:
                for filepath, line in grep_recursive(path, args.pattern,
                                                      args.invert_match, args.ignore_case):
                    print(f"{filepath}:{line}")
                    found_match = True
            else:
                print(f"ccgrep: {path}: Is a directory", file=sys.stderr)
        else:
            print(f"ccgrep: {path}: No such file or directory", file=sys.stderr)

sys.exit(0 if found_match else 1)

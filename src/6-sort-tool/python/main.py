# main.py
import sys, signal, argparse
from lib import sort_words

parser = argparse.ArgumentParser(description="Sort words from a file or stdin.")
parser.add_argument(
    "input_file",
    nargs="?",  # Makes the argument optional
    type=str,
    default=None,
    help="Path to the input file. If not provided, reads from stdin.",
)
parser.add_argument(
    "-u"
    "--unique",
    dest="unique",
    action="store_true",  # Stores True if flag is present, False otherwise
    help="Return only unique words.",
)
parser.add_argument(
    "-a",
    "--algorithm",
    dest="algorithm",
    type=str,
    default="timsort",  # Default to Python's built-in sort
    choices=["timsort", "radix", "merge", "quick", "heap", "random"],
    help="Sorting algorithm to use.",
)

args = parser.parse_args()

words = []
if args.input_file:
    try:
        with open(args.input_file, "r") as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found: {args.input_file}", file=sys.stderr)
        sys.exit(1)
else:
    # Read from stdin
    words = [line.strip() for line in sys.stdin if line.strip()]

sorted_result = sort_words(words, algorithm=args.algorithm, unique=args.unique)

# Ignore SIGPIPE signal to prevent BrokenPipeError on pipe closure
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

for word in sorted_result:
    print(word)
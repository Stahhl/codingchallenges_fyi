import argparse
import sys
from lib import *

parser = argparse.ArgumentParser()

parser.add_argument("-f", dest="field", help="field number", nargs="?")
parser.add_argument("-d", dest="delim", help="delimiter", nargs="?", required=False, default="\t")
# path to a file OR data from stdin
parser.add_argument('input', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, help="Input file (default: stdin)")

args = parser.parse_args()

fields = parse_fields(args.field)

data: bytes = sys.stdin.buffer.read() if args.input == sys.stdin else args.input.read()
content = data.decode("utf-8")

split = split_str(content, args.delim)

for row in zip(*split[fields[0]-1:fields[1]]):
    print(*row)
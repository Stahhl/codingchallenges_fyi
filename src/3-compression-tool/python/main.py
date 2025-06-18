import os, sys, argparse

parser = argparse.ArgumentParser()
# path to a file OR data from stdin
parser.add_argument('input', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, help="Input file (default: stdin)")

args = parser.parse_args()

data: bytes = sys.stdin.buffer.read() if args.input == sys.stdin else args.input.read()

input = True if len(data) > 0 else False

if(input == False):
    print("Received no data..!")
    exit(1)

print(f"Hello {len(data)}")
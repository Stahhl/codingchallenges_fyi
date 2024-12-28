import os, sys, argparse

# setup args
parser = argparse.ArgumentParser()
# path to a file OR data from stdin
parser.add_argument('input', nargs='?', type=argparse.FileType('rb'), default=sys.stdin, help="Input file (default: stdin)")
# optional
parser.add_argument("-c", action="store_true")
parser.add_argument("-l", action="store_true")
parser.add_argument("-w", action="store_true")
parser.add_argument("-m", action="store_true")

args = parser.parse_args()

data: bytes = sys.stdin.buffer.read() if args.input == sys.stdin else args.input.read()

input = True if len(data) > 0 else False

if(input == False):
    print("Received no data..!")
    exit(1)

def byte_count(data: bytes): 
    return len(data)

def row_count(data: bytes):
    return len(data.decode('utf-8').splitlines())

def word_count(data: bytes):
    return len(data.split())

def character_count(data: bytes):
    return len(data.decode('utf-8'))

outputArgs = []
if args.l:
    outputArgs.append(f"{row_count(data)}")
if args.w:
    outputArgs.append(f"{word_count(data)}")
if args.c:
    outputArgs.append(f"{byte_count(data)}")
if args.m:
    outputArgs.append(f"{character_count(data)}")
if not (args.c or args.l or args.w or args.m):
    outputArgs.append(f"{row_count(data)} {word_count(data)} {byte_count(data)}")

output = " ".join(outputArgs)
file_path = "" if args.input == sys.stdin else args.input.name

print(f"{output} {file_path}")
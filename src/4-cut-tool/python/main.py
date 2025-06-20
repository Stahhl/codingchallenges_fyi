import argparse
from lib import *

parser = argparse.ArgumentParser()

parser.add_argument("-f", dest="field", help="field number", nargs="?")
parser.add_argument("input_file", help="Path of the input file")

args = parser.parse_args()

print(args.field)
print(args.input_file)

content = read_file(args.input_file).decode("utf-8")
print(content)

split = split_str(content)

print(split[int(args.field)])
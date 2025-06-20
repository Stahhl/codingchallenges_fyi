import argparse
from lib import *

parser = argparse.ArgumentParser()

parser.add_argument("-f", dest="field", help="field number", nargs="?")
parser.add_argument("-d", dest="delim", help="delimiter", nargs="?", required=False, default="\t")
parser.add_argument("input_file", help="Path of the input file")

args = parser.parse_args()

content = read_file(args.input_file).decode("utf-8")

split = split_str(content, args.delim)

print(split[int(args.field)])
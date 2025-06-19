import argparse, sys
from lib import *

parser = argparse.ArgumentParser(description="Compress or decompress a file.")

parser.add_argument("input_file", help="Path of the input file")
parser.add_argument(
    "output_file", help="Path of the output file")

parser.add_argument(
    "-m", "--mode",
    choices=["c", "compress", "d", "decompress"],
    required=True,
    help="Operation mode: c/compress or d/decompress"
)

args = parser.parse_args()

print(args.input_file)
print(args.output_file)
print(args.mode)

input = read_file(args.input_file)

if args.mode[0] == "c":
    """compress"""
    s = input.decode("utf-8")
    freqs = char_frequencies(s)
    root = build_huffman_tree(freqs)
    codes = build_code_table(root)
    compressed = build_huffman_package(codes, s)
    write_file(compressed, args.output_file)
elif args.mode[0] == "d":
    """decompress"""
    decompressed = decode_huffman_package(input)
    write_file(decompressed, args.output_file)
import os
from lib import * 

def test_bar():
    input = "Hello World!"
    freqs = char_frequencies(input)
    # for k, v in freqs.items():
    #     print(f"{k}: {v}")

    root = build_huffman_tree(freqs)

    codes = build_code_table(root)
    # print(codes)
    compressed = build_huffman_package(codes, input)
    decompressed = decode_huffman_package(compressed)

    assert freqs["H"] == 1
    assert freqs["o"] == 2
    assert decompressed.decode("utf-8") == input


def test_4real():
    base_path = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_path, "test.txt")
    compressed_path = os.path.join(base_path, "compressed")
    decompressed_path = os.path.join(base_path, "decompressed.txt")

    if os.path.exists(compressed_path):
        os.remove(compressed_path)

    if os.path.exists(decompressed_path):
        os.remove(decompressed_path)

    input_txt_str = read_file(input_path).decode("utf-8")
    freqs = char_frequencies(input_txt_str)
    root = build_huffman_tree(freqs)
    codes = build_code_table(root)

    compressed = build_huffman_package(codes, input_txt_str)
    write_file(compressed, compressed_path)

    input_compressed_bytes = read_file(compressed_path)
    decompressed = decode_huffman_package(input_compressed_bytes)
    write_file(decompressed, decompressed_path)

    assert decompressed.decode("utf-8") == input_txt_str

import os
from lib import *

def test_split():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test-data", "sample.tsv")
    content = read_file(path).decode("utf-8")
    split = split_str(content)
    print(split[1])
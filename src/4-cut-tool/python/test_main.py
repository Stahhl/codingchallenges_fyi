import os
from lib import *

def test_split():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test-data", "sample.tsv")
    content = read_file(path).decode("utf-8")
    split = split_str(content)

    assert split[1] == ["f1", "1", "6", "11", "16", "21"]

def test_parse_field_a():
    input="7"
    result = parse_fields(input)

    assert result[0] == 0
    assert result[1] == 7

def test_parse_field_b():
    input="1,7"
    result = parse_fields(input)

    assert result[0] == 1
    assert result[1] == 7

def test_parse_field_c():
    input="1 7"
    result = parse_fields(input)

    assert result[0] == 1
    assert result[1] == 7
import os
import subprocess
from lib import *

def test_split():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test-data", "sample.tsv")
    content = read_file(path).decode("utf-8")
    split = split_str(content)

    assert split[1] == ["f1", "1", "6", "11", "16", "21"]

def test_parse_field_a():
    input="7"
    result = parse_fields(input)
    print(result)

    assert result[0] == 7
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

def test_step1():
    result = subprocess.run(
        ["python3", "main.py", "-f2", "../test-data/sample.tsv"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "f1\n1\n6\n11\n16\n21"

def test_step5():
    p1 = subprocess.Popen(
        ["python3", "main.py", "-f2", "-d,", "../test-data/fourchords.csv"],
        stdout=subprocess.PIPE
    )

    # Pipe to uniq
    p2 = subprocess.Popen(
        ["uniq"],
        stdin=p1.stdout,
        stdout=subprocess.PIPE
    )

    # Pipe to wc
    p3 = subprocess.Popen(
        ["wc", "-l"],
        stdin=p2.stdout,
        stdout=subprocess.PIPE,
        text=True
    )

    # Get final output
    out, err = p3.communicate()

    assert err == None
    assert out.strip() == "155"
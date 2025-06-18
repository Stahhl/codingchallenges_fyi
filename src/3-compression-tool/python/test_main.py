import os, subprocess
from lib import char_count

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_file() -> str:
    with open("test.txt") as f:
        return f.read()

def test_bar():
    result = char_count(read_file())
    for k, v in result.items():
        print(f"{k}: {v}")

    assert result["X"] == 333
    assert result["t"] == 223000
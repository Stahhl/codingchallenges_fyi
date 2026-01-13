import os
import subprocess

from lib import convert_pattern, match_line, grep_content, grep_file


TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test-data")
ROCKBANDS = os.path.join(TEST_DATA_DIR, "rockbands.txt")
SYMBOLS = os.path.join(TEST_DATA_DIR, "symbols.txt")
TEST_TXT = os.path.join(TEST_DATA_DIR, "test.txt")
BFS1985 = os.path.join(TEST_DATA_DIR, "test-subdir", "BFS1985.txt")


def run_grep(*args) -> subprocess.CompletedProcess:
    """Helper to run main.py with given arguments."""
    return subprocess.run(
        ["python3", "main.py", *args],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )


# Unit tests for lib.py

def test_convert_pattern_digit():
    assert convert_pattern("\\d") == "[0-9]"


def test_convert_pattern_word():
    assert convert_pattern("\\w") == "[a-zA-Z0-9_]"


def test_convert_pattern_anchors():
    assert convert_pattern("^A") == "^A"
    assert convert_pattern("na$") == "na$"


def test_match_line_simple():
    assert match_line("Hello World", "World") is True
    assert match_line("Hello World", "Foo") is False


def test_match_line_ignore_case():
    assert match_line("Hello World", "world", ignore_case=False) is False
    assert match_line("Hello World", "world", ignore_case=True) is True


def test_match_line_anchors():
    assert match_line("Apple", "^A") is True
    assert match_line("Banana", "^A") is False
    assert match_line("Nirvana", "na$") is True
    assert match_line("Nirvana!", "na$") is False


def test_grep_content_empty_pattern():
    content = "line1\nline2\nline3"
    results = grep_content(content, "")
    assert results == ["line1", "line2", "line3"]


def test_grep_content_simple():
    content = "Judas Priest\nBon Jovi\nJunkyard\nAC/DC"
    results = grep_content(content, "J")
    assert results == ["Judas Priest", "Bon Jovi", "Junkyard"]


def test_grep_content_invert():
    content = "Judas Priest\nBon Jovi\nJunkyard\nAC/DC"
    results = grep_content(content, "J", invert=True)
    assert results == ["AC/DC"]


# Integration tests using subprocess

def test_step1_empty_pattern():
    """Step 1: Empty expression matches every line."""
    result = run_grep("", TEST_TXT)
    with open(TEST_TXT, 'r') as f:
        expected_lines = len(f.read().splitlines())
    actual_lines = len(result.stdout.splitlines())
    assert actual_lines == expected_lines
    assert result.returncode == 0


def test_step2_single_char():
    """Step 2: Single character pattern."""
    result = run_grep("J", ROCKBANDS)
    lines = result.stdout.strip().split("\n")
    assert "Judas Priest" in lines
    assert "Bon Jovi" in lines
    assert "Junkyard" in lines
    assert result.returncode == 0


def test_step2_exit_code_match():
    """Step 2: Exit code 0 when pattern matches."""
    result = run_grep("J", ROCKBANDS)
    assert result.returncode == 0


def test_step2_exit_code_no_match():
    """Step 2: Exit code 1 when pattern doesn't match."""
    result = run_grep("ZZZZNOTFOUND", ROCKBANDS)
    assert result.returncode == 1


def test_step3_recursive():
    """Step 3: Recursive directory search."""
    result = run_grep("-r", "Nirvana", TEST_DATA_DIR)
    assert result.returncode == 0
    lines = result.stdout.strip().split("\n")
    # Should find in rockbands.txt and BFS1985.txt
    assert any("rockbands.txt:Nirvana" in line for line in lines)
    assert any("BFS1985.txt" in line and "Nirvana" in line for line in lines)


def test_step4_invert():
    """Step 4: Inverted matching."""
    result = run_grep("-v", "J", ROCKBANDS)
    lines = result.stdout.strip().split("\n")
    # Lines with J should NOT be in results
    assert "Judas Priest" not in lines
    assert "Bon Jovi" not in lines
    assert "Junkyard" not in lines
    # Lines without J should be there
    assert "AC/DC" in lines
    assert result.returncode == 0


def test_step5_digit():
    """Step 5: \\d matches digits."""
    result = run_grep("\\d", BFS1985)
    lines = result.stdout.strip().split("\n")
    # Lines with numbers should match
    assert any("24" in line for line in lines)
    assert any("1985" in line for line in lines)
    assert result.returncode == 0


def test_step5_word():
    """Step 5: \\w matches word characters."""
    result = run_grep("\\w", SYMBOLS)
    lines = result.stdout.strip().split("\n")
    # Only "pound" and "dollar" have word characters
    assert "pound" in lines
    assert "dollar" in lines
    # Symbol-only lines should not match
    assert "!" not in lines
    assert "@" not in lines


def test_step6_anchor_start():
    """Step 6: ^ matches start of line."""
    result = run_grep("^A", ROCKBANDS)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        assert line.startswith("A")


def test_step6_anchor_end():
    """Step 6: $ matches end of line."""
    result = run_grep("na$", ROCKBANDS)
    lines = result.stdout.strip().split("\n")
    for line in lines:
        assert line.endswith("na")


def test_step7_case_insensitive():
    """Step 7: -i flag for case-insensitive matching."""
    result_case = run_grep("A", ROCKBANDS)
    result_nocase = run_grep("-i", "A", ROCKBANDS)

    case_count = len(result_case.stdout.strip().split("\n"))
    nocase_count = len(result_nocase.stdout.strip().split("\n"))

    # Case-insensitive should match more lines
    assert nocase_count > case_count


def test_stdin():
    """Test reading from stdin."""
    result = subprocess.run(
        ["python3", "main.py", "J"],
        input="Judas Priest\nAC/DC\nBon Jovi",
        capture_output=True,
        text=True,
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    lines = result.stdout.strip().split("\n")
    assert "Judas Priest" in lines
    assert "Bon Jovi" in lines
    assert "AC/DC" not in lines

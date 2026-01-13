"""Tests for uniq implementation."""

import os
import subprocess
import sys

from lib import LineCount, count_adjacent_lines, uniq

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test-data")
MAIN_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")


class TestCountAdjacentLines:
    def test_empty_input(self):
        assert count_adjacent_lines([]) == []

    def test_single_line(self):
        result = count_adjacent_lines(["hello"])
        assert result == [LineCount("hello", 1)]

    def test_no_duplicates(self):
        result = count_adjacent_lines(["a", "b", "c"])
        assert result == [
            LineCount("a", 1),
            LineCount("b", 1),
            LineCount("c", 1),
        ]

    def test_adjacent_duplicates(self):
        result = count_adjacent_lines(["a", "b", "b", "c"])
        assert result == [
            LineCount("a", 1),
            LineCount("b", 2),
            LineCount("c", 1),
        ]

    def test_multiple_adjacent_duplicates(self):
        result = count_adjacent_lines(["a", "a", "a", "b", "b"])
        assert result == [
            LineCount("a", 3),
            LineCount("b", 2),
        ]

    def test_non_adjacent_duplicates_not_merged(self):
        result = count_adjacent_lines(["a", "b", "a"])
        assert result == [
            LineCount("a", 1),
            LineCount("b", 1),
            LineCount("a", 1),
        ]


class TestUniq:
    def test_empty_input(self):
        assert uniq("") == ""

    def test_basic_dedup(self):
        content = "line1\nline2\nline2\nline3\nline4\n"
        result = uniq(content)
        assert result == "line1\nline2\nline3\nline4\n"

    def test_no_duplicates(self):
        content = "a\nb\nc\n"
        result = uniq(content)
        assert result == "a\nb\nc\n"

    def test_count_flag(self):
        content = "line1\nline2\nline2\nline3\n"
        result = uniq(content, count=True)
        assert result == "   1 line1\n   2 line2\n   1 line3\n"

    def test_repeated_flag(self):
        content = "line1\nline2\nline2\nline3\nline4\n"
        result = uniq(content, repeated=True)
        assert result == "line2\n"

    def test_unique_flag(self):
        content = "line1\nline2\nline2\nline3\nline4\n"
        result = uniq(content, unique=True)
        assert result == "line1\nline3\nline4\n"

    def test_count_and_repeated(self):
        content = "line1\nline2\nline2\nline3\n"
        result = uniq(content, count=True, repeated=True)
        assert result == "   2 line2\n"

    def test_count_and_unique(self):
        content = "line1\nline2\nline2\nline3\n"
        result = uniq(content, count=True, unique=True)
        assert result == "   1 line1\n   1 line3\n"


class TestIntegration:
    def run_uniq(self, *args: str, input_data: str | None = None) -> tuple[str, int]:
        """Run main.py with arguments and return (stdout, returncode)."""
        cmd = [sys.executable, MAIN_PY, *args]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            input=input_data,
        )
        return result.stdout, result.returncode

    def test_basic_file(self):
        test_file = os.path.join(TEST_DATA_DIR, "test.txt")
        stdout, code = self.run_uniq(test_file)
        assert code == 0
        assert stdout == "line1\nline2\nline3\nline4\n"

    def test_stdin(self):
        stdout, code = self.run_uniq(input_data="a\na\nb\n")
        assert code == 0
        assert stdout == "a\nb\n"

    def test_count_flag_cli(self):
        test_file = os.path.join(TEST_DATA_DIR, "test.txt")
        stdout, code = self.run_uniq("-c", test_file)
        assert code == 0
        assert "   1 line1" in stdout
        assert "   2 line2" in stdout

    def test_repeated_flag_cli(self):
        test_file = os.path.join(TEST_DATA_DIR, "test.txt")
        stdout, code = self.run_uniq("-d", test_file)
        assert code == 0
        assert stdout == "line2\n"

    def test_unique_flag_cli(self):
        test_file = os.path.join(TEST_DATA_DIR, "test.txt")
        stdout, code = self.run_uniq("-u", test_file)
        assert code == 0
        assert "line1" in stdout
        assert "line2" not in stdout
        assert "line3" in stdout

    def test_countries_file(self):
        test_file = os.path.join(TEST_DATA_DIR, "countries.txt")
        stdout, code = self.run_uniq("-d", test_file)
        assert code == 0
        # Brazil, Italy, Turkey are duplicated
        assert "Brazil" in stdout
        assert "Italy" in stdout
        assert "Turkey" in stdout

    def test_countries_count(self):
        test_file = os.path.join(TEST_DATA_DIR, "countries.txt")
        stdout, code = self.run_uniq("-c", "-d", test_file)
        assert code == 0
        assert "   2 Brazil" in stdout
        assert "   2 Italy" in stdout
        assert "   2 Turkey" in stdout

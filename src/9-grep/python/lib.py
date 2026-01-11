import re
import os
from typing import Generator


def convert_pattern(pattern: str) -> str:
    """Convert grep-style pattern to Python regex pattern.

    Supports:
    - \\d -> [0-9] (digit)
    - \\w -> [a-zA-Z0-9_] (word character)
    - ^ and $ anchors
    """
    # Replace grep-style character classes with regex equivalents
    result = pattern.replace("\\d", "[0-9]")
    result = result.replace("\\w", "[a-zA-Z0-9_]")
    return result


def match_line(line: str, pattern: str, ignore_case: bool = False) -> bool:
    """Check if a line matches the given pattern."""
    regex_pattern = convert_pattern(pattern)
    flags = re.IGNORECASE if ignore_case else 0
    return re.search(regex_pattern, line, flags) is not None


def grep_content(content: str, pattern: str, invert: bool = False,
                 ignore_case: bool = False) -> list[str]:
    """Search content for lines matching pattern.

    Args:
        content: Text content to search
        pattern: Pattern to match
        invert: If True, return non-matching lines (-v flag)
        ignore_case: If True, ignore case (-i flag)

    Returns:
        List of matching (or non-matching if invert) lines
    """
    lines = content.splitlines()
    results = []

    for line in lines:
        matches = match_line(line, pattern, ignore_case)
        if invert:
            if not matches:
                results.append(line)
        else:
            if matches:
                results.append(line)

    return results


def grep_file(filepath: str, pattern: str, invert: bool = False,
              ignore_case: bool = False) -> list[tuple[str, str]]:
    """Search a file for lines matching pattern.

    Returns:
        List of (filepath, line) tuples for matching lines
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    matches = grep_content(content, pattern, invert, ignore_case)
    return [(filepath, line) for line in matches]


def grep_recursive(directory: str, pattern: str, invert: bool = False,
                   ignore_case: bool = False) -> Generator[tuple[str, str], None, None]:
    """Recursively search directory for lines matching pattern.

    Yields:
        (filepath, line) tuples for each matching line
    """
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            # Skip hidden files
            if filename.startswith('.'):
                continue

            filepath = os.path.join(root, filename)
            try:
                results = grep_file(filepath, pattern, invert, ignore_case)
                for result in results:
                    yield result
            except (UnicodeDecodeError, PermissionError, IsADirectoryError):
                # Skip binary files and files we can't read
                continue

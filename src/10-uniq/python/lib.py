"""Business logic for uniq - filter adjacent duplicate lines."""

from dataclasses import dataclass


@dataclass
class LineCount:
    """A line with its occurrence count."""
    line: str
    count: int


def count_adjacent_lines(lines: list[str]) -> list[LineCount]:
    """
    Count consecutive occurrences of each line.

    Returns a list of LineCount objects with each unique line and its count.
    """
    if not lines:
        return []

    result: list[LineCount] = []
    current_line = lines[0]
    current_count = 1

    for line in lines[1:]:
        if line == current_line:
            current_count += 1
        else:
            result.append(LineCount(current_line, current_count))
            current_line = line
            current_count = 1

    result.append(LineCount(current_line, current_count))
    return result


def uniq(
    content: str,
    count: bool = False,
    repeated: bool = False,
    unique: bool = False,
) -> str:
    """
    Filter adjacent duplicate lines from content.

    Args:
        content: Input text content
        count: If True, prepend each line with occurrence count
        repeated: If True, only output lines that appear more than once
        unique: If True, only output lines that appear exactly once

    Returns:
        Filtered output as a string
    """
    lines = content.splitlines()
    counted = count_adjacent_lines(lines)

    # Filter based on flags
    if repeated:
        counted = [lc for lc in counted if lc.count > 1]
    elif unique:
        counted = [lc for lc in counted if lc.count == 1]

    # Format output
    output_lines: list[str] = []
    for lc in counted:
        if count:
            output_lines.append(f"{lc.count:>4} {lc.line}")
        else:
            output_lines.append(lc.line)

    if output_lines:
        return "\n".join(output_lines) + "\n"
    return ""

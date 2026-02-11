"""Shared SLOC counting utility for pre-commit hooks."""


def count_sloc(source_lines: list[str], start_line: int, end_line: int) -> int:
    """Count non-blank, non-comment lines in a 1-based inclusive range."""
    count = 0
    for line in source_lines[start_line - 1 : end_line]:
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            count += 1
    return count

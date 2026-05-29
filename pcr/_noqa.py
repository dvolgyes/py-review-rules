"""Shared noqa handling for check exemptions."""

import re

from pcr.comment_by_line import comment_by_line

NOQA_RE = re.compile(
    r"#\s*(?:pcr\s*:\s*)?noqa\b(?:\s*:\s*(?P<codes>.*))?",
    re.IGNORECASE,
)


def line_has_noqa(source_lines: list[str], line_number: int, code: str | None) -> bool:
    """Return whether a 1-based line has a matching noqa marker."""
    for comment in comment_by_line(source_lines).get(line_number, []):
        match = NOQA_RE.search(comment)
        if match is None:
            continue
        if code is None:
            return True
        codes = match.group("codes")
        if codes is None or not codes.strip():
            return True
        if code in {item.strip() for item in codes.split(",")}:
            return True
    return False

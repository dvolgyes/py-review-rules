"""Placeholder comment rule."""

from pcr._noqa import line_has_noqa
from pcr.codes import PLACEHOLDER_COMMENT_CODE
from pcr.comment_by_line import comment_by_line
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation

PLACEHOLDER_MARKERS = frozenset({"todo", "fixme", "xxx", "hack", "placeholder"})


def check_placeholder_comments(
    filepath: str, lines: list[str], config: Config
) -> list[Violation]:
    """Check placeholder comments."""
    if not config.style.ban_placeholder_comment:
        return []
    if module_has_noqa(lines, PLACEHOLDER_COMMENT_CODE):
        return []
    return [
        Violation(filepath, line_number, PLACEHOLDER_COMMENT_CODE, "placeholder")
        for line_number, comments in comment_by_line(lines).items()
        for comment in comments
        if any(marker in comment.lower() for marker in PLACEHOLDER_MARKERS)
        and not line_has_noqa(lines, line_number, PLACEHOLDER_COMMENT_CODE)
    ]

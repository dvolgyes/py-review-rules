"""Placeholder comment rule."""

from prr._noqa import line_has_noqa
from prr.codes import PLACEHOLDER_COMMENT_CODE
from prr.comment_by_line import comment_by_line
from prr.config import Config
from prr.module_noqa import module_has_noqa
from prr.violation import Violation

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
        Violation(
            filepath,
            line_number,
            PLACEHOLDER_COMMENT_CODE,
            "placeholder comment is banned",
        )
        for line_number, comments in comment_by_line(lines).items()
        for comment in comments
        if any(marker in comment.lower() for marker in PLACEHOLDER_MARKERS)
        and not line_has_noqa(lines, line_number, PLACEHOLDER_COMMENT_CODE)
    ]

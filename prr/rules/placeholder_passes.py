"""Placeholder pass rule."""

import ast

from prr._noqa import line_has_noqa
from prr.codes import PLACEHOLDER_BODY_CODE
from prr.config import Config
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


def check_placeholder_passes(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check placeholder pass statements."""
    if not config.style.ban_placeholder_pass:
        return []
    if module_has_noqa(lines, PLACEHOLDER_BODY_CODE):
        return []
    return [
        Violation(
            filepath,
            node.lineno,
            PLACEHOLDER_BODY_CODE,
            "pass placeholder is banned",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.Pass)
        and not line_has_noqa(lines, node.lineno, PLACEHOLDER_BODY_CODE)
    ]

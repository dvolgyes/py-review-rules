"""Placeholder pass rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.codes import PLACEHOLDER_BODY_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_placeholder_passes(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check placeholder pass statements."""
    if not config.style.ban_placeholder_pass:
        return []
    if module_has_noqa(lines, PLACEHOLDER_BODY_CODE):
        return []
    return [
        Violation(filepath, node.lineno, PLACEHOLDER_BODY_CODE, "pass placeholder")
        for node in ast.walk(tree)
        if isinstance(node, ast.Pass)
        and not line_has_noqa(lines, node.lineno, PLACEHOLDER_BODY_CODE)
    ]

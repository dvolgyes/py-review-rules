"""Elif count rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.codes import ELIF_CODE
from pcr.config import Config
from pcr.elif_count import elif_count
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_elifs(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check maximum elif count per if chain."""
    limit = config.control_flow.max_elifs
    if limit is None or module_has_noqa(lines, ELIF_CODE):
        return []
    return [
        Violation(
            filepath, node.lineno, ELIF_CODE, f"too many elifs: {elif_count(node)}"
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.If)
        and elif_count(node) > limit
        and not line_has_noqa(lines, node.lineno, ELIF_CODE)
    ]

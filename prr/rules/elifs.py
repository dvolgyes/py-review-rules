"""Elif count rule."""

import ast

from prr._noqa import line_has_noqa
from prr.codes import ELIF_CODE
from prr.config import Config
from prr.elif_count import elif_count
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


def check_elifs(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check maximum elif count per if chain."""
    limit = config.control_flow.max_elifs
    if limit is None or module_has_noqa(lines, ELIF_CODE):
        return []
    return [
        Violation(
            filepath,
            node.lineno,
            ELIF_CODE,
            f"if chain has too many elifs: {elif_count(node)} (max {limit})",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.If)
        and elif_count(node) > limit
        and not line_has_noqa(lines, node.lineno, ELIF_CODE)
    ]

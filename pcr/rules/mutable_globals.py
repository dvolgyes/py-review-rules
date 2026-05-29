"""Mutable global rules."""

import ast

from pcr._noqa import line_has_noqa
from pcr.codes import MUTABLE_GLOBAL_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.mutable_value import is_mutable_value
from pcr.violation import Violation


def check_mutable_globals(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check module-level mutable values."""
    if not config.style.ban_mutable_global or module_has_noqa(
        lines, MUTABLE_GLOBAL_CODE
    ):
        return []
    return [
        Violation(filepath, node.lineno, MUTABLE_GLOBAL_CODE, "mutable global")
        for node in tree.body
        if isinstance(node, ast.Assign | ast.AnnAssign)
        and node.value is not None
        and is_mutable_value(node.value)
        and not line_has_noqa(lines, node.lineno, MUTABLE_GLOBAL_CODE)
    ]

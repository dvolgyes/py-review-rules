"""Mutable global rules."""

import ast
from pathlib import Path

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
        Violation(
            filepath,
            node.lineno,
            MUTABLE_GLOBAL_CODE,
            f"mutable global variable ({_assignment_targets(node)})",
        )
        for node in tree.body
        if isinstance(node, ast.Assign | ast.AnnAssign)
        and node.value is not None
        and is_mutable_value(node.value)
        and not _is_init_all_assignment(filepath, node)
        and not line_has_noqa(lines, node.lineno, MUTABLE_GLOBAL_CODE)
    ]


def _assignment_targets(node: ast.Assign | ast.AnnAssign) -> str:
    targets: list[ast.expr] = (
        [node.target] if isinstance(node, ast.AnnAssign) else node.targets
    )
    return ", ".join(
        target.id if isinstance(target, ast.Name) else ast.unparse(target)
        for target in targets
    )


def _is_init_all_assignment(filepath: str, node: ast.Assign | ast.AnnAssign) -> bool:
    if Path(filepath).name != "__init__.py":
        return False
    if isinstance(node, ast.AnnAssign):
        return isinstance(node.target, ast.Name) and node.target.id == "__all__"
    return any(
        isinstance(target, ast.Name) and target.id == "__all__"
        for target in node.targets
    )

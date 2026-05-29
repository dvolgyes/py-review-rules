"""Future annotations import rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.codes import FUTURE_IMPORT_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_future_imports(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check ``from __future__ import annotations`` is absent."""
    if not config.imports.ban_future_import or module_has_noqa(
        lines, FUTURE_IMPORT_CODE
    ):
        return []
    return [
        Violation(filepath, node.lineno, FUTURE_IMPORT_CODE, "future import is banned")
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module == "__future__"
        and any(alias.name == "annotations" for alias in node.names)
        and not line_has_noqa(lines, node.lineno, FUTURE_IMPORT_CODE)
    ]

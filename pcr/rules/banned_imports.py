"""Banned import rule."""

import ast

from pcr.codes import BANNED_IMPORT_CODE
from pcr.config import Config
from pcr.imported_names import imported_names
from pcr.module_noqa import module_has_noqa
from pcr.parse_banned_import import parse_banned_import
from pcr.violation import Violation


def check_banned_imports(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check configured banned import packages."""
    bans = [parse_banned_import(spec) for spec in config.imports.banned_imports]
    if not bans or module_has_noqa(lines, BANNED_IMPORT_CODE):
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import | ast.ImportFrom):
            imported = imported_names(node)
            violations.extend(
                Violation(filepath, node.lineno, BANNED_IMPORT_CODE, ban)
                for ban, _alternative in bans
                if any(name == ban or name.startswith(f"{ban}.") for name in imported)
            )
    return violations

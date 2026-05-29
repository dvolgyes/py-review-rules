"""Top-level import placement rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.codes import TOP_LEVEL_IMPORT_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_top_level_imports(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check imports appear directly at module top level."""
    if not config.imports.require_top_level_import:
        return []
    if module_has_noqa(lines, TOP_LEVEL_IMPORT_CODE):
        return []
    return [
        Violation(
            filepath, node.lineno, TOP_LEVEL_IMPORT_CODE, "import is not top level"
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.Import | ast.ImportFrom)
        and parents.get(node) is not tree
        and not line_has_noqa(lines, node.lineno, TOP_LEVEL_IMPORT_CODE)
    ]

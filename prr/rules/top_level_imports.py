"""Top-level import placement rule."""

import ast

from prr._noqa import line_has_noqa
from prr.codes import TOP_LEVEL_IMPORT_CODE
from prr.config import Config
from prr.imported_names import imported_names
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


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
            filepath,
            node.lineno,
            TOP_LEVEL_IMPORT_CODE,
            f"import is not top level ({', '.join(imported_names(node))})",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.Import | ast.ImportFrom)
        and parents.get(node) is not tree
        and not line_has_noqa(lines, node.lineno, TOP_LEVEL_IMPORT_CODE)
    ]

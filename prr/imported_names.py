"""Imported name extraction."""

import ast


def imported_names(node: ast.Import | ast.ImportFrom) -> list[str]:
    """Return fully qualified names introduced by an import node."""
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    module = node.module or ""
    return [f"{module}.{alias.name}" if module else alias.name for alias in node.names]

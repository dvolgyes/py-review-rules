"""AST parent mapping."""

import ast


def parents(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    """Return a child-to-parent map for an AST."""
    result: dict[ast.AST, ast.AST] = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            result[child] = parent
    return result

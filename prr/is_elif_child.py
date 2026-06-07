"""Elif child detection."""

import ast


def is_elif_child(parent: ast.AST, child: ast.If) -> bool:
    """Return whether ``child`` is the elif node of ``parent``."""
    return (
        isinstance(parent, ast.If)
        and len(parent.orelse) == 1
        and parent.orelse[0] is child
    )

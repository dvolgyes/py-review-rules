"""Class member detection."""

import ast


def is_class_member(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> bool:
    """Return whether a node is directly inside a class body."""
    return isinstance(parents.get(node), ast.ClassDef)

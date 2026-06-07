"""Dotted expression reconstruction."""

import ast


def dotted_name(node: ast.expr) -> str | None:
    """Reconstruct a dotted expression name."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        return f"{parent}.{node.attr}" if parent is not None else None
    return None

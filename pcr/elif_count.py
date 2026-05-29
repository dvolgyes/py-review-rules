"""Elif chain counting."""

import ast


def elif_count(node: ast.If) -> int:
    """Return the number of elif branches attached to an if node."""
    count = 0
    current = node
    while len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
        count += 1
        current = current.orelse[0]
    return count

"""Self assignment classification."""

import ast


def is_unannotated_self_assignment(node: ast.AST, members: set[str]) -> bool:
    """Return whether an AST node stores an undeclared ``self`` attribute."""
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.ctx, ast.Store)
        and isinstance(node.value, ast.Name)
        and node.value.id == "self"
        and node.attr not in members
    )

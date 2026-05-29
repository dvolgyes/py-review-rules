"""Typing alias classification."""

import ast

BANNED_TYPING_ALIASES = frozenset({"Dict", "List", "Optional", "Union"})


def uses_banned_typing_alias(node: ast.AST, typing_names: set[str]) -> bool:
    """Return whether a node imports or references a banned typing alias."""
    if isinstance(node, ast.ImportFrom) and node.module == "typing":
        return any(
            alias.name == "*" or alias.name in BANNED_TYPING_ALIASES
            for alias in node.names
        )
    return (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id in typing_names
        and node.attr in BANNED_TYPING_ALIASES
    )

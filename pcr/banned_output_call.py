"""Banned output call classification."""

import ast


def is_banned_output_call(
    node: ast.Call, click_names: set[str], echo_names: set[str]
) -> bool:
    """Return whether a call is print or click.echo."""
    if isinstance(node.func, ast.Name):
        return node.func.id == "print" or node.func.id in echo_names
    return (
        isinstance(node.func, ast.Attribute)
        and node.func.attr == "echo"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id in click_names
    )

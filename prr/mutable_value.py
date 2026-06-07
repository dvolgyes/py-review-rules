"""Mutable expression classification."""

import ast

from prr.dotted_name import dotted_name


def is_mutable_value(node: ast.expr) -> bool:
    """Return whether an expression creates a mutable value."""
    if isinstance(
        node,
        ast.List | ast.Dict | ast.Set | ast.ListComp | ast.DictComp | ast.SetComp,
    ):
        return True
    return isinstance(node, ast.Call) and dotted_name(node.func) in {
        "dict",
        "list",
        "set",
        "collections.defaultdict",
        "defaultdict",
    }

"""Boolean argument classification."""

import ast


def is_bool_arg(arg: ast.arg, default: ast.expr | None) -> bool:
    """Return whether an argument is explicitly or implicitly boolean."""
    if isinstance(default, ast.Constant) and isinstance(default.value, bool):
        return True
    return isinstance(arg.annotation, ast.Name) and arg.annotation.id == "bool"

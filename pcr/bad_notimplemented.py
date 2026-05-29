"""NotImplementedError placeholder classification."""

import ast

from pcr.dotted_name import dotted_name

ABSTRACT_WORDS = frozenset({"abstract", "interface", "override", "subclass"})


def is_bad_notimplemented(node: ast.Raise) -> bool:
    """Return whether NotImplementedError is used as a vague placeholder."""
    if not isinstance(node.exc, ast.Call):
        return dotted_name(node.exc) == "NotImplementedError" if node.exc else False
    if dotted_name(node.exc.func) != "NotImplementedError":
        return False
    if not node.exc.args:
        return True
    first = node.exc.args[0]
    if not isinstance(first, ast.Constant) or not isinstance(first.value, str):
        return True
    return not any(word in first.value.lower() for word in ABSTRACT_WORDS)

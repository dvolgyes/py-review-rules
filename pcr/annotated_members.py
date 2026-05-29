"""Class annotation collection."""

import ast


def annotated_members(node: ast.ClassDef) -> set[str]:
    """Return class-level annotated member names."""
    return {
        child.target.id
        for child in node.body
        if isinstance(child, ast.AnnAssign) and isinstance(child.target, ast.Name)
    }

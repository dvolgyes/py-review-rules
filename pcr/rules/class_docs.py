"""Class documentation rule."""

import ast

from pcr.annotated_members import annotated_members
from pcr.codes import CLASS_DOCSTRING_CODE
from pcr.config import Config
from pcr.documented_members import documented_members
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_class_docs(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check class docstrings and documented members."""
    if not config.classes.require_class_doc:
        return []
    if module_has_noqa(lines, CLASS_DOCSTRING_CODE):
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)
            if not docstring:
                violations.append(
                    Violation(filepath, node.lineno, CLASS_DOCSTRING_CODE, node.name)
                )
            else:
                violations.extend(
                    Violation(filepath, node.lineno, CLASS_DOCSTRING_CODE, member)
                    for member in sorted(
                        annotated_members(node) - documented_members(docstring)
                    )
                )
    return violations

"""Class member hint rule."""

import ast

from pcr.annotated_members import annotated_members
from pcr.codes import CLASS_MEMBER_HINTS_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.unannotated_self_assignment import is_unannotated_self_assignment
from pcr.violation import Violation


def check_class_member_hints(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check ``self`` assignments are declared as class member annotations."""
    if not config.classes.require_class_member_hint:
        return []
    if module_has_noqa(lines, CLASS_MEMBER_HINTS_CODE):
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            members = annotated_members(node)
            violations.extend(
                Violation(filepath, child.lineno, CLASS_MEMBER_HINTS_CODE, node.name)
                for child in ast.walk(node)
                if isinstance(child, ast.Attribute)
                if is_unannotated_self_assignment(child, members)
            )
    return violations

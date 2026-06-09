"""Class member hint rule."""

import ast

from prr.annotated_members import annotated_members
from prr.codes import CLASS_MEMBER_HINTS_CODE
from prr.config import Config
from prr.module_noqa import module_has_noqa
from prr.unannotated_self_assignment import is_unannotated_self_assignment
from prr.violation import Violation


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
                Violation(
                    filepath,
                    child.lineno,
                    CLASS_MEMBER_HINTS_CODE,
                    f"self assignment is missing class member annotation "
                    f"({node.name}.{child.attr}). "
                    f"Document class members at the class level:\n"
                    f"  class {node.name}:\n"
                    f"      {child.attr}: <type>",
                )
                for child in ast.walk(node)
                if isinstance(child, ast.Attribute)
                if is_unannotated_self_assignment(child, members)
            )
    return violations

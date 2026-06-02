"""Class member count rule."""

import ast

from pcr.annotated_members import annotated_members
from pcr.codes import MAX_CLASS_MEMBERS_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_class_member_counts(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check maximum annotated member count per class."""
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        members = annotated_members(node)
        limit = config.counts.max_class_members
        if limit is None or len(members) <= limit:
            continue
        if not module_has_noqa(lines, MAX_CLASS_MEMBERS_CODE):
            violations.append(
                Violation(
                    filepath,
                    node.lineno,
                    MAX_CLASS_MEMBERS_CODE,
                    f"class has too many annotated members ({node.name}): "
                    f"{len(members)} (max {limit})",
                )
            )
    return violations

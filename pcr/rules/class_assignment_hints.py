"""Class assignment type hint rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.codes import TYPE_HINT_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_class_assignment_hints(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check class-level assignments use annotations."""
    if not config.functions.require_type_hint or module_has_noqa(lines, TYPE_HINT_CODE):
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.Assign) and not line_has_noqa(
                    lines, child.lineno, TYPE_HINT_CODE
                ):
                    violations.extend(
                        Violation(filepath, child.lineno, TYPE_HINT_CODE, target.id)
                        for target in child.targets
                        if isinstance(target, ast.Name)
                    )
    return violations

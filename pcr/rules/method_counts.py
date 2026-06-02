"""Class method count rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.ast_utils import is_function
from pcr.codes import MAX_METHODS_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_method_counts(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check maximum method count per class."""
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        methods = [child for child in node.body if is_function(child)]
        limit = config.counts.max_methods
        if limit is None or len(methods) <= limit:
            continue
        if module_has_noqa(lines, MAX_METHODS_CODE):
            continue
        if line_has_noqa(lines, node.lineno, MAX_METHODS_CODE):
            continue
        violations.append(
            Violation(
                filepath,
                methods[limit].lineno,
                MAX_METHODS_CODE,
                f"class has too many methods ({node.name}): "
                f"{len(methods)} (max {limit})",
            )
        )
    return violations

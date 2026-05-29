"""Nested function depth rule."""

import ast

from pcr.codes import FUNCTION_NESTING_CODE
from pcr.config import Config
from pcr.function_depth import collect_function_depth_violations
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_function_nesting(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check nested function depth."""
    limit = config.functions.max_function_nesting_depth
    if limit is None or module_has_noqa(lines, FUNCTION_NESTING_CODE):
        return []
    violations: list[Violation] = []
    collect_function_depth_violations(tree, 0, limit, filepath, lines, violations)
    return violations

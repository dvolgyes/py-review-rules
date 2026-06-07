"""Nested function depth rule."""

import ast

from prr.codes import FUNCTION_NESTING_CODE
from prr.config import Config
from prr.function_depth import collect_function_depth_violations
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


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

"""Nested if depth rule."""

import ast

from pcr.codes import NESTED_IF_CODE
from pcr.config import Config
from pcr.if_depth import collect_if_depth_violations
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_nested_ifs(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check maximum nested if depth."""
    limit = config.control_flow.max_nested_ifs
    if limit is None or module_has_noqa(lines, NESTED_IF_CODE):
        return []
    violations: list[Violation] = []
    collect_if_depth_violations(tree, 0, limit, filepath, lines, violations)
    return violations

"""Nested if depth traversal."""

import ast

from pcr._noqa import line_has_noqa
from pcr.codes import NESTED_IF_CODE
from pcr.is_elif_child import is_elif_child
from pcr.violation import Violation


def collect_if_depth_violations(
    node: ast.AST,
    depth: int,
    limit: int,
    filepath: str,
    lines: list[str],
    violations: list[Violation],
) -> None:
    """Collect nested if depth violations below an AST node."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.If):
            if is_elif_child(node, child):
                collect_if_depth_violations(
                    child, depth, limit, filepath, lines, violations
                )
                continue
            new_depth = depth + 1
            if new_depth > limit and not line_has_noqa(
                lines, child.lineno, NESTED_IF_CODE
            ):
                violations.append(
                    Violation(filepath, child.lineno, NESTED_IF_CODE, "nested if")
                )
            collect_if_depth_violations(
                child, new_depth, limit, filepath, lines, violations
            )
        else:
            collect_if_depth_violations(
                child, depth, limit, filepath, lines, violations
            )

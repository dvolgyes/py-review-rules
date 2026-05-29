"""Nested function depth traversal."""

import ast

from pcr._noqa import line_has_noqa
from pcr.ast_utils import is_function
from pcr.codes import FUNCTION_NESTING_CODE
from pcr.violation import Violation


def collect_function_depth_violations(
    node: ast.AST,
    depth: int,
    limit: int,
    filepath: str,
    lines: list[str],
    violations: list[Violation],
) -> None:
    """Collect nested function depth violations below an AST node."""
    for child in ast.iter_child_nodes(node):
        if is_function(child):
            is_exempt = line_has_noqa(lines, child.lineno, FUNCTION_NESTING_CODE)
            new_depth = depth if is_exempt else depth + 1
            if not is_exempt and new_depth > limit:
                violations.append(
                    Violation(filepath, child.lineno, FUNCTION_NESTING_CODE, child.name)
                )
            collect_function_depth_violations(
                child, new_depth, limit, filepath, lines, violations
            )
        else:
            collect_function_depth_violations(
                child, depth, limit, filepath, lines, violations
            )

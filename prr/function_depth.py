"""Nested function depth traversal."""

import ast

from prr._noqa import line_has_noqa
from prr.ast_utils import is_function
from prr.codes import FUNCTION_NESTING_CODE
from prr.violation import Violation


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
            # Top-level functions (children of Module) are not nested.
            new_depth = (
                depth if (is_exempt or isinstance(node, ast.Module)) else depth + 1
            )
            if not is_exempt and new_depth > limit:
                violations.append(
                    Violation(
                        filepath,
                        child.lineno,
                        FUNCTION_NESTING_CODE,
                        f"function nesting is too deep ({child.name}): "
                        f"{new_depth} (max {limit})",
                    )
                )
            collect_function_depth_violations(
                child, new_depth, limit, filepath, lines, violations
            )
        else:
            collect_function_depth_violations(
                child, depth, limit, filepath, lines, violations
            )

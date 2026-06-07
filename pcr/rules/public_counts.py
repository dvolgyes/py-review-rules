"""Public top-level construct count rules."""

import ast
from typing import TypeGuard

from pcr._noqa import line_has_noqa
from pcr.ast_utils import ConstructNode, FunctionNode, is_function
from pcr.codes import MAX_CLASSES_CODE, MAX_CONSTRUCTS_CODE, MAX_FUNCS_CODE
from pcr.config import Config
from pcr.construct_violation import construct_violation
from pcr.count_violation import count_violation
from pcr.violation import Violation


def check_public_counts(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check public top-level class, function, and combined construct counts."""
    public_classes = [node for node in tree.body if _is_counted_class(node, lines)]
    public_funcs = [node for node in tree.body if _is_counted_function(node, lines)]
    constructs: list[ConstructNode] = [*public_classes, *public_funcs]
    violations = count_violation(
        filepath, public_classes, config.counts.max_classes, MAX_CLASSES_CODE
    )
    violations.extend(
        count_violation(filepath, public_funcs, config.counts.max_funcs, MAX_FUNCS_CODE)
    )
    if violations:
        return violations
    return construct_violation(filepath, lines, constructs, config)


def _is_counted_class(node: ast.AST, lines: list[str]) -> TypeGuard[ast.ClassDef]:
    if not isinstance(node, ast.ClassDef) or node.name.startswith("_"):
        return False
    return not line_has_noqa(
        lines, node.lineno, MAX_CLASSES_CODE
    ) and not line_has_noqa(lines, node.lineno, MAX_CONSTRUCTS_CODE)


def _is_counted_function(node: ast.AST, lines: list[str]) -> TypeGuard[FunctionNode]:
    if not is_function(node) or node.name.startswith("_"):
        return False
    return not line_has_noqa(lines, node.lineno, MAX_FUNCS_CODE) and not line_has_noqa(
        lines, node.lineno, MAX_CONSTRUCTS_CODE
    )

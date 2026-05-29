"""Function and method SLOC rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr._sloc import count_sloc
from pcr.ast_utils import FunctionNode
from pcr.class_member import is_class_member
from pcr.codes import MAX_FUNC_SLOC_CODE, MAX_METHOD_SLOC_CODE
from pcr.config import Config
from pcr.violation import Violation


def check_function_sloc(
    filepath: str,
    lines: list[str],
    node: FunctionNode,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check maximum function and method SLOC."""
    is_method = is_class_member(node, parents)
    code = MAX_METHOD_SLOC_CODE if is_method else MAX_FUNC_SLOC_CODE
    limit = config.size.max_method_sloc if is_method else config.size.max_func_sloc
    if limit is None or line_has_noqa(lines, node.lineno, code):
        return []
    sloc = count_sloc(lines, node.lineno, node.end_lineno or node.lineno)
    if sloc <= limit:
        return []
    kind = "method" if is_method else "function"
    return [
        Violation(
            filepath,
            node.lineno,
            code,
            f"{kind} '{node.name}' has {sloc} SLOC (max {limit})",
        )
    ]

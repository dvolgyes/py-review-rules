"""Function type hint rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.ast_utils import is_function
from pcr.codes import TYPE_HINT_CODE
from pcr.config import Config
from pcr.hinted_args import hinted_args
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_function_type_hints(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check function argument and return type hints."""
    if not config.functions.require_type_hint or module_has_noqa(lines, TYPE_HINT_CODE):
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if is_function(node) and not line_has_noqa(lines, node.lineno, TYPE_HINT_CODE):
            args = hinted_args(node, parents)
            violations.extend(
                Violation(filepath, arg.lineno, TYPE_HINT_CODE, arg.arg)
                for arg in args
                if arg.annotation is None
                and not line_has_noqa(lines, arg.lineno, TYPE_HINT_CODE)
            )
            if node.returns is None:
                violations.append(
                    Violation(filepath, node.lineno, TYPE_HINT_CODE, node.name)
                )
    return violations

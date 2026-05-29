"""Keyword-only default argument rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.ast_utils import is_function
from pcr.codes import KW_ONLY_DEFAULT_CODE
from pcr.config import Config
from pcr.violation import Violation


def check_kw_only_defaults(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check defaulted parameters are keyword-only."""
    if not config.functions.require_kw_only_defaults:
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if is_function(node) and not line_has_noqa(
            lines, node.lineno, KW_ONLY_DEFAULT_CODE
        ):
            positional = [*node.args.posonlyargs, *node.args.args]
            defaulted = (
                positional[-len(node.args.defaults) :] if node.args.defaults else []
            )
            violations.extend(
                Violation(filepath, arg.lineno, KW_ONLY_DEFAULT_CODE, arg.arg)
                for arg in defaulted
                if not line_has_noqa(lines, arg.lineno, KW_ONLY_DEFAULT_CODE)
            )
    return violations

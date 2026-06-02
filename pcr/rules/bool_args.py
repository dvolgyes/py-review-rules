"""Boolean argument count rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.ast_utils import is_function
from pcr.bool_arg import is_bool_arg
from pcr.class_member import is_class_member
from pcr.codes import BOOL_ARG_CODE
from pcr.config import Config
from pcr.defaults_by_arg import defaults_by_arg
from pcr.violation import Violation


def check_bool_args(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check maximum boolean argument count."""
    if config.functions.max_bool_args is None:
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if is_function(node) and not line_has_noqa(lines, node.lineno, BOOL_ARG_CODE):
            args = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
            if (
                is_class_member(node, parents)
                and args
                and args[0].arg in {"self", "cls"}
            ):
                args = args[1:]
            defaults = defaults_by_arg(node)
            count = sum(1 for arg in args if is_bool_arg(arg, defaults.get(arg.arg)))
            if count > config.functions.max_bool_args:
                violations.append(
                    Violation(
                        filepath,
                        node.lineno,
                        BOOL_ARG_CODE,
                        f"function has too many bool args ({node.name}): "
                        f"{count} (max {config.functions.max_bool_args})",
                    )
                )
    return violations

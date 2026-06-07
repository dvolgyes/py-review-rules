"""Boolean argument count rule."""

import ast

from prr._noqa import line_has_noqa
from prr.ast_utils import is_function
from prr.bool_arg import is_bool_arg
from prr.class_member import is_class_member
from prr.codes import BOOL_ARG_CODE
from prr.config import Config
from prr.defaults_by_arg import defaults_by_arg
from prr.violation import Violation


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
        if not is_function(node) or line_has_noqa(lines, node.lineno, BOOL_ARG_CODE):
            continue
        count = _bool_arg_count(node, parents)
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


def _bool_arg_count(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    parents: dict[ast.AST, ast.AST],
) -> int:
    defaults = defaults_by_arg(node)
    return sum(
        1
        for arg in _counted_args(node, parents)
        if is_bool_arg(arg, defaults.get(arg.arg))
    )


def _counted_args(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
    parents: dict[ast.AST, ast.AST],
) -> list[ast.arg]:
    args = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    if is_class_member(node, parents) and args and args[0].arg in {"self", "cls"}:
        return args[1:]
    return args

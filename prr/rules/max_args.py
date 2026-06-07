"""Maximum argument count rule."""

import ast

from prr._noqa import line_has_noqa
from prr.arg_count import arg_count
from prr.ast_utils import is_function
from prr.codes import MAX_ARGS_CODE
from prr.config import Config
from prr.violation import Violation


def check_max_args(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check maximum positional and keyword argument count."""
    if config.functions.max_args is None:
        return []
    violations: list[Violation] = []
    for node in ast.walk(tree):
        if is_function(node) and not line_has_noqa(lines, node.lineno, MAX_ARGS_CODE):
            count = arg_count(node, parents)
            if count > config.functions.max_args:
                violations.append(
                    Violation(
                        filepath,
                        node.lineno,
                        MAX_ARGS_CODE,
                        f"function has too many args ({node.name}): "
                        f"{count} (max {config.functions.max_args})",
                    )
                )
    return violations

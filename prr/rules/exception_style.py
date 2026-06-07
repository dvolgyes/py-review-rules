"""Exception style rules."""

import ast

from prr._noqa import line_has_noqa
from prr.module_noqa import module_has_noqa
from prr.codes import EMPTY_EXCEPT_CODE
from prr.config import Config
from prr.violation import Violation


def check_exception_style(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check exception handlers."""
    if not config.style.ban_pass_only_except:
        return []
    if module_has_noqa(lines, EMPTY_EXCEPT_CODE):
        return []
    return [
        Violation(
            filepath,
            node.lineno,
            EMPTY_EXCEPT_CODE,
            "exception handler only contains pass",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.ExceptHandler)
        and len(node.body) == 1
        and isinstance(node.body[0], ast.Pass)
        and not line_has_noqa(lines, node.lineno, EMPTY_EXCEPT_CODE)
    ]

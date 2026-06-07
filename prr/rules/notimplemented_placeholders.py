"""NotImplementedError placeholder rule."""

import ast

from prr._noqa import line_has_noqa
from prr.bad_notimplemented import is_bad_notimplemented
from prr.codes import NOTIMPLEMENTED_PLACEHOLDER_CODE
from prr.config import Config
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


def check_notimplemented_placeholders(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check vague NotImplementedError placeholders."""
    if not config.style.ban_notimplemented_placeholder:
        return []
    if module_has_noqa(lines, NOTIMPLEMENTED_PLACEHOLDER_CODE):
        return []
    return [
        Violation(
            filepath,
            node.lineno,
            NOTIMPLEMENTED_PLACEHOLDER_CODE,
            "NotImplementedError message is a placeholder",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.Raise)
        and is_bad_notimplemented(node)
        and not line_has_noqa(lines, node.lineno, NOTIMPLEMENTED_PLACEHOLDER_CODE)
    ]

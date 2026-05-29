"""NotImplementedError placeholder rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.bad_notimplemented import is_bad_notimplemented
from pcr.codes import NOTIMPLEMENTED_PLACEHOLDER_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def check_notimplemented_placeholders(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check vague NotImplementedError placeholders."""
    if not config.style.ban_notimplemented_placeholder:
        return []
    if module_has_noqa(lines, NOTIMPLEMENTED_PLACEHOLDER_CODE):
        return []
    return [
        Violation(filepath, node.lineno, NOTIMPLEMENTED_PLACEHOLDER_CODE, "placeholder")
        for node in ast.walk(tree)
        if isinstance(node, ast.Raise)
        and is_bad_notimplemented(node)
        and not line_has_noqa(lines, node.lineno, NOTIMPLEMENTED_PLACEHOLDER_CODE)
    ]

"""Function documentation rule."""

import ast

from prr._noqa import line_has_noqa
from prr.module_noqa import module_has_noqa
from prr.ast_utils import is_function
from prr.codes import FUNCTION_DOCSTRING_CODE
from prr.config import Config
from prr.violation import Violation


def check_function_docs(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check public functions and methods have docstrings."""
    if not config.functions.require_function_doc:
        return []
    if module_has_noqa(lines, FUNCTION_DOCSTRING_CODE):
        return []
    return [
        Violation(
            filepath,
            node.lineno,
            FUNCTION_DOCSTRING_CODE,
            f"missing function docstring ({node.name})",
        )
        for node in ast.walk(tree)
        if is_function(node)
        and not node.name.startswith("_")
        and ast.get_docstring(node) is None
        and not line_has_noqa(lines, node.lineno, FUNCTION_DOCSTRING_CODE)
    ]

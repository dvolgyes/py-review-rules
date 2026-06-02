"""Function documentation rule."""

import ast

from pcr._noqa import line_has_noqa
from pcr.module_noqa import module_has_noqa
from pcr.ast_utils import is_function
from pcr.codes import FUNCTION_DOCSTRING_CODE
from pcr.config import Config
from pcr.violation import Violation


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

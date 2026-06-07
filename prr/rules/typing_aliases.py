"""Legacy typing alias rule."""

import ast

from prr._noqa import line_has_noqa
from prr.banned_typing_alias import uses_banned_typing_alias
from prr.codes import TYPING_ALIAS_CODE
from prr.config import Config
from prr.dotted_name import dotted_name
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


def check_typing_aliases(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check legacy ``typing.List``-style aliases are absent."""
    if not config.imports.ban_typing_alias or module_has_noqa(lines, TYPING_ALIAS_CODE):
        return []
    typing_names = {
        alias.asname or "typing"
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
        if alias.name == "typing"
    }
    return [
        Violation(
            filepath,
            node.lineno,
            TYPING_ALIAS_CODE,
            f"legacy typing alias is banned ({_typing_alias_label(node)})",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom | ast.Attribute)
        if uses_banned_typing_alias(node, typing_names)
        and not line_has_noqa(lines, node.lineno, TYPING_ALIAS_CODE)
    ]


def _typing_alias_label(node: ast.ImportFrom | ast.Attribute) -> str:
    if isinstance(node, ast.ImportFrom):
        names = ", ".join(alias.name for alias in node.names)
        return f"typing.{names}"
    return dotted_name(node) or "typing alias"

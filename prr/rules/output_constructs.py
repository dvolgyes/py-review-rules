"""Output construct rules."""

import ast

from prr._noqa import line_has_noqa
from prr.banned_output_call import is_banned_output_call
from prr.click_aliases import click_aliases
from prr.codes import OUTPUT_CONSTRUCT_CODE
from prr.config import Config
from prr.dotted_name import dotted_name
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


def check_output_constructs(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check banned output constructs."""
    if not config.style.ban_output_construct:
        return []
    if module_has_noqa(lines, OUTPUT_CONSTRUCT_CODE):
        return []
    click_names, echo_names = click_aliases(tree)
    return [
        Violation(
            filepath,
            node.lineno,
            OUTPUT_CONSTRUCT_CODE,
            f"banned stdout output call ({dotted_name(node.func) or 'call'})",
        )
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and is_banned_output_call(node, click_names, echo_names)
        and not line_has_noqa(lines, node.lineno, OUTPUT_CONSTRUCT_CODE)
    ]

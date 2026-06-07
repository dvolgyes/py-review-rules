"""Class SLOC rule."""

import ast

from prr._noqa import line_has_noqa
from prr._sloc import count_sloc
from prr.codes import MAX_CLASS_SLOC_CODE
from prr.config import Config
from prr.violation import Violation


def check_class_sloc(
    filepath: str, lines: list[str], node: ast.ClassDef, config: Config
) -> list[Violation]:
    """Check maximum class SLOC."""
    if config.size.max_class_sloc is None:
        return []
    if line_has_noqa(lines, node.lineno, MAX_CLASS_SLOC_CODE):
        return []
    sloc = count_sloc(lines, node.lineno, node.end_lineno or node.lineno)
    if sloc <= config.size.max_class_sloc:
        return []
    return [
        Violation(
            filepath,
            node.lineno,
            MAX_CLASS_SLOC_CODE,
            f"class '{node.name}' has {sloc} SLOC (max {config.size.max_class_sloc})",
        )
    ]

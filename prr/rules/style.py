"""Style rule orchestration."""

import ast

from prr.config import Config
from prr.rules.exception_style import check_exception_style
from prr.rules.mutable_globals import check_mutable_globals
from prr.rules.output_constructs import check_output_constructs
from prr.rules.placeholders import check_placeholders
from prr.violation import Violation


def check_style(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check globals, exceptions, output, and placeholder code."""
    violations = check_mutable_globals(filepath, lines, tree, config)
    violations.extend(check_exception_style(filepath, lines, tree, config))
    violations.extend(check_output_constructs(filepath, lines, tree, config))
    violations.extend(check_placeholders(filepath, lines, tree, config))
    return violations

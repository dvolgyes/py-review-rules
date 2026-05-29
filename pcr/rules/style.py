"""Style rule orchestration."""

import ast

from pcr.config import Config
from pcr.rules.exception_style import check_exception_style
from pcr.rules.mutable_globals import check_mutable_globals
from pcr.rules.output_constructs import check_output_constructs
from pcr.rules.placeholders import check_placeholders
from pcr.violation import Violation


def check_style(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check globals, exceptions, output, and placeholder code."""
    violations = check_mutable_globals(filepath, lines, tree, config)
    violations.extend(check_exception_style(filepath, lines, tree, config))
    violations.extend(check_output_constructs(filepath, lines, tree, config))
    violations.extend(check_placeholders(filepath, lines, tree, config))
    return violations

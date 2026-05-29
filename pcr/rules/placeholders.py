"""Placeholder rule orchestration."""

import ast

from pcr.config import Config
from pcr.rules.notimplemented_placeholders import check_notimplemented_placeholders
from pcr.rules.placeholder_comments import check_placeholder_comments
from pcr.rules.placeholder_passes import check_placeholder_passes
from pcr.violation import Violation


def check_placeholders(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check placeholder comments, pass statements, and NotImplementedError."""
    violations = check_placeholder_comments(filepath, lines, config)
    violations.extend(check_placeholder_passes(filepath, lines, tree, config))
    violations.extend(check_notimplemented_placeholders(filepath, lines, tree, config))
    return violations

"""Placeholder rule orchestration."""

import ast

from prr.config import Config
from prr.rules.notimplemented_placeholders import check_notimplemented_placeholders
from prr.rules.placeholder_comments import check_placeholder_comments
from prr.rules.placeholder_passes import check_placeholder_passes
from prr.violation import Violation


def check_placeholders(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check placeholder comments, pass statements, and NotImplementedError."""
    violations = check_placeholder_comments(filepath, lines, config)
    violations.extend(check_placeholder_passes(filepath, lines, tree, config))
    violations.extend(check_notimplemented_placeholders(filepath, lines, tree, config))
    return violations

"""Top-level count rule orchestration."""

import ast

from prr.rules.local_helpers import check_local_helpers
from prr.rules.public_counts import check_public_counts
from prr.test_paths import is_test_file
from prr.config import Config
from prr.violation import Violation


def check_counts(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    config: Config,
) -> list[Violation]:
    """Check top-level public and private helper counts."""
    if is_test_file(filepath):
        return []
    violations = check_public_counts(filepath, lines, tree, config)
    violations.extend(check_local_helpers(filepath, lines, tree, config))
    return violations

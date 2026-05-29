"""Control-flow rule orchestration."""

import ast

from pcr.config import Config
from pcr.rules.elifs import check_elifs
from pcr.rules.nested_ifs import check_nested_ifs
from pcr.violation import Violation


def check_control_flow(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check elif counts and nested if depth."""
    violations = check_elifs(filepath, lines, tree, config)
    violations.extend(check_nested_ifs(filepath, lines, tree, config))
    return violations

"""Import rule orchestration."""

import ast

from pcr.config import Config
from pcr.rules.banned_imports import check_banned_imports
from pcr.rules.future_imports import check_future_imports
from pcr.rules.top_level_imports import check_top_level_imports
from pcr.rules.typing_aliases import check_typing_aliases
from pcr.violation import Violation


def check_imports(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check import placement, bans, future imports, and typing aliases."""
    violations = check_future_imports(filepath, lines, tree, config)
    violations.extend(check_top_level_imports(filepath, lines, tree, parents, config))
    violations.extend(check_banned_imports(filepath, lines, tree, config))
    violations.extend(check_typing_aliases(filepath, lines, tree, config))
    return violations

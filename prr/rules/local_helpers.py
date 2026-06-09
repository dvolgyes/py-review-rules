"""Local helper count rule."""

import ast

from prr._noqa import line_has_noqa
from prr.module_noqa import module_has_noqa
from prr.ast_utils import is_function
from prr.codes import LOCAL_HELPERS_CODE
from prr.config import Config
from prr.violation import Violation


def check_local_helpers(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check private top-level helper function count."""
    limit = config.counts.max_local_helpers
    if limit is None or module_has_noqa(lines, LOCAL_HELPERS_CODE):
        return []
    helpers = [
        node
        for node in tree.body
        if is_function(node)
        and node.name.startswith("_")
        and not line_has_noqa(lines, node.lineno, LOCAL_HELPERS_CODE)
    ]
    if len(helpers) <= limit:
        return []
    names = ", ".join(node.name for node in helpers)
    return [
        Violation(
            filepath,
            helpers[limit].lineno,
            LOCAL_HELPERS_CODE,
            f"file has {len(helpers)} local helper functions (max {limit}); "
            f"consider organizing into their own module: {names}",
        )
    ]

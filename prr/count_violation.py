"""Count violation construction."""

from collections.abc import Sequence

from prr.ast_utils import ConstructNode
from prr.codes import MAX_CLASSES_CODE
from prr.violation import Violation

MAX_DETAIL_ITEMS = 3


def count_violation(
    filepath: str, nodes: Sequence[ConstructNode], limit: int | None, code: str
) -> list[Violation]:
    """Return a violation when a node list exceeds a limit."""
    if limit is None or len(nodes) <= limit:
        return []
    if code == MAX_CLASSES_CODE:
        label = "public classes"
        hint = "consider one class per file"
    else:
        label = "public functions"
        hint = "consider organizing functions into their own module"
    message = f"too many {label}: {len(nodes)} (max {limit}); {hint}"
    if len(nodes) <= MAX_DETAIL_ITEMS:
        names = ", ".join(node.name for node in nodes)
        message = f"{message}: {names}"
    return [
        Violation(
            filepath,
            nodes[limit].lineno,
            code,
            message,
        )
    ]

"""Count violation construction."""

from collections.abc import Sequence

from pcr.ast_utils import ConstructNode
from pcr.codes import MAX_CLASSES_CODE
from pcr.violation import Violation

MAX_DETAIL_ITEMS = 3


def count_violation(
    filepath: str, nodes: Sequence[ConstructNode], limit: int | None, code: str
) -> list[Violation]:
    """Return a violation when a node list exceeds a limit."""
    if limit is None or len(nodes) <= limit:
        return []
    label = "public classes" if code == MAX_CLASSES_CODE else "public functions"
    message = f"too many {label}: {len(nodes)} (max {limit})"
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

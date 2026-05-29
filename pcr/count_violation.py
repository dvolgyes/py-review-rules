"""Count violation construction."""

from collections.abc import Sequence

from pcr.ast_utils import ConstructNode
from pcr.violation import Violation


def count_violation(
    filepath: str, nodes: Sequence[ConstructNode], limit: int | None, code: str
) -> list[Violation]:
    """Return a violation when a node list exceeds a limit."""
    if limit is None or len(nodes) <= limit:
        return []
    names = ", ".join(node.name for node in nodes)
    return [Violation(filepath, nodes[limit].lineno, code, f"too many: {names}")]

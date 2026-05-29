"""Combined public construct violation construction."""

from collections.abc import Sequence

from pcr.ast_utils import ConstructNode
from pcr.codes import MAX_CONSTRUCTS_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation


def construct_violation(
    filepath: str, lines: list[str], nodes: Sequence[ConstructNode], config: Config
) -> list[Violation]:
    """Return a violation when combined public constructs exceed the limit."""
    limit = config.counts.max_constructs
    if limit is None or module_has_noqa(lines, MAX_CONSTRUCTS_CODE):
        return []
    if len(nodes) <= limit:
        return []
    names = ", ".join(node.name for node in nodes)
    sorted_nodes = sorted(nodes, key=lambda node: node.lineno)
    return [
        Violation(
            filepath,
            sorted_nodes[limit].lineno,
            MAX_CONSTRUCTS_CODE,
            f"file has {len(nodes)} public constructs (max {limit}): {names}",
        )
    ]

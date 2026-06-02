"""Combined public construct violation construction."""

from collections.abc import Sequence

from pcr.ast_utils import ConstructNode
from pcr.codes import MAX_CONSTRUCTS_CODE
from pcr.config import Config
from pcr.module_noqa import module_has_noqa
from pcr.violation import Violation

MAX_DETAIL_ITEMS = 3


def construct_violation(
    filepath: str, lines: list[str], nodes: Sequence[ConstructNode], config: Config
) -> list[Violation]:
    """Return a violation when combined public constructs exceed the limit."""
    limit = config.counts.max_constructs
    if limit is None or module_has_noqa(lines, MAX_CONSTRUCTS_CODE):
        return []
    if len(nodes) <= limit:
        return []
    message = f"file has {len(nodes)} public constructs (max {limit})"
    if len(nodes) <= MAX_DETAIL_ITEMS:
        names = ", ".join(node.name for node in nodes)
        message = f"{message}: {names}"
    sorted_nodes = sorted(nodes, key=lambda node: node.lineno)
    return [
        Violation(
            filepath,
            sorted_nodes[limit].lineno,
            MAX_CONSTRUCTS_CODE,
            message,
        )
    ]

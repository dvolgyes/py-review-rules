"""Unified project constraint checks."""

import ast

from pcr.config import Config
from pcr.parents import parents
from pcr.rules.classes import check_classes
from pcr.rules.control_flow import check_control_flow
from pcr.rules.counts import check_counts
from pcr.rules.functions import check_functions
from pcr.rules.imports import check_imports
from pcr.rules.sloc import check_sloc
from pcr.rules.style import check_style
from pcr.violation import Violation


def check_file(filepath: str, source: str, config: Config) -> list[Violation]:
    """Run all enabled checks for a Python file."""
    lines = source.splitlines()
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        return []

    node_parents = parents(tree)
    violations: list[Violation] = []
    violations.extend(check_sloc(filepath, lines, tree, node_parents, config))
    violations.extend(check_counts(filepath, lines, tree, config))
    violations.extend(check_imports(filepath, lines, tree, node_parents, config))
    violations.extend(check_functions(filepath, lines, tree, node_parents, config))
    violations.extend(check_classes(filepath, lines, tree, config))
    violations.extend(check_style(filepath, lines, tree, config))
    violations.extend(check_control_flow(filepath, lines, tree, config))
    return violations

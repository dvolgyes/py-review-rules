"""Unified project constraint checks."""

import ast

from prr.config import Config
from prr.parents import parents
from prr.rules.classes import check_classes
from prr.rules.control_flow import check_control_flow
from prr.rules.counts import check_counts
from prr.rules.functions import check_functions
from prr.rules.imports import check_imports
from prr.rules.sloc import check_sloc
from prr.rules.style import check_style
from prr.violation import Violation


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

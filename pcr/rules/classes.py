"""Class rule orchestration."""

import ast

from pcr.config import Config
from pcr.rules.class_assignment_hints import check_class_assignment_hints
from pcr.rules.class_docs import check_class_docs
from pcr.rules.class_member_counts import check_class_member_counts
from pcr.rules.class_member_hints import check_class_member_hints
from pcr.rules.method_counts import check_method_counts
from pcr.violation import Violation


def check_classes(
    filepath: str, lines: list[str], tree: ast.Module, config: Config
) -> list[Violation]:
    """Check class member, method, and documentation rules."""
    violations = check_method_counts(filepath, lines, tree, config)
    violations.extend(check_class_member_counts(filepath, lines, tree, config))
    violations.extend(check_class_member_hints(filepath, lines, tree, config))
    violations.extend(check_class_docs(filepath, lines, tree, config))
    violations.extend(check_class_assignment_hints(filepath, lines, tree, config))
    return violations

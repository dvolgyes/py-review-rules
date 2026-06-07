"""Class rule orchestration."""

import ast

from prr.config import Config
from prr.rules.class_assignment_hints import check_class_assignment_hints
from prr.rules.class_docs import check_class_docs
from prr.rules.class_member_counts import check_class_member_counts
from prr.rules.class_member_hints import check_class_member_hints
from prr.rules.method_counts import check_method_counts
from prr.violation import Violation


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

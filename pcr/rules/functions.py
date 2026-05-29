"""Function rule orchestration."""

import ast

from pcr.config import Config
from pcr.rules.bool_args import check_bool_args
from pcr.rules.function_docs import check_function_docs
from pcr.rules.function_nesting import check_function_nesting
from pcr.rules.function_type_hints import check_function_type_hints
from pcr.rules.kw_only_defaults import check_kw_only_defaults
from pcr.rules.max_args import check_max_args
from pcr.violation import Violation


def check_functions(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check function signatures, docs, and nesting."""
    violations = check_max_args(filepath, lines, tree, parents, config)
    violations.extend(check_bool_args(filepath, lines, tree, parents, config))
    violations.extend(check_kw_only_defaults(filepath, lines, tree, config))
    violations.extend(check_function_docs(filepath, lines, tree, config))
    violations.extend(check_function_type_hints(filepath, lines, tree, parents, config))
    violations.extend(check_function_nesting(filepath, lines, tree, config))
    return violations

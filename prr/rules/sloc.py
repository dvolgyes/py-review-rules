"""SLOC rule orchestration."""

import ast

from prr.config import Config
from prr.rules.class_sloc import check_class_sloc
from prr.rules.file_sloc import check_file_sloc
from prr.rules.function_sloc import check_function_sloc
from prr.violation import Violation


def check_sloc(
    filepath: str,
    lines: list[str],
    tree: ast.Module,
    parents: dict[ast.AST, ast.AST],
    config: Config,
) -> list[Violation]:
    """Check file, class, function, and method SLOC limits."""
    violations = check_file_sloc(filepath, lines, config)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            violations.extend(check_class_sloc(filepath, lines, node, config))
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            violations.extend(
                check_function_sloc(filepath, lines, node, parents, config)
            )
    return violations

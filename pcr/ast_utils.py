"""AST helper predicates."""

import ast
from typing import TypeGuard

FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef
ConstructNode = ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef


def is_function(node: ast.AST) -> TypeGuard[FunctionNode]:
    """Return whether an AST node is a function definition."""
    return isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)

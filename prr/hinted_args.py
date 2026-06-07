"""Function arguments requiring type hints."""

import ast

from prr.ast_utils import FunctionNode
from prr.class_member import is_class_member


def hinted_args(node: FunctionNode, parents: dict[ast.AST, ast.AST]) -> list[ast.arg]:
    """Return arguments that require annotations."""
    args = [*node.args.posonlyargs, *node.args.args]
    if is_class_member(node, parents) and args and args[0].arg in {"self", "cls"}:
        args = args[1:]
    return [*args, *node.args.kwonlyargs]

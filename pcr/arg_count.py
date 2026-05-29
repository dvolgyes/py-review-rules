"""Function argument counting."""

import ast

from pcr.ast_utils import FunctionNode
from pcr.class_member import is_class_member


def arg_count(node: FunctionNode, parents: dict[ast.AST, ast.AST]) -> int:
    """Return the effective argument count for a function."""
    args = [*node.args.posonlyargs, *node.args.args]
    if is_class_member(node, parents) and args and args[0].arg in {"self", "cls"}:
        args = args[1:]
    count = len(args) + len(node.args.kwonlyargs)
    return count + int(node.args.vararg is not None) + int(node.args.kwarg is not None)

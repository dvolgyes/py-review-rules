"""Function default mapping."""

import ast

from pcr.ast_utils import FunctionNode


def defaults_by_arg(node: FunctionNode) -> dict[str, ast.expr]:
    """Return defaults keyed by argument name."""
    positional = [*node.args.posonlyargs, *node.args.args]
    return {
        arg.arg: default
        for arg, default in zip(
            positional[-len(node.args.defaults) :], node.args.defaults, strict=False
        )
    } | {
        arg.arg: default
        for arg, default in zip(
            node.args.kwonlyargs, node.args.kw_defaults, strict=False
        )
        if default is not None
    }

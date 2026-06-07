"""Click import alias collection."""

import ast


def click_aliases(tree: ast.Module) -> tuple[set[str], set[str]]:
    """Return imported click and click.echo aliases."""
    click_names: set[str] = set()
    echo_names: set[str] = set()
    for node in ast.walk(tree):
        click_names.update(_click_import_aliases(node))
        echo_names.update(_echo_import_aliases(node))
    return click_names, echo_names


def _click_import_aliases(node: ast.AST) -> set[str]:
    if not isinstance(node, ast.Import):
        return set()
    return {alias.asname or "click" for alias in node.names if alias.name == "click"}


def _echo_import_aliases(node: ast.AST) -> set[str]:
    if not isinstance(node, ast.ImportFrom) or node.module != "click":
        return set()
    return {alias.asname or "echo" for alias in node.names if alias.name == "echo"}

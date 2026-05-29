"""Click import alias collection."""

import ast


def click_aliases(tree: ast.Module) -> tuple[set[str], set[str]]:
    """Return imported click and click.echo aliases."""
    click_names: set[str] = set()
    echo_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            click_names.update(
                alias.asname or "click" for alias in node.names if alias.name == "click"
            )
        if isinstance(node, ast.ImportFrom) and node.module == "click":
            echo_names.update(
                alias.asname or "echo" for alias in node.names if alias.name == "echo"
            )
    return click_names, echo_names

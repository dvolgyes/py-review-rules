"""Pre-commit hook: enforce maximum nesting depth for function definitions."""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

import click
from loguru import logger


@dataclass(frozen=True)
class NestingViolation:
    filepath: str
    line: int
    name: str
    depth: int
    max_allowed: int


def _walk_nesting(
    node: ast.AST,
    current_depth: int,
    max_depth: int,
    filepath: str,
    violations: list[NestingViolation],
) -> None:
    """Recursively walk AST nodes, tracking function nesting depth."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.FunctionDef | ast.AsyncFunctionDef):
            new_depth = current_depth + 1
            if new_depth > max_depth:
                violations.append(
                    NestingViolation(
                        filepath=filepath,
                        line=child.lineno,
                        name=child.name,
                        depth=new_depth,
                        max_allowed=max_depth,
                    )
                )
            _walk_nesting(child, new_depth, max_depth, filepath, violations)
        elif isinstance(child, ast.ClassDef):
            # Classes don't increase nesting depth
            _walk_nesting(child, current_depth, max_depth, filepath, violations)
        else:
            _walk_nesting(child, current_depth, max_depth, filepath, violations)


def check_file(
    filepath: str,
    source: str,
    max_depth: int,
) -> list[NestingViolation]:
    """Check a single file for functions exceeding the maximum nesting depth."""
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        logger.warning("Skipping {} (syntax error)", filepath)
        return []

    violations: list[NestingViolation] = []
    _walk_nesting(tree, 0, max_depth, filepath, violations)
    return violations


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--max-depth", default=2, type=int, show_default=True)
@click.option("--logfile", default=None, type=click.Path(), help="Optional log file.")
@click.option("--loglevel", default="INFO", help="Log level.")
def main(
    files: tuple[str, ...],
    max_depth: int,
    logfile: str | None,
    loglevel: str,
) -> None:
    """Check that function definitions don't exceed a maximum nesting depth."""
    logger.remove()
    logger.add(sys.stderr, level=loglevel)
    if logfile:
        logger.add(logfile, level=loglevel)

    all_violations: list[NestingViolation] = []
    for filepath in files:
        source = Path(filepath).read_text(encoding="utf-8")
        all_violations.extend(check_file(filepath, source, max_depth))

    for v in all_violations:
        print(  # noqa: T201
            f"{v.filepath}:{v.line}: function '{v.name}' is nested {v.depth} levels deep (max {v.max_allowed})"
        )

    raise SystemExit(1 if all_violations else 0)


if __name__ == "__main__":
    main()

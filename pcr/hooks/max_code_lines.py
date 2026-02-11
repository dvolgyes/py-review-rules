"""Pre-commit hook: enforce maximum SLOC per function/class."""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

import click
from loguru import logger

from pcr.hooks._sloc import count_sloc


@dataclass(frozen=True)
class Violation:
    filepath: str
    line: int
    name: str
    kind: str
    sloc_count: int
    max_allowed: int


def check_file(
    filepath: str,
    source: str,
    max_function_lines: int,
    max_class_lines: int,
) -> list[Violation]:
    """Check a single file for functions/classes exceeding SLOC limits."""
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        logger.warning("Skipping {} (syntax error)", filepath)
        return []

    lines = source.splitlines()
    violations: list[Violation] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            sloc = count_sloc(lines, node.lineno, node.end_lineno or node.lineno)
            if sloc > max_class_lines:
                violations.append(
                    Violation(
                        filepath, node.lineno, node.name, "class", sloc, max_class_lines
                    )
                )

        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            sloc = count_sloc(lines, node.lineno, node.end_lineno or node.lineno)
            if sloc > max_function_lines:
                violations.append(
                    Violation(
                        filepath,
                        node.lineno,
                        node.name,
                        "function",
                        sloc,
                        max_function_lines,
                    )
                )

    return violations


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--max-function-lines", default=50, type=int, show_default=True)
@click.option("--max-class-lines", default=200, type=int, show_default=True)
@click.option("--logfile", default=None, type=click.Path(), help="Optional log file.")
@click.option("--loglevel", default="INFO", help="Log level.")
def main(
    files: tuple[str, ...],
    max_function_lines: int,
    max_class_lines: int,
    logfile: str | None,
    loglevel: str,
) -> None:
    """Check that functions and classes don't exceed SLOC limits."""
    logger.remove()
    logger.add(sys.stderr, level=loglevel)
    if logfile:
        logger.add(logfile, level=loglevel)

    all_violations: list[Violation] = []
    for filepath in files:
        source = Path(filepath).read_text(encoding="utf-8")
        all_violations.extend(
            check_file(filepath, source, max_function_lines, max_class_lines)
        )

    for v in all_violations:
        print(  # noqa: T201
            f"{v.filepath}:{v.line}: {v.kind} '{v.name}' has {v.sloc_count} SLOC (max {v.max_allowed})"
        )

    raise SystemExit(1 if all_violations else 0)


if __name__ == "__main__":
    main()

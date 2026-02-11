"""Pre-commit hook: ban specific Python constructs via AST analysis."""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

import click
from loguru import logger


@dataclass(frozen=True)
class BanViolation:
    filepath: str
    line: int
    construct: str
    message: str


def parse_ban_spec(spec: str) -> tuple[str, str]:
    """Split 'construct:message' on the first colon."""
    construct, _, message = spec.partition(":")
    return construct, message


def reconstruct_dotted_name(node: ast.expr) -> str | None:
    """Reconstruct a dotted name like 'click.echo' from an AST Attribute/Name chain."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = reconstruct_dotted_name(node.value)
        if parent is not None:
            return f"{parent}.{node.attr}"
    return None


def _scan_imports(
    tree: ast.Module,
    filepath: str,
    banned: dict[str, str],
) -> tuple[list[BanViolation], dict[str, str]]:
    """Scan import statements for banned constructs."""
    violations: list[BanViolation] = []
    alias_map: dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                full_name = f"{node.module}.{alias.name}"
                if full_name in banned:
                    violations.append(
                        BanViolation(
                            filepath, node.lineno, full_name, banned[full_name]
                        )
                    )
                    alias_map[alias.asname or alias.name] = full_name

        if isinstance(node, ast.Import):
            violations.extend(
                BanViolation(filepath, node.lineno, alias.name, banned[alias.name])
                for alias in node.names
                if alias.name in banned
            )

    return violations, alias_map


def _scan_usage(
    tree: ast.Module,
    filepath: str,
    banned: dict[str, str],
    alias_map: dict[str, str],
) -> list[BanViolation]:
    """Scan AST for usage of banned constructs."""
    violations: list[BanViolation] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            dotted = reconstruct_dotted_name(node)
            if dotted and dotted in banned:
                violations.append(
                    BanViolation(filepath, node.lineno, dotted, banned[dotted])
                )
        elif isinstance(node, ast.Name) and node.id in alias_map:
            construct = alias_map[node.id]
            violations.append(
                BanViolation(filepath, node.lineno, construct, banned[construct])
            )

    return violations


def check_file(
    filepath: str,
    source: str,
    banned: dict[str, str],
) -> list[BanViolation]:
    """Check a single file for banned constructs."""
    try:
        tree = ast.parse(source, filename=filepath)
    except SyntaxError:
        logger.warning("Skipping {} (syntax error)", filepath)
        return []

    import_violations, alias_map = _scan_imports(tree, filepath, banned)
    usage_violations = _scan_usage(tree, filepath, banned, alias_map)
    return import_violations + usage_violations


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--ban", multiple=True, help="Format: 'construct:error message'")
@click.option("--logfile", default=None, type=click.Path(), help="Optional log file.")
@click.option("--loglevel", default="INFO", help="Log level.")
def main(
    files: tuple[str, ...],
    ban: tuple[str, ...],
    logfile: str | None,
    loglevel: str,
) -> None:
    """Check files for banned Python constructs."""
    logger.remove()
    logger.add(sys.stderr, level=loglevel)
    if logfile:
        logger.add(logfile, level=loglevel)

    banned: dict[str, str] = {}
    for spec in ban:
        construct, message = parse_ban_spec(spec)
        banned[construct] = message

    all_violations: list[BanViolation] = []
    for filepath in files:
        source = Path(filepath).read_text(encoding="utf-8")
        all_violations.extend(check_file(filepath, source, banned))

    for v in all_violations:
        print(f"{v.filepath}:{v.line}: banned construct '{v.construct}': {v.message}")  # noqa: T201

    raise SystemExit(1 if all_violations else 0)


if __name__ == "__main__":
    main()

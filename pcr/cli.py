"""Unified command-line interface for pcr."""

import sys
from pathlib import Path

import click

from pcr.check import check_file
from pcr.config import Config
from pcr.csv_options import split_csv

main = click.Group(help="Project constraint checks.")


@main.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--max-sloc", default=800, type=int, show_default=True)
@click.option("--max-func-sloc", default=500, type=int, show_default=True)
@click.option("--max-class-sloc", default=800, type=int, show_default=True)
@click.option("--max-method-sloc", default=300, type=int, show_default=True)
@click.option("--max-constructs", default=1, type=int, show_default=True)
@click.option("--max-classes", default=1, type=int, show_default=True)
@click.option("--max-funcs", default=1, type=int, show_default=True)
@click.option("--banned-import", multiple=True)
@click.option("--max-args", default=6, type=int, show_default=True)
@click.option("--max-methods", default=10, type=int, show_default=True)
@click.option("--max-class-members", default=10, type=int, show_default=True)
@click.option(
    "--require-class-member-hint/--no-require-class-member-hint",
    default=True,
    show_default=True,
)
@click.option(
    "--require-class-doc/--no-require-class-doc",
    default=True,
    show_default=True,
)
@click.option(
    "--require-function-doc/--no-require-function-doc",
    default=True,
    show_default=True,
)
@click.option(
    "--require-top-level-import/--no-require-top-level-import",
    default=True,
    show_default=True,
)
@click.option(
    "--ban-future-import/--no-ban-future-import", default=True, show_default=True
)
@click.option(
    "--require-type-hint/--no-require-type-hint", default=True, show_default=True
)
@click.option(
    "--ban-typing-alias/--no-ban-typing-alias", default=True, show_default=True
)
@click.option(
    "--ban-mutable-global/--no-ban-mutable-global", default=True, show_default=True
)
@click.option(
    "--ban-pass-only-except/--no-ban-pass-only-except",
    default=True,
    show_default=True,
)
@click.option(
    "--ban-output-construct/--no-ban-output-construct",
    default=True,
    show_default=True,
)
@click.option(
    "--ban-placeholder-comment/--no-ban-placeholder-comment",
    default=True,
    show_default=True,
)
@click.option(
    "--ban-placeholder-pass/--no-ban-placeholder-pass",
    default=True,
    show_default=True,
)
@click.option(
    "--ban-notimplemented-placeholder/--no-ban-notimplemented-placeholder",
    default=True,
    show_default=True,
)
@click.option("--max-bool-args", default=1, type=int, show_default=True)
@click.option(
    "--require-kw-only-defaults/--no-require-kw-only-defaults",
    default=True,
    show_default=True,
)
@click.option("--max-elifs", default=2, type=int, show_default=True)
@click.option("--max-nested-ifs", default=2, type=int, show_default=True)
@click.option("--max-function-nesting-depth", default=2, type=int, show_default=True)
@click.option("--max-local-helpers", default=2, type=int, show_default=True)
def check(files: tuple[str, ...], **options: object) -> None:
    """Check Python files against enabled rules."""
    banned_import = options.pop("banned_import")
    if not isinstance(banned_import, tuple):
        banned_import = ()
    options["banned_imports"] = split_csv(
        tuple(item for item in banned_import if isinstance(item, str))
    )
    config = Config.from_options(options)

    violations = []
    for filepath in files:
        source = Path(filepath).read_text(encoding="utf-8")
        violations.extend(check_file(filepath, source, config))

    for violation in violations:
        sys.stderr.write(
            f"{violation.filepath}:{violation.line}: "
            f"{violation.code}: {violation.message}\n"
        )

    raise SystemExit(1 if violations else 0)


if __name__ == "__main__":
    sys.exit(main())

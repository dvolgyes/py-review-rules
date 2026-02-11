"""Pre-commit hook: ban specific packages from the resolved dependency tree."""

import json
import re
import subprocess
import sys
from dataclasses import dataclass

import click
from loguru import logger
from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import Version


@dataclass(frozen=True)
class BannedDepViolation:
    package: str
    installed_version: str
    specifier: str
    message: str


# Matches where the version specifier starts (first operator character)
_SPECIFIER_RE = re.compile(r"[~<>=!]")


def parse_ban_spec(spec: str) -> tuple[str, str, str]:
    """Parse 'name[specifier]:message' into (name, specifier, message).

    Examples:
        "requests:use httpx" -> ("requests", "", "use httpx")
        "requests<2.0:too old" -> ("requests", "<2.0", "too old")
        "requests>=1.0,<2.0:bad" -> ("requests", ">=1.0,<2.0", "bad")
    """
    # Split on first colon that is NOT part of a version specifier.
    # Version specifiers never contain ':', so first ':' is always the delimiter.
    # But we need to find where the specifier starts (before the colon).
    colon_idx = spec.index(":")
    name_and_spec = spec[:colon_idx]
    message = spec[colon_idx + 1 :]

    match = _SPECIFIER_RE.search(name_and_spec)
    if match:
        name = name_and_spec[: match.start()]
        specifier = name_and_spec[match.start() :]
    else:
        name = name_and_spec
        specifier = ""

    return name, specifier, message


def check_installed_packages(
    packages: list[dict[str, str]],
    bans: list[tuple[str, str, str]],
) -> list[BannedDepViolation]:
    """Check installed packages against ban list."""
    violations: list[BannedDepViolation] = []
    pkg_map: dict[str, str] = {}
    for pkg in packages:
        pkg_map[pkg["name"].lower()] = pkg["version"]

    for name, specifier, message in bans:
        version_str = pkg_map.get(name.lower())
        if version_str is None:
            continue

        if not specifier:
            # Banned unconditionally
            violations.append(BannedDepViolation(name, version_str, specifier, message))
            continue

        try:
            spec_set = SpecifierSet(specifier)
        except InvalidSpecifier:
            logger.warning("Invalid specifier '{}' for package '{}'", specifier, name)
            continue

        if Version(version_str) in spec_set:
            violations.append(BannedDepViolation(name, version_str, specifier, message))

    return violations


def _get_installed_packages() -> list[dict[str, str]]:
    """Get installed packages via uv pip list."""
    result = subprocess.run(
        ["uv", "pip", "list", "--format", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        logger.error("Failed to run 'uv pip list': {}", result.stderr.strip())
        return []
    return json.loads(result.stdout)  # type: ignore[no-any-return]


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--ban", multiple=True, help="Format: 'package[specifier]:message'")
@click.option("--logfile", default=None, type=click.Path(), help="Optional log file.")
@click.option("--loglevel", default="INFO", help="Log level.")
def main(
    files: tuple[str, ...],
    ban: tuple[str, ...],
    logfile: str | None,
    loglevel: str,
) -> None:
    """Check that banned packages are not in the dependency tree."""
    logger.remove()
    logger.add(sys.stderr, level=loglevel)
    if logfile:
        logger.add(logfile, level=loglevel)

    bans: list[tuple[str, str, str]] = []
    for spec in ban:
        name, specifier, message = parse_ban_spec(spec)
        bans.append((name, specifier, message))

    if not bans:
        raise SystemExit(0)

    packages = _get_installed_packages()
    violations = check_installed_packages(packages, bans)

    for v in violations:
        version_info = f" {v.specifier}" if v.specifier else ""
        print(  # noqa: T201
            f"Banned dependency '{v.package}{version_info}' "
            f"is installed (version {v.installed_version}): {v.message}"
        )

    raise SystemExit(1 if violations else 0)


if __name__ == "__main__":
    main()

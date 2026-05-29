"""Module-level noqa detection."""

from pcr._noqa import line_has_noqa


def module_has_noqa(source_lines: list[str], code: str | None) -> bool:
    """Return whether the module header has a matching noqa marker."""
    for line_number, line in enumerate(source_lines, start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("#"):
            return False
        if line_has_noqa(source_lines, line_number, code):
            return True
    return False

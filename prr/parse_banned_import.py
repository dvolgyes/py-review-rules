"""Banned import spec parsing."""


def parse_banned_import(spec: str) -> tuple[str, str | None]:
    """Return banned import name and optional alternative."""
    alternative: str | None
    if "->" in spec:
        name, alternative = spec.split("->", maxsplit=1)
    elif "=" in spec:
        name, alternative = spec.split("=", maxsplit=1)
    else:
        name, alternative = spec, None
    if alternative is not None:
        alternative = alternative.strip() or None
    return name.strip(), alternative

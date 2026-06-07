"""Optional integer option coercion."""


def optional_int(value: object) -> int | None:
    """Return an optional integer option."""
    return value if isinstance(value, int) else None

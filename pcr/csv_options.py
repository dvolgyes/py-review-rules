"""CSV option parsing."""


def split_csv(values: tuple[str, ...]) -> tuple[str, ...]:
    """Split repeated comma-separated option values."""
    return tuple(
        item.strip() for value in values for item in value.split(",") if item.strip()
    )

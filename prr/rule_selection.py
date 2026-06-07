"""Rule-code selection for reported violations."""

from prr.csv_options import split_csv
from prr.violation import Violation


def selected_violations(
    violations: list[Violation], select: object, ignore: object
) -> tuple[list[Violation], str | None]:
    """Filter violations by selected or ignored rule codes."""
    selected = _csv_option(select)
    ignored = _csv_option(ignore)
    if selected and ignored:
        return violations, "--select and --ignore are mutually exclusive"
    if selected:
        selected_codes = set(selected)
        return [
            violation for violation in violations if violation.code in selected_codes
        ], None
    if ignored:
        ignored_codes = set(ignored)
        return [
            violation for violation in violations if violation.code not in ignored_codes
        ], None
    return violations, None


def _csv_option(value: object) -> tuple[str, ...]:
    if not isinstance(value, tuple):
        return ()
    return split_csv(tuple(item for item in value if isinstance(item, str)))

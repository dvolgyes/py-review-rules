"""Violation model."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Violation:
    """A single check violation.

    :ivar filepath: path to the checked file
    :ivar line: 1-based source line
    :ivar code: PRR rule code
    :ivar message: human-readable violation details
    """

    filepath: str
    line: int
    code: str
    message: str

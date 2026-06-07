"""File SLOC rule."""

from prr._sloc import count_sloc
from prr.codes import MAX_SLOC_CODE
from prr.config import Config
from prr.module_noqa import module_has_noqa
from prr.violation import Violation


def check_file_sloc(filepath: str, lines: list[str], config: Config) -> list[Violation]:
    """Check maximum file SLOC."""
    if config.size.max_sloc is None or module_has_noqa(lines, MAX_SLOC_CODE):
        return []
    sloc = count_sloc(lines, 1, len(lines))
    if sloc <= config.size.max_sloc:
        return []
    return [
        Violation(
            filepath,
            1,
            MAX_SLOC_CODE,
            f"file has {sloc} SLOC (max {config.size.max_sloc})",
        )
    ]

from pcr._noqa import line_has_noqa
from pcr.module_noqa import module_has_noqa


def test_line_noqa_is_whitespace_insensitive() -> None:
    lines = ["def f():  #noqa: PCR102"]
    assert line_has_noqa(lines, 1, "PCR102")


def test_bare_noqa_matches_any_code() -> None:
    lines = ["def f():  # noqa"]
    assert line_has_noqa(lines, 1, "PCR102")


def test_specific_noqa_does_not_match_other_code() -> None:
    lines = ["def f():  # noqa: PCR501"]
    assert not line_has_noqa(lines, 1, "PCR102")


def test_module_noqa_is_read_from_header_comment() -> None:
    lines = ["", "#noqa:PCR501", "def a():", "    pass"]
    assert module_has_noqa(lines, "PCR501")

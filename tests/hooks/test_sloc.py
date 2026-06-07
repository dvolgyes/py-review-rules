from prr._sloc import count_sloc


def test_counts_only_code_lines() -> None:
    lines = [
        "def foo():",
        "    x = 1",
        "",
        "    # comment",
        "    return x",
    ]
    assert count_sloc(lines, start_line=1, end_line=5) == 3


def test_single_line() -> None:
    lines = ["x = 1"]
    assert count_sloc(lines, start_line=1, end_line=1) == 1


def test_all_blank_and_comments() -> None:
    lines = ["", "  # comment", "   ", "# another"]
    assert count_sloc(lines, start_line=1, end_line=4) == 0


def test_indented_comment() -> None:
    lines = ["def f():", "    # todo", "    pass"]
    assert count_sloc(lines, start_line=1, end_line=3) == 2


def test_partial_range() -> None:
    lines = ["a = 1", "b = 2", "c = 3", "d = 4"]
    assert count_sloc(lines, start_line=2, end_line=3) == 2

from pcr.hooks.max_code_lines import Violation, check_file


def test_short_function_no_violation() -> None:
    source = "def f():\n    return 1\n"
    assert (
        check_file("test.py", source, max_function_lines=50, max_class_lines=200) == []
    )


def test_function_exceeding_limit() -> None:
    body = "\n".join(f"    x{i} = {i}" for i in range(10))
    source = f"def big():\n{body}\n"
    violations = check_file(
        "test.py", source, max_function_lines=5, max_class_lines=200
    )
    assert len(violations) == 1
    v = violations[0]
    assert v.name == "big"
    assert v.kind == "function"
    assert v.sloc_count == 11  # def + 10 body lines
    assert v.max_allowed == 5


def test_class_exceeding_limit() -> None:
    body = "\n".join(f"    x{i} = {i}" for i in range(10))
    source = f"class Big:\n{body}\n"
    violations = check_file("test.py", source, max_function_lines=50, max_class_lines=5)
    assert len(violations) == 1
    assert violations[0].kind == "class"
    assert violations[0].name == "Big"


def test_method_checked_individually() -> None:
    method_body = "\n".join(f"        x{i} = {i}" for i in range(10))
    source = f"class C:\n    def m(self):\n{method_body}\n"
    violations = check_file(
        "test.py", source, max_function_lines=5, max_class_lines=200
    )
    assert any(v.kind == "function" and v.name == "m" for v in violations)


def test_decorators_excluded_from_count() -> None:
    # 2 decorator lines should NOT be counted
    body = "\n".join(f"    x{i} = {i}" for i in range(5))
    source = f"@decorator1\n@decorator2\ndef f():\n{body}\n"
    violations = check_file(
        "test.py", source, max_function_lines=6, max_class_lines=200
    )
    assert violations == []  # 6 SLOC (def + 5 body), limit is 6


def test_async_function() -> None:
    body = "\n".join(f"    x{i} = {i}" for i in range(10))
    source = f"async def big():\n{body}\n"
    violations = check_file(
        "test.py", source, max_function_lines=5, max_class_lines=200
    )
    assert len(violations) == 1
    assert violations[0].name == "big"


def test_blank_and_comment_lines_not_counted() -> None:
    lines = ["def f():"]
    for i in range(20):
        lines.append(f"    x{i} = {i}")
        lines.append("")
        lines.append("    # comment")
    source = "\n".join(lines) + "\n"
    violations = check_file(
        "test.py", source, max_function_lines=50, max_class_lines=200
    )
    # 21 SLOC: def + 20 body, blanks/comments excluded
    assert violations == []


def test_violation_dataclass_is_frozen() -> None:
    v = Violation(
        filepath="a.py", line=1, name="f", kind="function", sloc_count=10, max_allowed=5
    )
    try:
        v.name = "other"  # type: ignore[misc]
        msg = "should be frozen"
        raise AssertionError(msg)
    except AttributeError:
        pass

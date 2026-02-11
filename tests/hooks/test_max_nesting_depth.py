from pcr.hooks.max_nesting_depth import NestingViolation, check_file


def test_flat_function_no_violation() -> None:
    source = "def f():\n    return 1\n"
    assert check_file("test.py", source, max_depth=2) == []


def test_nested_function_within_limit() -> None:
    source = "def outer():\n    def inner():\n        return 1\n"
    assert check_file("test.py", source, max_depth=2) == []


def test_triple_nested_function_violation() -> None:
    source = "def a():\n    def b():\n        def c():\n            return 1\n"
    violations = check_file("test.py", source, max_depth=2)
    assert len(violations) == 1
    v = violations[0]
    assert v.filepath == "test.py"
    assert v.line == 3
    assert v.name == "c"
    assert v.depth == 3
    assert v.max_allowed == 2


def test_async_functions_count_same_as_regular() -> None:
    source = (
        "async def a():\n"
        "    async def b():\n"
        "        async def c():\n"
        "            return 1\n"
    )
    violations = check_file("test.py", source, max_depth=2)
    assert len(violations) == 1
    assert violations[0].name == "c"
    assert violations[0].depth == 3


def test_class_method_does_not_count_as_extra_nesting() -> None:
    source = "class MyClass:\n    def method(self):\n        return 1\n"
    assert check_file("test.py", source, max_depth=1) == []


def test_nested_function_inside_class_method() -> None:
    source = (
        "class MyClass:\n"
        "    def method(self):\n"
        "        def helper():\n"
        "            return 1\n"
    )
    # method is depth 1 (class doesn't count), helper is depth 2
    assert check_file("test.py", source, max_depth=2) == []
    violations = check_file("test.py", source, max_depth=1)
    assert len(violations) == 1
    assert violations[0].name == "helper"
    assert violations[0].depth == 2


def test_custom_max_depth_parameter() -> None:
    source = (
        "def a():\n"
        "    def b():\n"
        "        def c():\n"
        "            def d():\n"
        "                return 1\n"
    )
    # max_depth=3: only d (depth 4) should violate
    violations = check_file("test.py", source, max_depth=3)
    assert len(violations) == 1
    assert violations[0].name == "d"
    assert violations[0].depth == 4


def test_violation_reports_correct_fields() -> None:
    source = "def outer():\n    def middle():\n        def deep():\n            pass\n"
    violations = check_file("src/app.py", source, max_depth=2)
    assert len(violations) == 1
    v = violations[0]
    assert v.filepath == "src/app.py"
    assert v.line == 3
    assert v.name == "deep"
    assert v.depth == 3
    assert v.max_allowed == 2


def test_nesting_violation_is_frozen() -> None:
    v = NestingViolation(filepath="a.py", line=1, name="f", depth=3, max_allowed=2)
    try:
        v.name = "other"  # type: ignore[misc]
        msg = "should be frozen"
        raise AssertionError(msg)
    except AttributeError:
        pass

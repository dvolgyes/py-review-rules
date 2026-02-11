from pcr.hooks.ban_constructs import BanViolation, check_file, parse_ban_spec


def test_parse_ban_spec() -> None:
    construct, message = parse_ban_spec("click.echo:use loguru instead")
    assert construct == "click.echo"
    assert message == "use loguru instead"


def test_parse_ban_spec_with_colons_in_message() -> None:
    construct, message = parse_ban_spec("click.echo:use loguru: it's better")
    assert construct == "click.echo"
    assert message == "use loguru: it's better"


def test_direct_attribute_access() -> None:
    source = "import click\nclick.echo('hi')\n"
    banned = {"click.echo": "use loguru"}
    violations = check_file("test.py", source, banned)
    assert len(violations) == 1
    assert violations[0].line == 2
    assert violations[0].construct == "click.echo"


def test_from_import() -> None:
    source = "from click import echo\necho('hi')\n"
    banned = {"click.echo": "use loguru"}
    violations = check_file("test.py", source, banned)
    # Violation on import line + usage line
    assert len(violations) == 2
    assert violations[0].line == 1  # import
    assert violations[1].line == 2  # usage


def test_aliased_import() -> None:
    source = "from click import echo as e\ne('hi')\n"
    banned = {"click.echo": "use loguru"}
    violations = check_file("test.py", source, banned)
    assert len(violations) == 2
    assert violations[0].line == 1  # import
    assert violations[1].line == 2  # aliased usage


def test_direct_import() -> None:
    source = "import os.path\n"
    banned = {"os.path": "use pathlib"}
    violations = check_file("test.py", source, banned)
    assert len(violations) == 1
    assert violations[0].construct == "os.path"


def test_no_violation() -> None:
    source = "from loguru import logger\nlogger.info('hi')\n"
    banned = {"click.echo": "use loguru"}
    assert check_file("test.py", source, banned) == []


def test_violation_dataclass_is_frozen() -> None:
    v = BanViolation(
        filepath="a.py", line=1, construct="click.echo", message="use loguru"
    )
    try:
        v.construct = "other"  # type: ignore[misc]
        msg = "should be frozen"
        raise AssertionError(msg)
    except AttributeError:
        pass


def test_syntax_error_skips_file() -> None:
    source = "def f(\n"  # invalid syntax
    banned = {"click.echo": "use loguru"}
    assert check_file("test.py", source, banned) == []

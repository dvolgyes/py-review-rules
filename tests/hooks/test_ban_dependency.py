from pcr.hooks.ban_dependency import (
    BannedDepViolation,
    check_installed_packages,
    parse_ban_spec,
)


def test_parse_ban_spec_name_only() -> None:
    name, specifier, message = parse_ban_spec("requests:use httpx instead")
    assert name == "requests"
    assert specifier == ""
    assert message == "use httpx instead"


def test_parse_ban_spec_with_version() -> None:
    name, specifier, message = parse_ban_spec("requests<2.0:too old")
    assert name == "requests"
    assert specifier == "<2.0"
    assert message == "too old"


def test_parse_ban_spec_complex_version() -> None:
    name, specifier, message = parse_ban_spec("requests>=1.0,<2.0:bad range")
    assert name == "requests"
    assert specifier == ">=1.0,<2.0"
    assert message == "bad range"


def test_parse_ban_spec_tilde_equals() -> None:
    name, specifier, message = parse_ban_spec("requests~=2.0:compat issue")
    assert name == "requests"
    assert specifier == "~=2.0"
    assert message == "compat issue"


def test_parse_ban_spec_double_equals() -> None:
    name, specifier, message = parse_ban_spec("requests==2.28.0:pinned bad")
    assert name == "requests"
    assert specifier == "==2.28.0"
    assert message == "pinned bad"


def test_check_ban_name_only() -> None:
    packages = [{"name": "requests", "version": "2.28.0"}]
    bans = [("requests", "", "use httpx")]
    violations = check_installed_packages(packages, bans)
    assert len(violations) == 1
    assert violations[0].package == "requests"
    assert violations[0].installed_version == "2.28.0"


def test_check_ban_version_match() -> None:
    packages = [{"name": "requests", "version": "1.5.0"}]
    bans = [("requests", "<2.0", "too old")]
    violations = check_installed_packages(packages, bans)
    assert len(violations) == 1


def test_check_ban_version_no_match() -> None:
    packages = [{"name": "requests", "version": "2.5.0"}]
    bans = [("requests", "<2.0", "too old")]
    violations = check_installed_packages(packages, bans)
    assert violations == []


def test_check_ban_not_installed() -> None:
    packages = [{"name": "click", "version": "8.0.0"}]
    bans = [("requests", "", "use httpx")]
    violations = check_installed_packages(packages, bans)
    assert violations == []


def test_check_ban_case_insensitive() -> None:
    packages = [{"name": "PyYAML", "version": "6.0"}]
    bans = [("pyyaml", "", "use ruamel.yaml")]
    violations = check_installed_packages(packages, bans)
    assert len(violations) == 1


def test_check_ban_multiple() -> None:
    packages = [
        {"name": "requests", "version": "2.28.0"},
        {"name": "pyyaml", "version": "6.0"},
    ]
    bans = [
        ("requests", "", "use httpx"),
        ("pyyaml", "", "use ruamel.yaml"),
    ]
    violations = check_installed_packages(packages, bans)
    assert len(violations) == 2


def test_violation_is_frozen() -> None:
    v = BannedDepViolation(
        package="requests", installed_version="2.28.0", specifier="", message="bad"
    )
    try:
        v.package = "other"  # type: ignore[misc]
        msg = "should be frozen"
        raise AssertionError(msg)
    except AttributeError:
        pass


def test_check_ban_complex_specifier() -> None:
    packages = [{"name": "requests", "version": "1.5.0"}]
    bans = [("requests", ">=1.0,<2.0", "bad range")]
    violations = check_installed_packages(packages, bans)
    assert len(violations) == 1


def test_check_ban_complex_specifier_no_match() -> None:
    packages = [{"name": "requests", "version": "2.5.0"}]
    bans = [("requests", ">=1.0,<2.0", "bad range")]
    violations = check_installed_packages(packages, bans)
    assert violations == []

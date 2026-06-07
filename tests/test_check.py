from pathlib import Path

from click.testing import CliRunner

from prr.check import check_file
from prr.cli import main
from prr.config import Config
from prr.default_options import default_options


def relaxed_config(**kwargs: object) -> Config:
    config = default_options()
    for key in config:
        if isinstance(config[key], bool):
            config[key] = False
        elif key != "banned_imports":
            config[key] = None
    config.update(kwargs)
    return Config.from_options(config)


def codes(source: str, config: Config) -> list[str]:
    return [violation.code for violation in check_file("test.py", source, config)]


def messages(source: str, config: Config, *, filepath: str = "test.py") -> list[str]:
    return [violation.message for violation in check_file(filepath, source, config)]


def test_max_sloc() -> None:
    source = "\n".join(f"x{i} = {i}" for i in range(3))
    assert codes(source, relaxed_config(max_sloc=2)) == ["PRR001"]


def test_max_function_class_and_method_sloc() -> None:
    source = (
        "def f():\n"
        "    x = 1\n"
        "    y = 2\n"
        "\n"
        "class C:\n"
        "    x: int\n"
        "    def m(self):\n"
        "        a = 1\n"
        "        b = 2\n"
    )
    result = codes(
        source,
        relaxed_config(max_func_sloc=2, max_class_sloc=4, max_method_sloc=2),
    )
    assert result == ["PRR002", "PRR003", "PRR004"]


def test_top_level_construct_limits_ignore_private_names() -> None:
    source = (
        "def a():\n"
        "    pass\n"
        "def b():\n"
        "    pass\n"
        "class C:\n"
        "    pass\n"
        "class _D:\n"
        "    pass\n"
    )
    result = codes(source, relaxed_config(max_constructs=1, max_classes=0, max_funcs=1))
    assert result == ["PRR006", "PRR007"]


def test_top_level_construct_limit_reports_when_specific_limits_pass() -> None:
    source = "def a():\n    pass\nclass C:\n    pass\n"
    result = codes(source, relaxed_config(max_constructs=1, max_classes=1, max_funcs=1))
    assert result == ["PRR005"]


def test_public_function_limit_ignores_private_names() -> None:
    source = (
        "def public():\n"
        "    pass\n"
        "def _private_a():\n"
        "    pass\n"
        "def _private_b():\n"
        "    pass\n"
    )
    result = codes(source, relaxed_config(max_constructs=1, max_funcs=1))
    assert not result


def test_top_level_construct_limits_ignore_test_files() -> None:
    source = "def test_a() -> None:\n    return None\n\ndef test_b() -> None:\n    return None\n"
    violations = check_file(
        "tests/test_many.py",
        source,
        relaxed_config(max_constructs=1, max_classes=1, max_funcs=1),
    )
    assert not violations


def test_banned_import_supports_alternatives() -> None:
    assert codes(
        "import pyyaml\n", relaxed_config(banned_imports=("pyyaml=ruamel.yaml",))
    ) == ["PRR008"]


def test_banned_import_supports_arrow_alternative() -> None:
    assert codes(
        "import pyyaml\n", relaxed_config(banned_imports=("pyyaml->ruamel.yaml",))
    ) == ["PRR008"]


def test_banned_import_accepts_comma_separated_cli_values(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("import pyyaml\n", encoding="utf-8")
    result = CliRunner().invoke(
        main,
        [
            "check",
            "--banned-import=osgeo, pyyaml->ruamel.yaml, pyaml->ruamel.yaml",
            "--no-require-function-doc",
            "--no-require-class-doc",
            str(path),
        ],
    )
    assert result.exit_code == 1
    assert "PRR008" in result.stderr


def test_max_args_counts_varargs_and_kwargs_but_not_self() -> None:
    source = "class C:\n    def m(self, a, *args, b, **kwargs):\n        pass\n"
    assert codes(source, relaxed_config(max_args=3)) == ["PRR009"]


def test_max_methods() -> None:
    source = (
        "class C:\n    def a(self):\n        pass\n    def b(self):\n        pass\n"
    )
    assert codes(source, relaxed_config(max_methods=1)) == ["PRR010"]


def test_class_member_hints_reject_undeclared_self_assignment() -> None:
    source = (
        "class C:\n"
        "    x: int\n"
        "    def __init__(self):\n"
        "        self.x = 1\n"
        "        self.y = 2\n"
    )
    assert codes(source, relaxed_config(require_class_member_hint=True)) == ["PRR011"]


def test_max_class_members() -> None:
    source = "class C:\n    x: int\n    y: int\n"
    assert codes(source, relaxed_config(max_class_members=1)) == ["PRR012"]


def test_class_docstring_requires_ivar_entries() -> None:
    source = 'class C:\n    """Class docs."""\n    x: int\n'
    assert codes(source, relaxed_config(require_class_doc=True)) == ["PRR013"]


def test_class_docstring_accepts_documented_members() -> None:
    source = 'class C:\n    """Class docs.\n\n    :ivar x: value\n    """\n    x: int\n'
    assert not codes(source, relaxed_config(require_class_doc=True))


def test_function_docstring_required() -> None:
    source = "def f():\n    pass\n"
    assert codes(source, relaxed_config(require_function_doc=True)) == ["PRR014"]


def test_top_level_imports_required() -> None:
    source = "def f():\n    import os\n"
    assert codes(source, relaxed_config(require_top_level_import=True)) == ["PRR015"]


def test_future_annotations_import_is_banned() -> None:
    source = "from __future__ import annotations\n"
    assert codes(source, relaxed_config(ban_future_import=True)) == ["PRR016"]


def test_type_hints_required_for_arguments_returns_and_class_members() -> None:
    source = "class C:\n    x = 1\n\ndef f(a, *args, **kwargs):\n    pass\n"
    assert codes(source, relaxed_config(require_type_hint=True)) == [
        "PRR017",
        "PRR017",
        "PRR017",
    ]


def test_type_hint_noqa_exempts_single_line() -> None:
    source = (
        "class C:\n    x = 1  # noqa: PRR017\n\ndef f(a):  # noqa: PRR017\n    pass\n"
    )
    assert not codes(source, relaxed_config(require_type_hint=True))


def test_typing_alias_import_and_usage_are_banned() -> None:
    source = "import typing as t\nfrom typing import Dict\nx: t.Optional[str]\n"
    assert codes(source, relaxed_config(ban_typing_alias=True)) == [
        "PRR018",
        "PRR018",
    ]


def test_module_level_mutables_are_banned_with_noqa_override() -> None:
    source = "ALLOWED = []  # noqa: PRR019\nBLOCKED = {}\n"
    assert codes(source, relaxed_config(ban_mutable_global=True)) == ["PRR019"]


def test_module_level_mutable_message_names_target() -> None:
    source = "BLOCKED = {}\n"
    assert messages(source, relaxed_config(ban_mutable_global=True)) == [
        "mutable global variable (BLOCKED)"
    ]


def test_init_all_is_not_a_mutable_global_violation() -> None:
    config = relaxed_config(ban_mutable_global=True)
    source = "__all__ = ['main']\nCACHE = {}\n"
    assert messages(source, config, filepath="pkg/__init__.py") == [
        "mutable global variable (CACHE)"
    ]
    assert messages("__all__ = ['main']\n", config, filepath="pkg/module.py") == [
        "mutable global variable (__all__)"
    ]


def test_pass_only_exception_handlers_are_banned() -> None:
    source = "try:\n    risky()\nexcept ValueError:\n    pass\n"
    assert codes(source, relaxed_config(ban_pass_only_except=True)) == ["PRR020"]


def test_print_and_click_echo_are_banned() -> None:
    source = "import click as c\nprint('x')\nc.echo('x')\n"
    assert codes(source, relaxed_config(ban_output_construct=True)) == [
        "PRR021",
        "PRR021",
    ]


def test_placeholder_comments_and_pass_are_banned() -> None:
    source = "# TODO: finish\n\ndef f() -> None:\n    pass\n"
    assert codes(
        source,
        relaxed_config(ban_placeholder_comment=True, ban_placeholder_pass=True),
    ) == ["PRR022", "PRR023"]


def test_notimplemented_placeholder_is_banned_but_abstract_contract_is_allowed() -> (
    None
):
    bad = "def f() -> None:\n    raise NotImplementedError('TODO')\n"
    good = (
        "def f() -> None:\n"
        "    raise NotImplementedError('Subclasses must override this method')\n"
    )
    config = relaxed_config(ban_notimplemented_placeholder=True)
    assert codes(bad, config) == ["PRR024"]
    assert not codes(good, config)


def test_max_bool_args_defaults_to_one() -> None:
    source = "def f(*, a: bool, b: bool = False) -> None:\n    return None\n"
    assert codes(source, relaxed_config(max_bool_args=1)) == ["PRR025"]


def test_defaulted_positional_args_must_be_keyword_only() -> None:
    source = "def f(a: int = 1, *, b: int = 2) -> None:\n    return None\n"
    assert codes(source, relaxed_config(require_kw_only_defaults=True)) == ["PRR026"]


def test_max_elifs() -> None:
    source = (
        "if a:\n    x = 1\nelif b:\n    x = 2\nelif c:\n    x = 3\nelif d:\n    x = 4\n"
    )
    assert codes(source, relaxed_config(max_elifs=2)) == ["PRR027"]


def test_max_nested_ifs_ignores_elif_chain() -> None:
    source = "if a:\n    if b:\n        if c:\n            x = 1\nelif d:\n    x = 2\n"
    assert codes(source, relaxed_config(max_nested_ifs=2)) == ["PRR028"]


def test_noqa_exempts_specific_unified_rule() -> None:
    source = "def f(a, b):  # noqa: PRR009\n    pass\n"
    assert not codes(source, relaxed_config(max_args=1))


def test_diagnostics_explain_rule_and_subject() -> None:
    assert messages(
        "def f(a, b):\n    return None\n",
        relaxed_config(max_args=1),
    ) == ["function has too many args (f): 2 (max 1)"]
    assert messages(
        'class C:\n    """Docs."""\n    files: list[str]\n',
        relaxed_config(require_class_doc=True),
    ) == ["missing class docstring member entry (:ivar files:)"]
    assert messages(
        "def f() -> None:\n    import numpy\n",
        relaxed_config(require_top_level_import=True),
    ) == ["import is not top level (numpy)"]
    assert messages(
        "def main():\n    pass\n\ndef configure_logging():\n    pass\n",
        relaxed_config(max_funcs=1),
    ) == ["too many public functions: 2 (max 1): main, configure_logging"]
    assert messages(
        "def a():\n    pass\n"
        "def b():\n    pass\n"
        "def c():\n    pass\n"
        "def d():\n    pass\n",
        relaxed_config(max_funcs=1),
    ) == ["too many public functions: 4 (max 1)"]


def test_cli_check_reports_violations(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("def f(a, b):\n    return None\n", encoding="utf-8")
    result = CliRunner().invoke(
        main,
        [
            "check",
            "--max-args=1",
            "--no-require-function-doc",
            "--no-require-type-hint",
            str(path),
        ],
    )
    assert result.exit_code == 1
    assert (
        result.stderr == "PRR009 function has too many args (f): 2 (max 1)\n"
        f"  --> {path}:1\n"
        "\n"
        "Found 1 bug.\n"
    )


def test_cli_check_colors_code_and_description(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("def f(a, b):\n    return None\n", encoding="utf-8")
    result = CliRunner().invoke(
        main,
        [
            "check",
            "--max-args=1",
            "--no-require-function-doc",
            "--no-require-type-hint",
            "--color=always",
            str(path),
        ],
    )
    assert result.exit_code == 1
    assert "\x1b[31mPRR009\x1b[0m" in result.stderr
    assert "\x1b[34mfunction has too many args (f): 2 (max 1)\x1b[0m" in result.stderr


def test_cli_check_accepts_directories_recursively(tmp_path: Path) -> None:
    root = tmp_path / "pkg"
    nested = root / "nested"
    nested.mkdir(parents=True)
    (root / "ok.txt").write_text(
        "def ignored(a, b):\n    return None\n", encoding="utf-8"
    )
    (root / "top.py").write_text("def top(a, b):\n    return None\n", encoding="utf-8")
    (nested / "deep.py").write_text(
        "def deep(a, b):\n    return None\n", encoding="utf-8"
    )

    result = CliRunner().invoke(
        main,
        [
            "check",
            "--max-args=1",
            "--no-require-function-doc",
            "--no-require-type-hint",
            str(root),
        ],
    )

    assert result.exit_code == 1
    assert f"  --> {root / 'top.py'}:1" in result.stderr
    assert f"  --> {nested / 'deep.py'}:1" in result.stderr
    assert result.stderr.endswith("Found 2 bugs.\n")
    assert "ok.txt" not in result.stderr


def test_cli_check_selects_codes(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("def f(a, b):\n    return None\n", encoding="utf-8")
    result = CliRunner().invoke(
        main,
        [
            "check",
            "--max-args=1",
            "--no-require-type-hint",
            "--select=PRR009",
            str(path),
        ],
    )
    assert result.exit_code == 1
    assert "PRR009" in result.stderr
    assert "PRR014" not in result.stderr


def test_cli_check_ignores_codes(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("def f(a, b):\n    return None\n", encoding="utf-8")
    result = CliRunner().invoke(
        main,
        [
            "check",
            "--max-args=1",
            "--no-require-type-hint",
            "--ignore=PRR014",
            str(path),
        ],
    )
    assert result.exit_code == 1
    assert "PRR009" in result.stderr
    assert "PRR014" not in result.stderr


def test_cli_check_rejects_select_with_ignore(tmp_path: Path) -> None:
    path = tmp_path / "bad.py"
    path.write_text("def f() -> None:\n    return None\n", encoding="utf-8")
    result = CliRunner().invoke(
        main,
        ["check", "--select=PRR009", "--ignore=PRR014", str(path)],
    )
    assert result.exit_code == 2
    assert "--select and --ignore are mutually exclusive" in result.stderr

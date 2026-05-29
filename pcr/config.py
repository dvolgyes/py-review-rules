"""Checker configuration."""

from dataclasses import dataclass, field
from collections.abc import Iterable

from pcr.optional_int import optional_int


@dataclass(frozen=True)
class _SizeConfig:
    """Size limits.

    :ivar max_sloc: maximum file SLOC
    :ivar max_func_sloc: maximum top-level function SLOC
    :ivar max_class_sloc: maximum class SLOC
    :ivar max_method_sloc: maximum method SLOC
    """

    max_sloc: int | None = 800
    max_func_sloc: int | None = 500
    max_class_sloc: int | None = 800
    max_method_sloc: int | None = 300


@dataclass(frozen=True)
class _CountConfig:
    """Top-level and class count limits.

    :ivar max_constructs: maximum public top-level classes and functions
    :ivar max_classes: maximum public top-level classes
    :ivar max_funcs: maximum public top-level functions
    :ivar max_methods: maximum methods per class
    :ivar max_class_members: maximum annotated class members
    :ivar max_local_helpers: maximum private top-level helper functions
    """

    max_constructs: int | None = 1
    max_classes: int | None = 1
    max_funcs: int | None = 1
    max_methods: int | None = 10
    max_class_members: int | None = 10
    max_local_helpers: int | None = 2


@dataclass(frozen=True)
class _FunctionConfig:
    """Function interface rules.

    :ivar max_args: maximum function parameters
    :ivar max_bool_args: maximum boolean parameters
    :ivar require_function_doc: require function docstrings
    :ivar require_type_hint: require argument and return type hints
    :ivar require_kw_only_defaults: require defaulted parameters to be keyword-only
    :ivar max_function_nesting_depth: maximum nested function depth
    """

    max_args: int | None = 6
    max_bool_args: int | None = 1
    require_function_doc: bool = True
    require_type_hint: bool = True
    require_kw_only_defaults: bool = True
    max_function_nesting_depth: int | None = 2


@dataclass(frozen=True)
class _ClassConfig:
    """Class rules.

    :ivar require_class_member_hint: require class member annotations
    :ivar require_class_doc: require class docs and member docs
    """

    require_class_member_hint: bool = True
    require_class_doc: bool = True


@dataclass(frozen=True)
class _ImportConfig:
    """Import rules.

    :ivar banned_imports: import names that should not appear
    :ivar require_top_level_import: require imports directly at module top level
    :ivar ban_future_import: ban future annotations import
    :ivar ban_typing_alias: ban legacy typing aliases
    """

    banned_imports: tuple[str, ...] = ()
    require_top_level_import: bool = True
    ban_future_import: bool = True
    ban_typing_alias: bool = True


@dataclass(frozen=True)
class _StyleConfig:
    """Style and placeholder rules.

    :ivar ban_mutable_global: ban module-level mutable values
    :ivar ban_pass_only_except: ban exception handlers that only pass
    :ivar ban_output_construct: ban print and click.echo
    :ivar ban_placeholder_comment: ban TODO-style comments
    :ivar ban_placeholder_pass: ban pass as placeholder code
    :ivar ban_notimplemented_placeholder: ban vague NotImplementedError placeholders
    """

    ban_mutable_global: bool = True
    ban_pass_only_except: bool = True
    ban_output_construct: bool = True
    ban_placeholder_comment: bool = True
    ban_placeholder_pass: bool = True
    ban_notimplemented_placeholder: bool = True


@dataclass(frozen=True)
class _ControlFlowConfig:
    """Control-flow shape rules.

    :ivar max_elifs: maximum elif branches in one chain
    :ivar max_nested_ifs: maximum nested if depth
    """

    max_elifs: int | None = 2
    max_nested_ifs: int | None = 2


@dataclass(frozen=True)
class Config:
    """Configuration for enabled project checks.

    :ivar size: size-related checks
    :ivar counts: count-related checks
    :ivar functions: function rules
    :ivar classes: class rules
    :ivar imports: import rules
    :ivar style: style rules
    :ivar control_flow: control-flow rules
    """

    size: _SizeConfig = field(default_factory=_SizeConfig)
    counts: _CountConfig = field(default_factory=_CountConfig)
    functions: _FunctionConfig = field(default_factory=_FunctionConfig)
    classes: _ClassConfig = field(default_factory=_ClassConfig)
    imports: _ImportConfig = field(default_factory=_ImportConfig)
    style: _StyleConfig = field(default_factory=_StyleConfig)
    control_flow: _ControlFlowConfig = field(default_factory=_ControlFlowConfig)

    @classmethod
    def from_options(cls, options: dict[str, object]) -> "Config":
        """Build configuration from flat CLI/test options."""
        return cls(
            size=_SizeConfig(
                max_sloc=optional_int(options["max_sloc"]),
                max_func_sloc=optional_int(options["max_func_sloc"]),
                max_class_sloc=optional_int(options["max_class_sloc"]),
                max_method_sloc=optional_int(options["max_method_sloc"]),
            ),
            counts=_CountConfig(
                max_constructs=optional_int(options["max_constructs"]),
                max_classes=optional_int(options["max_classes"]),
                max_funcs=optional_int(options["max_funcs"]),
                max_methods=optional_int(options["max_methods"]),
                max_class_members=optional_int(options["max_class_members"]),
                max_local_helpers=optional_int(options["max_local_helpers"]),
            ),
            functions=_FunctionConfig(
                max_args=optional_int(options["max_args"]),
                max_bool_args=optional_int(options["max_bool_args"]),
                require_function_doc=bool(options["require_function_doc"]),
                require_type_hint=bool(options["require_type_hint"]),
                require_kw_only_defaults=bool(options["require_kw_only_defaults"]),
                max_function_nesting_depth=optional_int(
                    options["max_function_nesting_depth"]
                ),
            ),
            classes=_ClassConfig(
                require_class_member_hint=bool(options["require_class_member_hint"]),
                require_class_doc=bool(options["require_class_doc"]),
            ),
            imports=_ImportConfig(
                banned_imports=tuple(
                    item
                    for item in (
                        options["banned_imports"]
                        if isinstance(options["banned_imports"], Iterable)
                        else ()
                    )
                    if isinstance(item, str)
                ),
                require_top_level_import=bool(options["require_top_level_import"]),
                ban_future_import=bool(options["ban_future_import"]),
                ban_typing_alias=bool(options["ban_typing_alias"]),
            ),
            style=_StyleConfig(
                ban_mutable_global=bool(options["ban_mutable_global"]),
                ban_pass_only_except=bool(options["ban_pass_only_except"]),
                ban_output_construct=bool(options["ban_output_construct"]),
                ban_placeholder_comment=bool(options["ban_placeholder_comment"]),
                ban_placeholder_pass=bool(options["ban_placeholder_pass"]),
                ban_notimplemented_placeholder=bool(
                    options["ban_notimplemented_placeholder"]
                ),
            ),
            control_flow=_ControlFlowConfig(
                max_elifs=optional_int(options["max_elifs"]),
                max_nested_ifs=optional_int(options["max_nested_ifs"]),
            ),
        )

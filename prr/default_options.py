"""Default CLI option values."""

from prr.config import Config


def default_options() -> dict[str, object]:
    """Return flat default options used by the CLI and tests."""
    config = Config()
    return {
        "max_sloc": config.size.max_sloc,
        "max_func_sloc": config.size.max_func_sloc,
        "max_class_sloc": config.size.max_class_sloc,
        "max_method_sloc": config.size.max_method_sloc,
        "max_constructs": config.counts.max_constructs,
        "max_classes": config.counts.max_classes,
        "max_funcs": config.counts.max_funcs,
        "max_methods": config.counts.max_methods,
        "max_class_members": config.counts.max_class_members,
        "max_local_helpers": config.counts.max_local_helpers,
        "max_args": config.functions.max_args,
        "max_bool_args": config.functions.max_bool_args,
        "require_function_doc": config.functions.require_function_doc,
        "require_type_hint": config.functions.require_type_hint,
        "require_kw_only_defaults": config.functions.require_kw_only_defaults,
        "max_function_nesting_depth": config.functions.max_function_nesting_depth,
        "require_class_member_hint": config.classes.require_class_member_hint,
        "require_class_doc": config.classes.require_class_doc,
        "banned_imports": config.imports.banned_imports,
        "require_top_level_import": config.imports.require_top_level_import,
        "ban_future_import": config.imports.ban_future_import,
        "ban_typing_alias": config.imports.ban_typing_alias,
        "ban_mutable_global": config.style.ban_mutable_global,
        "ban_pass_only_except": config.style.ban_pass_only_except,
        "ban_output_construct": config.style.ban_output_construct,
        "ban_placeholder_comment": config.style.ban_placeholder_comment,
        "ban_placeholder_pass": config.style.ban_placeholder_pass,
        "ban_notimplemented_placeholder": config.style.ban_notimplemented_placeholder,
        "max_elifs": config.control_flow.max_elifs,
        "max_nested_ifs": config.control_flow.max_nested_ifs,
    }

# py-review-rules - Python pre-commit rules

`py-review-rules` is a small Python package of command-line hooks for enforcing
project-specific code review rules before changes are committed.

Highly opinionated, but it aims quality code production by AI: enforcing modularity,
limits source code lines, number of constructs (functions, classes) in a file, etc.,
therefore the coding agent gets direct feedback at commit time.

The package currently provides hooks that:

- limit source lines of code for functions, classes, and files
- reject deeply nested function definitions
- ban selected Python constructs, such as specific imports or API calls
- limit the number of public top-level functions or classes in each file
- enforce function/class size, argument, member, docstring, and import placement
  policies from one command

The hooks are designed to be configurable from the command line and suitable for
use with pre-commit or similar local quality gates. They focus on lightweight
structural checks that complement linters: keeping modules small, discouraging
hard-to-review nesting, and blocking imports or APIs that a project has
decided not to allow.

## Unified Command

The preferred interface is one `py-review-rules check` command. The defaults are
intentionally strict, so a pre-commit hook can use the checks directly and
override only the constraints a project wants to tune:

```yaml
- repo: local
  hooks:
    - id: py-review-rules
      name: py-review-rules
      entry: uv run py-review-rules check
      language: system
      types: [python]
      args:
        - --max-sloc=1000
        - --max-func-sloc=500
        - --max-class-sloc=1000
        - --max-method-sloc=300
        - --max-function-nesting-depth=2
        - --max-constructs=1
        - --max-classes=1
        - --max-funcs=1
        - --max-local-helpers=2
        - --banned-import=osgeo, pyyaml->ruamel.yaml, pyaml->ruamel.yaml
        - --max-args=6
        - --max-methods=10
        - --max-class-members=10
        - --require-class-member-hint
        - --require-class-doc
        - --require-function-doc
        - --require-top-level-import
        - --ban-future-import
        - --require-type-hint
        - --ban-typing-alias
        - --ban-mutable-global
        - --ban-pass-only-except
        - --ban-output-construct
        - --ban-placeholder-comment
        - --ban-placeholder-pass
        - --ban-notimplemented-placeholder
        - --max-bool-args=1
        - --require-kw-only-defaults
        - --max-elifs=2
        - --max-nested-ifs=2
```

Pre-commit does not pass arbitrary hook keys such as `max-sloc: 1000` to hook
executables, so project-specific settings must be written under `args`.

Supported rules:

- `--max-sloc`: maximum source lines of code in a file, default `800`
- `--max-func-sloc`: maximum SLOC in a function, default `500`
- `--max-class-sloc`: maximum SLOC in a class, default `800`
- `--max-method-sloc`: maximum SLOC in a class method, default `300`
- `--max-function-nesting-depth`: maximum nested function definition depth,
  default `2`
- `--max-constructs`: maximum public top-level classes and functions in a file,
  default `1`
- `--max-classes`: maximum public top-level classes in a file, default `1`
- `--max-funcs`: maximum public top-level functions in a file, default `1`
- `--max-local-helpers`: maximum private top-level helper functions in a file,
  default `2`
- `--banned-import`: banned import name, optionally with an alternative
- `--max-args`: maximum function or method parameters, including `*args` and
  `**kwargs`, default `6`
- `--max-methods`: maximum methods in a class, default `10`
- `--max-class-members`: maximum annotated class member variables, default `10`
- `--require-class-member-hint`: forbid assigning `self.member` unless the
  member is declared as a class-level annotation, default enabled
- `--require-class-doc`: require class docstrings and `:ivar name:` entries for
  each annotated member variable, default enabled
- `--require-function-doc`: require docstrings on public functions and methods,
  default enabled
- `--require-top-level-import`: require imports to appear directly at module top
  level, default enabled
- `--ban-future-import`: ban `from __future__ import annotations`, default
  enabled
- `--require-type-hint`: require type hints on function parameters, return
  values, and class member assignments, default enabled. `*args` and `**kwargs`
  are ignored.
- `--ban-typing-alias`: ban `typing.List`, `typing.Dict`, `typing.Optional`,
  and `typing.Union` imports/usages, default enabled
- `--ban-mutable-global`: ban module-level mutable values such as `[]`, `{}`,
  `set()`, and `dict()`, default enabled
- `--ban-pass-only-except`: ban exception handlers whose body is only `pass`,
  default enabled
- `--ban-output-construct`: ban `print` and `click.echo`, default enabled. Use
  `sys.stdout.write` for pipeable data and `loguru` for non-pipe output.
- `--ban-placeholder-comment`: ban placeholder comments such as `TODO`,
  `FIXME`, `XXX`, `HACK`, and `placeholder`, default enabled
- `--ban-placeholder-pass`: ban `pass` as placeholder code, default enabled
- `--ban-notimplemented-placeholder`: ban vague `NotImplementedError`
  placeholders, default enabled. Intentional abstract/interface contracts are
  allowed when the message says so.
- `--max-bool-args`: maximum boolean parameters, default `1`
- `--require-kw-only-defaults`: require every parameter with a default value to
  be keyword-only, default enabled
- `--max-elifs`: maximum `elif` branches in one `if` chain, default `2`
- `--max-nested-ifs`: maximum nested non-`elif` `if` depth, default `2`

Banned imports can be written as `--banned-import=pyyaml`, or with an
alternative as `--banned-import=pyyaml=ruamel.yaml`. The form
`--banned-import=pyyaml->ruamel.yaml` is also accepted. Multiple banned imports
can be passed by repeating the option or as a comma-separated list.

See `examples/pre-commit-config.yaml` for a complete local pre-commit
configuration that demonstrates every rule.

## Exemptions

Rules can be exempted with `# noqa` comments. A bare `# noqa` exempts the
definition or module from all `py-review-rules` checks that apply there, while
rule-specific comments such as `# noqa: PCR009` exempt only the named rule. For
project files that also run Ruff, prefer `# pcr: noqa: PCR009` so Ruff does not
interpret the custom code. Public definition counting treats names that start
with `_` as local helpers for public construct limits. They are still limited by
`--max-local-helpers`; prefer moving reusable behavior into a focused public
function in its own module.

Unified rule codes:

- `PCR001`: file SLOC
- `PCR002`: function SLOC
- `PCR003`: class SLOC
- `PCR004`: method SLOC
- `PCR005`: public constructs per file
- `PCR006`: public classes per file
- `PCR007`: public functions per file
- `PCR008`: banned imports
- `PCR009`: function or method parameters
- `PCR010`: class methods
- `PCR011`: undeclared class member assignments
- `PCR012`: class member variables
- `PCR013`: class docstrings and member documentation
- `PCR014`: function docstrings
- `PCR015`: non-top-level imports
- `PCR016`: banned future annotations import
- `PCR017`: missing type hints
- `PCR018`: banned `typing` aliases
- `PCR019`: module-level mutable values
- `PCR020`: pass-only exception handlers
- `PCR021`: banned output constructs
- `PCR022`: placeholder comments
- `PCR023`: placeholder `pass`
- `PCR024`: placeholder `NotImplementedError`
- `PCR025`: boolean parameters
- `PCR026`: positional parameters with defaults
- `PCR027`: too many `elif` branches
- `PCR028`: nested `if` depth
- `PCR029`: nested function depth
- `PCR030`: local helper functions per file

## Ruff Equivalents

`py-review-rules` intentionally focuses on project-shaping rules that are either
absent from Ruff or more specific than Ruff's general complexity checks. Keep
using Ruff for broad complexity and size metrics when it already has the rule:

- `C901`: McCabe complexity
- `PLR0911`: too many returns
- `PLR0912`: too many branches
- `PLR0913`: too many arguments
- `PLR0914`: too many local variables
- `PLR0915`: too many statements
- `PLR0916`: too many boolean expressions
- `PLR0917`: too many positional arguments

Configure those thresholds in `pyproject.toml`:

```toml
[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.pylint]
max-args = 6
max-returns = 6
max-branches = 10
max-locals = 12
max-statements = 40
max-positional-args = 3
```

Use `py-review-rules` for the stricter architectural choices Ruff does not
express directly, such as `--require-kw-only-defaults`, `--max-bool-args`,
`--max-elifs`, `--max-nested-ifs`, `--max-function-nesting-depth`, and
`--max-local-helpers`.

"""Documented class member parsing."""


def documented_members(docstring: str) -> set[str]:
    """Return class members documented with ``:ivar name:`` lines."""
    members: set[str] = set()
    for line in docstring.splitlines():
        stripped = line.strip()
        if stripped.startswith(":ivar "):
            member, _, _ = stripped.removeprefix(":ivar ").partition(":")
            members.add(member.strip())
    return members

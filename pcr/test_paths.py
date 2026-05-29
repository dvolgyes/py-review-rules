"""Test path detection."""


def is_test_file(filepath: str) -> bool:
    """Return whether a path should use test-file count exemptions."""
    path_parts = filepath.replace("\\", "/").split("/")
    return "tests" in path_parts or path_parts[-1].startswith("test_")

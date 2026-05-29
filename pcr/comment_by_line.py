"""Python comment extraction."""

import io
import tokenize


def comment_by_line(source_lines: list[str]) -> dict[int, list[str]]:
    """Return Python comments keyed by 1-based source line."""
    source = "\n".join(source_lines)
    if source_lines:
        source += "\n"

    comments: dict[int, list[str]] = {}
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                comments.setdefault(token.start[0], []).append(token.string)
    except tokenize.TokenError:
        return comments

    return comments

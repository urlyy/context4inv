"""Format generated checker artifacts in the current Python environment."""

from pathlib import Path

import black


def format_py(code_file: str | Path) -> str | None:
    """Return a syntax diagnostic, or format valid source in place and return None."""
    path = Path(code_file)
    source = path.read_text(encoding="utf-8")
    try:
        formatted = black.format_file_contents(source, fast=True, mode=black.FileMode())
    except black.NothingChanged:
        return None
    except black.InvalidInput as error:
        return str(error)
    path.write_text(formatted, encoding="utf-8")
    return None

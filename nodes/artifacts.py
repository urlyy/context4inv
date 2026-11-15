"""Artifact paths are pure; creation happens explicitly at loop initialization."""

from pathlib import Path


def function_directory(config, function_name: str) -> Path:
    return Path(config["configurable"]["output_dir"]) / f"FUNC_{function_name}"


def loop_directory(config, function_name: str, loop_index: int) -> Path:
    return function_directory(config, function_name) / f"LOOP_{loop_index}"


def loop_source_path(config, function_name: str, loop_index: int) -> Path:
    return loop_directory(config, function_name, loop_index) / "tmp_code.c"


def invariant_template_path(config, function_name: str, loop_index: int) -> Path:
    return loop_directory(config, function_name, loop_index) / "z3_template_pre.py"


def postcondition_template_path(config, function_name: str, loop_index: int) -> Path:
    return loop_directory(config, function_name, loop_index) / "z3_template_post.py"


def verification_directory(config, function_name: str, loop_index: int) -> Path:
    return loop_directory(config, function_name, loop_index) / "verify"


def error_log_path(config, function_name: str, loop_index: int) -> Path:
    return loop_directory(config, function_name, loop_index) / "err.log"


def create_loop_artifacts(
    config, function_name: str, loop_index: int, *, has_postcondition: bool
) -> None:
    """Create a new loop directory, its diagnostics, and its verification workspace."""
    loop_directory(config, function_name, loop_index).mkdir()
    verification_directory(config, function_name, loop_index).mkdir()
    loop_source_path(config, function_name, loop_index).touch()
    invariant_template_path(config, function_name, loop_index).touch()
    error_log_path(config, function_name, loop_index).touch()
    if has_postcondition:
        postcondition_template_path(config, function_name, loop_index).touch()

"""Interpret experiment modes without coupling stages to CLI argument parsing."""

from dataclasses import dataclass

EXPERIMENT_MODES = ("full", "task12_only", "no_iterative", "no_task4_pre_enhance")


@dataclass(frozen=True)
class ExperimentOptions:
    """Mode switches shared by every stage; retry_limit also bounds API attempts."""

    mode: str
    retry_limit: int
    per_variable_enabled: bool
    combined_enabled: bool
    joint_enabled: bool
    fixed_point_enabled: bool
    strengthening_enabled: bool


def read_experiment_options(config) -> ExperimentOptions:
    experiment = (config or {}).get("configurable", {}).get("experiment", {})
    mode = experiment.get("mode", "full")
    if mode not in EXPERIMENT_MODES:
        raise ValueError(f"Unknown experiment mode: {mode}")
    retry_limit = int(experiment.get("llm_retry_limit", 5))
    if retry_limit < 1:
        raise ValueError("llm_retry_limit must be at least 1")
    joint_only = mode == "task12_only"
    return ExperimentOptions(
        mode=mode,
        retry_limit=retry_limit,
        per_variable_enabled=not joint_only,
        combined_enabled=not joint_only,
        joint_enabled=joint_only,
        fixed_point_enabled=mode != "no_iterative",
        strengthening_enabled=experiment.get(
            "enable_task4_pre_enhance", mode != "no_task4_pre_enhance"
        ),
    )

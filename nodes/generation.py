"""Request candidates and save the stage conversation at every request boundary."""

from nodes.artifacts import loop_directory
from nodes.config import read_experiment_options
from utils.llm import request_candidates

STAGE_LOG_FILES = {
    "per_variable": "run_per_variable.log",
    "combined": "run_combined.log",
    "joint": "run_joint.log",
    "postcondition": "run_postcondition.log",
    "strengthening": "run_strengthening.log",
}


def request_stage_candidates(state, config, stage_name, messages, **response_format):
    folder = loop_directory(config, state["function"]["name"], state["loop"]["index"])
    return request_candidates(
        config["configurable"]["llm"],
        messages,
        state[stage_name]["messages"],
        read_experiment_options(config).retry_limit,
        transcript_path=folder / STAGE_LOG_FILES[stage_name],
        **response_format,
    )

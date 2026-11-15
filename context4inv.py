"""Command-line entry point for context4inv's loop invariant workflow."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from langgraph.graph import StateGraph

from nodes.config import EXPERIMENT_MODES, read_experiment_options
from nodes.program import build_program_workflow
from nodes.state import WorkflowState
from utils.llm import create_llm


def build_workflow():
    """Connect program traversal to function, loop and invariant stages."""
    workflow = StateGraph(WorkflowState)
    last_node = build_program_workflow("__start__", workflow)
    workflow.add_edge(last_node, "__end__")
    return workflow.compile()


def _run_configuration(code_path, model, output_directory, mode, retry_limit):
    configuration = {
        "configurable": {
            "code_path": str(code_path),
            "llm": model,
            "output_dir": str(output_directory),
            "experiment": {"mode": mode, "llm_retry_limit": retry_limit},
        },
        "recursion_limit": 1000,
    }
    read_experiment_options(configuration)
    return configuration


def _write_invariant_summary(state: WorkflowState, output_directory: Path) -> None:
    summary = {
        function_name: [sorted(invariants) for invariants in loops]
        for function_name, loops in state["program"]["function_invariants"].items()
    }
    (output_directory / "invariants.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def run(code_path, llm, output_dir, *, mode="full", llm_retry_limit=5) -> WorkflowState:
    """Verify one C file using an injected model and a new artifact directory."""
    code_path = Path(code_path).resolve(strict=True)
    if not code_path.is_file():
        raise ValueError(f"Expected a C source file: {code_path}")
    output_directory = Path(output_dir).resolve()
    configuration = _run_configuration(
        code_path, llm, output_directory, mode, llm_retry_limit
    )
    output_directory.mkdir(parents=True)
    workflow = build_workflow()
    (output_directory / "workflow.mmd").write_text(
        workflow.get_graph().draw_mermaid(), encoding="utf-8"
    )
    state = workflow.invoke({}, configuration)
    _write_invariant_summary(state, output_directory)
    return state


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def build_parser():
    parser = argparse.ArgumentParser(
        description="Generate and verify C loop invariants."
    )
    parser.add_argument("--path", type=Path, required=True, help="Input C source file")
    parser.add_argument("--mode", choices=EXPERIMENT_MODES, default="full")
    parser.add_argument(
        "--llm-retry-limit",
        type=positive_int,
        default=5,
        help="Maximum request attempts and model generation rounds per task",
    )
    parser.add_argument(
        "--provider", choices=("deepseek", "openai", "qwen", "zhipu", "fma")
    )
    parser.add_argument("--model", help="Override the provider's default model")
    parser.add_argument(
        "--base-url", help="Override the OpenAI-compatible API endpoint"
    )
    parser.add_argument(
        "--output-dir", type=Path, help="New directory for this run's artifacts"
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        code_path = args.path.resolve(strict=True)
        llm = create_llm(args.provider, model=args.model, base_url=args.base_url)
        output_dir = args.output_dir or (
            Path("output")
            / code_path.stem
            / datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        )
        run(
            code_path,
            llm,
            output_dir,
            mode=args.mode,
            llm_retry_limit=args.llm_retry_limit,
        )
        print(f"Results: {output_dir.resolve()}")
    except TimeoutError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

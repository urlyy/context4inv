# context4inv

`context4inv` is an experimental project for generating and verifying loop invariants for C programs. It uses Tree-sitter to parse C source code, LangGraph to organize a multi-stage analysis workflow, and a combination of large language models and the Z3 SMT solver to generate candidate invariants, check counterexamples, iteratively refine results, and produce logs, Z3 verification scripts, and invariant outputs for each function and loop.

## Project Overview

The main entry point is `neo_main.py`. During execution, the system reads a C source file and processes it through the following workflow:

1. Parse the C program and build the function call graph and inverted call graph.
2. Traverse the program function by function, identifying loops, branches, assignments, array accesses, and `assume` / `assert` annotations.
3. Generate Z3 verification templates for each loop.
4. Use an LLM to generate candidate loop invariants.
5. Use Z3 to check initialization, preservation, and postcondition-related properties.
6. When verification fails, feed counterexamples back to the LLM for refinement.
7. Write logs, candidate invariants, final results, and verification scripts to the experiment output directory.

The codebase is organized into several analysis layers:

- `nodes/global_level/`: builds the global function call graph.
- `nodes/func_level/`: parses functions, locates loop paths, and identifies key variables.
- `nodes/loop_level/`: coordinates loop-level experiments, generates verification templates, and merges results.
- `nodes/task1/`, `nodes/task2/`, `nodes/task12/`, `nodes/task3/`, `nodes/task4/`: implement different invariant-generation, counterexample-feedback, and SMT-verification strategies.
- `utils/cparser/`: Tree-sitter-based C parsing support.
- `utils/solve_smt/`: converts the intermediate representation into Z3 verification code.
- `utils/*/`: wrappers for different LLM backends, such as DeepSeek, Qwen, OpenAI, Zhipu, and others.
- `prompt_templates/`: prompt templates used by the LLM workflow.

## Dataset Description

This repository does not include a full benchmark dataset. The experiment input is a single C source file, and a dataset can be organized as a collection of `.c` files, such as loop-verification benchmarks, manually written test cases, or C programs collected from other projects.

Each sample should preferably follow these conventions:

- The file extension is `.c`.
- The program contains C function definitions that can be parsed by the project.
- Loops may be written as `while`, `for`, or `do while` loops.
- Special comments can be used to express preconditions and postconditions:
  - `//@ assume(...)`: path assumptions or input constraints.
  - `//@ assert(...)`: target properties to be verified.
- Expressions should stay within the integer, array, comparison, and logical operations currently supported by the parser and Z3 conversion logic.

A minimal example:

```c
void example(int n) {
    int i = 0;
    //@ assume(n >= 0)
    while (i < n) {
        i = i + 1;
    }
    //@ assert(i == n)
}
```

For batch experiments, place multiple C files in the same directory, for example:

```text
benchmarks/
  001.c
  002.c
  003.c
```

Then call `neo_main.py --path <file>` for each file. The current entry script is designed for single-file execution, so batch scheduling should be handled by an external script.

## Environment Setup

Python 3.10 or newer is recommended. Install dependencies inside a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Main dependencies include:

- `tree-sitter`: parses C source code.
- `langgraph`: organizes the multi-node agent workflow.
- `langchain-core`, `langchain-community`: provide message and LLM invocation interfaces.
- `langchain_deepseek`: the default DeepSeek backend.
- `z3-solver`: SMT verification.
- `black`, `pyparsing`: formatting and expression-parsing utilities.

## LLM Configuration

By default, `neo_main.py` uses:

```python
from utils.ds import llm
```

The corresponding configuration file is `utils/ds/__init__.py`. Before running experiments, configure a valid API key there:

```python
token = "sk-..."
```

You can also switch to another backend. `neo_main.py` already contains several candidate imports:

```python
# from utils.zhipu import llm
# from utils.qwen import llm
from utils.ds import llm
# from utils.openai import llm
# from utils.ollama import llm
```

To switch models, comment out the current import and enable the target backend. Also make sure the corresponding `utils/<backend>/__init__.py` file has the correct API key, model name, and service endpoint settings.

## Starting an Experiment

After preparing a C file, run the following command from the project root:

```bash
python neo_main.py --path /path/to/example.c
```

Windows example:

```powershell
python .\neo_main.py --path E:\benchmarks\001.c
```

You can also set the LLM retry limit:

```bash
python neo_main.py --path /path/to/example.c --llm-retry-limit 5
```

Note: the current `main()` function sets the experiment configuration internally as follows:

```python
experiment_mode = "full"
llm_retry_limit = 6
```

For ablation experiments, edit `experiment_mode` in `neo_main.py`. The code comments list the following available modes:

- `full`: runs the full workflow.
- `task12_only`: uses only the task12-related workflow.
- `no_iterative`: disables iterative counterexample feedback.
- `no_task4_pre_enhance`: a reserved experiment-mode name; verify that the current node logic fully supports it before use.

## Experiment Outputs

For an input file:

```text
/path/to/example.c
```

The program creates an output directory next to the input file:

```text
/path/to/LOG_example/
```

The output directory is organized by function and loop:

```text
LOG_example/
  FUNC_<function_name>/
    LOOP_<loop_id>/
      loop_code.txt
      z3_template_pre.py
      z3_template_post.py
      inv.json
      post_inv.json
      task12.log
      each.log
      combined.log
      post.log
      err.log
      verify/
```

Common output files:

- `loop_code.txt`: code snippet and context for the current loop.
- `z3_template_pre.py`: Z3 template for precondition-related verification tasks.
- `z3_template_post.py`: Z3 template for postcondition-related verification tasks.
- `inv.json`: loop invariant results.
- `post_inv.json`: invariant results related to postcondition enhancement.
- `*.log`: LLM conversations, candidate generation logs, and counterexample-feedback logs.
- `err.log`: errors from parsing, formatting, or SMT solving.
- `verify/`: generated verification scripts after filling templates.

In addition, the workflow initialization step generates the following file in the current working directory:

```text
igent.mmd
```

This file contains a Mermaid graph of the LangGraph workflow and can be used to inspect node connections.

## Batch Running

If a dataset contains multiple `.c` files, use a simple script to run them one by one:

```bash
for file in benchmarks/*.c; do
  python neo_main.py --path "$file"
done
```

Windows PowerShell:

```powershell
Get-ChildItem E:\benchmarks -Filter *.c | ForEach-Object {
    python .\neo_main.py --path $_.FullName
}
```

Each sample produces its own `LOG_<filename>/` directory. You can later collect and summarize `inv.json`, `post_inv.json`, and `err.log` across all runs.

## Notes

- The project deletes and recreates the matching `LOG_<filename>/` output directory at the start of each run. Back up important logs before rerunning an experiment.
- Function calls in the input C file must have corresponding declarations or definitions; otherwise, the global call-graph check may fail.
- Complex pointer usage, complex structs, macro expansion, and some C syntax may be outside the current parser and verifier support.
- LLM calls may incur cost and depend on network availability, API keys, model rate limits, and service stability.
- To reduce debug output, set the environment variable `DPRINT_ENABLED=0` before running.

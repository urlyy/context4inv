import traceback
import argparse

from common import dprint

# from utils.zhipu import llm
# from utils.qwen import llm
from utils.ds import llm
# from utils.qwenfma import llm
# from utils.openai import llm
# from utils.ollama import llm

from nodes.common import (
    AgentState, StateGraph,
)
from nodes.global_level import add_edge
from nodes.func_level import entry_node, next_func

def init_agent():
    workflow = StateGraph(AgentState)
    last_node = add_edge("__start__", workflow)
    workflow.add_edge(last_node, "__end__")
    agent = workflow.compile()
    mermaid = agent.get_graph().draw_mermaid()
    output_path = "igent.mmd"
    with open(output_path, "w") as f:
        f.write(mermaid)
    return agent

def main(args):
    import os
    from pathlib import Path
    import shutil
    
    code_path = args.path
    # create output dir
    p = Path(code_path)
    output_dir = os.path.join(p.parent, f"LOG_{p.stem}")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    # set init_data
    initial_state = {
        "global_data":{
            
        }
    }
    agent = init_agent()
    # 实验模式字符串："full" / "task12_only" / "no_iterative" / "no_task4_pre_enhance"
    experiment_mode = "full"
    llm_retry_limit = 6
    experiment = {
        "mode": experiment_mode,
        "llm_retry_limit": llm_retry_limit,
    }
    # 不可变的全局数据
    config = {
        "configurable": {
            "thread_id": "1",
            "code_path": args.path,
            "llm": llm,
            "output_dir": output_dir,
            "experiment": experiment,
        },
        "recursion_limit": 1000,
    }
    try:
        # res = agent.invoke(initial_state, config)
        # res_dict = dict(res)
        for output in agent.stream(initial_state, config):
            for node_name, value_updated in output.items():
                print("-" * 30, node_name, "-" * 30)
    except Exception as e:
        raise e

if __name__ == "__main__":
    import sys
    code_paths = [
        # "/home/urlyy/workspace/my_benchmark/LaM4Inv/253/253.c",
        # "/home/urlyy/workspace/igent_xiaorong/test/77.c",
        "/home/urlyy/workspace/igent_xiaorong/test/253_new.c",
    ]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--path",
        type=str,
        default=code_paths[0],
    )
    parser.add_argument(
        "--llm-retry-limit",
        type=int,
        default=5,
        help="Global retry limit for all LLM ask nodes (excluding format/parse errors).",
    )
    args = parser.parse_args()
    try:
        main(args)
    except TimeoutError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)  # 通知外部程序这是超时退出
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)  # 通知外部程序这是错误退出
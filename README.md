# context4inv

为 C 程序生成并验证循环不变式的实验工具。Tree-sitter 将受支持的 C 语句转换为 IR，LangGraph 编排候选生成与反例反馈，Z3 验证初始化、保持性及后置断言。

## 安装与运行

要求 Python 3.12 及以上；当前在 Windows、Python 3.13.5 下验证。C 语法包使用预编译 wheel，无需本地 C 编译器。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
```

`requirements.txt` 声明直接依赖，`requirements.lock` 固定完整依赖及下载校验值。开发时可以用 `pip install -e .` 安装命令行入口；本地 FMA 模型的额外依赖通过 `pip install -e '.[local]'` 安装。

默认使用 DeepSeek，通过环境变量配置 key：

```powershell
$env:DEEPSEEK_API_KEY = '<DeepSeek API key>'
.\.venv\Scripts\python.exe .\context4inv.py --path .\examples\branch.c
```

模型配置集中在 `utils/llm.py`，仅在实际运行时创建模型，导入模块或查看帮助不需要 key。

| `--provider` | key 环境变量 | 默认模型 |
| --- | --- | --- |
| `deepseek`（默认） | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| `openai` | `OPENAI_API_KEY` | `gpt-4.1-mini` |
| `qwen` | `DASHSCOPE_API_KEY` | `qwen-plus` |
| `zhipu` | `ZHIPUAI_API_KEY` | `glm-4-flash` |
| `fma` | 无；需安装 local 额外依赖 | `fm-universe/qwen2.5-7b-fma` |

在线服务统一通过 OpenAI 兼容接口调用，可用 `--model`、`--base-url` 覆盖默认值。环境变量 `CONTEXT4INV_PROVIDER`、`CONTEXT4INV_MODEL`、`CONTEXT4INV_BASE_URL` 也可配置；命令行参数优先。本地 FMA 模型仅在选中该 provider 时加载。

```powershell
.\.venv\Scripts\python.exe .\context4inv.py --help
.\.venv\Scripts\python.exe .\context4inv.py --path .\examples\implication.c --mode task12_only --llm-retry-limit 3
.\.venv\Scripts\python.exe .\context4inv.py --path .\examples\nested_loops.c --provider deepseek --model deepseek-reasoner
```

## 工作流程与实验模式

程序按被调用者优先的顺序访问已定义函数，逐函数隔离状态，并按从内到外的顺序处理嵌套循环。

- `per_variable` 按修改变量生成候选，`combined` 生成变量间关系的候选；两条分支并行执行。
- `joint` 一次生成混合候选，可作为前两条生成分支的替代。
- 候选经过初始化与保持性检查，再由 `postcondition` 验证其合取是否足以证明后置断言。
- 验证失败时，模型收到具体反例或 Z3 的 `unknown` 原因。必要时，`strengthening` 增强前序循环，并重新验证受影响循环。

| `--mode` | 行为 |
| --- | --- |
| `full` | 按变量生成 + 关系式生成、反例反馈、后置验证和前序循环增强 |
| `task12_only` | 使用一次性混合候选生成，保留后续验证 |
| `no_iterative` | 关闭本地候选固定点迭代，保留模型反例反馈 |
| `no_task4_pre_enhance` | 关闭前序循环增强，后置条件无法证明时报告失败 |

`--llm-retry-limit` 控制每次请求的最大尝试次数，以及每个阶段的模型生成轮数上限；初次候选生成计一轮。后置验证阶段先检查已有不变式，再按此上限追加生成。API 异常、JSON 格式错误和结构错误都会消耗请求次数。

## 输入与语义范围

用特殊注释标记假设与目标断言：

```c
void example(int n) {
    int i = 0;
    //@ assume(n >= 0)
    while (i < n) {
        i++;
    }
    //@ assert(i == n)
}
```

支持整数/实数表达式、数组读写、声明与初始化、复合赋值、自增自减、`if/else`、`while/for`、嵌套循环，以及循环结束到断言之间的赋值。多个紧邻断言按合取验证。不变式支持逻辑运算、量词及 `old(expr)`；`old(expr)` 指目标循环完成初始化、第一次检查条件之前的值，内外层循环各自有独立入口快照。

验证采用数学整数、实数和 Z3 数组抽象；赋值中的实数转整数按向零截断处理。不模拟 C 的有限位宽溢出、完整整数除法规则或指针别名。`do while`、`break/continue`、提前返回、变量遮蔽、复杂结构体和函数调用执行语义尚未支持，会明确报错；调用图排序不代表已实现跨函数摘要。纯粹的函数末尾 `return` 可以解析。断言须位于相应循环所在语句块中；工具检查的是断言的部分正确性，不证明循环终止。

## 输出

默认每次运行写入独立目录：`output/<输入文件名>/<时间戳>/`。可用 `--output-dir` 指定一个尚不存在的目录。重新运行不会删除已有实验结果。

```text
output/<name>/<run>/
  workflow.mmd                 # LangGraph 流程图
  invariants.json              # 按函数、循环汇总的已验证不变式
  FUNC_<function>/
    FINAL_code.c              # 标注循环不变式的函数代码
    LOOP_<id>/
      tmp_code.c
      z3_template_pre.py
      z3_template_post.py      # 存在后置断言时生成
      invariants_pre.json
      invariants_post.json
      run_*.log
      err.log
      verify/                 # 每轮候选的实际 Z3 检查脚本及反例
```

模型会看到完整循环源码及已验证内循环的局部不变式，保留初始化与更新。反例反馈包括逐个候选被拒的原因、失败阶段及入口快照值，避免只看到整体断言失败。每次模型请求和响应都会及时保存到对应 `run_*.log`，中途失败也能排查。非法或类型不匹配的候选会单独剔除并记入 `err.log`，Z3 的反例、`unknown`、检查脚本执行错误和超时分别处理。需要调试输出时设置 `DPRINT_ENABLED=1`；位置标注可通过 `DPRINT_LOCATION=1` 开启。

## 阅读代码

建议先读 `context4inv.py` 的 `run()`，再依次查看 `program/workflow.py`、`functions/workflow.py`、`loops/workflow.py`。各生成阶段均用 `generate_candidates.py`、`refine_candidates.py`、`verify_candidates.py` 表达生成、反馈修正、验证三个职责；`workflow.py` 明确连接这些步骤，包入口只导出流程构建函数。

```text
context4inv.py               命令行与单文件运行入口
nodes/
  ir.py                     C 语句的中间表示
  state.py                  程序、函数、循环及各阶段状态
  config.py                 实验模式与重试选项
  artifacts.py              输出路径与显式目录初始化
  source_rendering.py       保留源码语义的循环标注
  formulas.py               不变式合取与检查器表达式编译
  generation.py             模型请求上下文与会话日志
  verification.py           候选验证和固定点迭代
  feedback.py               被拒候选、失败阶段与反例格式化
  program/                  调用图与函数调度
  functions/                C → IR、修改变量和循环路径
  loops/                    循环调度、验证模板和结果合并
  per_variable/             按变量生成候选
  combined/                 生成变量间关系的候选
  joint/                    一次生成混合候选
  postcondition/            证明后置断言并补充候选
  strengthening/            增强前序循环并重验受影响循环
utils/
  c_parser.py               Tree-sitter C 与源码词法辅助
  c_types.py                受支持的标量及数组类型约定
  debug.py                  可选调试输出
  expr_parser/
    ast.py                  表达式的数据结构
    parser.py               C 表达式与逻辑公式的语法
    rendering.py            AST → Z3 表达式
  fol_parser/               一阶逻辑及带作用域的 old(expr) 解析
  smt/
    models.py               具名验证输入、SSA 快照和求解结果
    encoding.py             IR → SSA 约束
    codegen.py              初始化、保持性、后置断言义务
    checker_template.py     独立 Z3 检查脚本
    runner.py               子进程执行与结果分类
  llm.py                    模型配置、响应校验和有限重试
  local_model.py            可选本地模型适配器
prompt_templates/           按生成阶段命名的提示词
examples/                   小型输入样例与来源说明
```

`WorkflowState` 按 `program`、`function`、`loop` 和各生成阶段划分数据，节点返回自己更新的部分。`LoopStateMaps` 明确区分入口、迭代前、迭代后和循环出口的 SSA 符号；`SolverResult`、`ProofFailure`、`CandidateRejection` 用具名字段传递结果与反例。

固定点验证会利用已经接受的不变式重新检查未决候选，直到没有新增结果。`unknown` 表示求解未得出结论，语法或类型错误表示候选无效；它们均不视为已证明或真实反例。
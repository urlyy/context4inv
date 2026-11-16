# context4inv

context4inv 是一个为 C 程序自动生成并验证循环不变式的实验工具。它使用大语言模型生成候选不变式，通过 Z3 检查初始化、保持性和循环后的断言，并利用反例反馈修正候选。

支持 `while`、`for`、条件分支、嵌套循环和数组读写。不变式可以使用逻辑运算、量词以及表示循环入口值的 `old(...)`。验证采用数学整数、实数和数组抽象，不模拟有限位宽溢出、完整的 C 整数除法规则或指针别名，也不证明循环终止。输入须不含预处理指令；尚未支持的语法会报错。

## 依赖安装

需要 Python 3.12 及以上。以下命令在项目根目录执行，以 Windows PowerShell 为例：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
```

Linux/macOS 使用 `.venv/bin/python` 替换上述 Python 路径。`requirements.lock` 固定完整依赖版本，`requirements.txt` 列出直接依赖；C 语法解析使用预编译包，无需本地 C 编译器。

## 使用示例

[`examples/demo.c`](examples/demo.c) 从 0 开始递增计数，目标是证明循环结束时 `i == n`：

```c
void count_to(int n) {
    int i = 0;
    //@ assume(n >= 0)
    while (i < n) {
        i++;
    }
    //@ assert(i == n)
}
```

`//@ assume(...)` 指定输入假设，`//@ assert(...)` 指定需要证明的循环后断言。每条验证注释放在独立行中，断言与对应循环位于同一个语句块。

默认使用 DeepSeek。配置 API key 后运行：

```powershell
$env:DEEPSEEK_API_KEY = '<DeepSeek API key>'
.\.venv\Scripts\python.exe .\context4inv.py --path .\examples\demo.c
```

工具会尝试生成例如 `0 <= i && i <= n` 的不变式，检查其是否成立，并验证它能否推出 `i == n`。实际候选由模型生成。

成功后，终端显示结果目录 `output/demo/<时间戳>/`。其中 `invariants.json` 汇总已验证的不变式，`FUNC_count_to/FINAL_code.c` 包含标注后的源码，各循环目录保存模型日志、Z3 检查脚本和反例。

可通过 `--model` 指定模型、`--output-dir` 指定新的输出目录；完整参数见：

```powershell
.\.venv\Scripts\python.exe .\context4inv.py --help
```

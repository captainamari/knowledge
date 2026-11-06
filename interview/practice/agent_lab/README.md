# 手写只读 Agent：可重复操作的最小练习

这是 [学习主文](../../topics/agent-from-scratch-to-personal-product.md) 的配套代码，不是生产 Agent 框架。默认不联网，不依赖第三方 Python 包，不修改 ai-research-copilot，不接触真实预约、付款、交易和个人文件。

## 1. 准备

使用 Python 3.11 或更新版本。终端进入本目录，先确认能看到 agent.py 和 test_agent.py：

```bash
python3 --version
python3 -m unittest -v
python3 agent.py --mode fake
```

Windows 可用 `py -3 --version`、`py -3 -m unittest -v`、`py -3 agent.py --mode fake`。如果 Python 命令不存在，先从 Python 官方渠道安装适合操作系统的版本，再打开新终端。代码仅用标准库，不需要 pip install，也不需要 .env 或任何 API Key。

预期测试数量为 14，最后显示 OK。预期 fake 返回 completed_unverified、read_ids 包含 copilot，trace 依次有 search、read、finish。耗时可能不同，不比较具体毫秒数。

## 2. 保存自己的第一次记录

```bash
python3 agent.py --mode fake --output first-run.json
```

输出写入当前目录。已存在同名文件会抛出 FileExistsError，使用另一个文件名，不覆盖学习证据。运行文件与 __pycache__ 是本地产物，不提交。

fake 的动作和答案是固定脚本，不会随 question 自动推理。它只证明循环可以执行，不能用它证明模型能力、任务正确率或成本优势。

## 3. 对照测试读代码

先读 validate_action，再读 execute 和 run。打开 test_agent.py，逐项看坏 JSON、未知动作、参数错误、不存在的资料、模型异常、步数上限、上下文上限、伪造引用等测试。

我可以复制一个测试，尝试修改动作，再判断应当返回何种状态。每次只改一个边界，并完整重跑测试。不要为了让测试通过，直接删掉拒绝逻辑。

结果状态：

- completed_unverified：动作循环结束，引用来自成功读取的资料；答案是否忠实仍需核验。
- model_error：模型适配器异常。trace 只记录异常类型，避免泄露可能敏感的异常正文。
- context_limit：超过字符预算。不是精确 token 限额。
- step_limit：达到最多动作次数，未拿到通过结构检查的最终答复。

CLI 对非 completed_unverified 返回非零退出码。引用来源检查不是事实检查，测试 finish_does_not_prove_truth 专门展示了这一限制。资料注入测试用的是脚本模型，也不能代替真实模型安全评估。

## 4. 可选：已有本机模型服务时再执行

```bash
python3 agent.py --mode local --model "本机实际模型名" --endpoint http://127.0.0.1:11434/v1/chat/completions --question "copilot 当前有什么能力？" --output local-run-01.json
```

前提是我自己已启动与该接口兼容的本机服务；这个示例不负责安装、下载或启动模型。端口只是默认值，以实际服务配置为准。只允许本机 HTTP，禁止外部地址、重定向与环境代理。不支持认证 Header 或云端调用。看到连接错误，应检查服务、端口、模型名和兼容格式，不能把 model_error 当作模型推理失败。

适配器要求响应为 choices[0].message.content 字符串，其中是本练习的 JSON 动作。它不是原生 tool_calls 客户端。个别模型会输出 Markdown 围栏或解释文字，当前实现会拒绝；如要改进解析，应添加测试，不能把任意文本交给 eval。

## 5. 自己动手的三个任务

1. 增加一个 count_docs 只读工具：补 SYSTEM、validate_action、execute 和成功/非法参数测试。记录为什么工具只能接受允许的参数。
2. 给 finish 增加一条更严格的验收规则，并设计反例。注意不要误称一条规则就能证明语义正确。
3. 用固定的合成 dining 数据问聚餐候选。此数据不是真实餐厅，缺实时空位；答案必须保留未知项，不得声称已经预订。fake 不适合完成此任务，可先编写新的脚本场景，再用真实本地模型测试。

如果之后要做预约动作，先另写 mock 服务与确认状态机。不要把外部 HTTP、shell 或付款入口直接塞进本练习。

## 6. 本次验证记录

- 日期：2026-11-06。
- 环境：隔离工作目录，Python 3.12.14。
- 执行者：助手；不是用户个人实践经历。
- 已执行：python -m unittest -v（14 项通过）、python agent.py --mode fake（返回 completed_unverified）；提交前再次执行测试和语法检查。
- 未执行：真实模型接口、原 ai-research-copilot 的整套测试、网页/App 集成、多用户、真实生活服务、生产部署。

我实际操作之后，应另记日期、代码版本、命令、输出、失败和自己的修改，不把这段记录直接写成我的面试经历。

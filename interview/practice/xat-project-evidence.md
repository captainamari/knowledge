# xat：把 Python 机制讲成可验证的测试工程设计

核验日期：2026-10-23。代码基线为 xat `main` 的固定提交 [`2f471b32667658704de6a2a28576638a0e43305f`](https://github.com/captainamari/xat/tree/2f471b32667658704de6a2a28576638a0e43305f)，版本 0.4.0。本文是项目备考证据卡，不是某家公司的原始面试题。

用户已确认这是与 AI 协作重构的个人项目。以下能证明代码存在及机制可解释，不能自动证明每行由本人独立编写、个人已熟练掌握，或已在公司生产环境取得收益。面试前应自己演示、解释关键路径，并补充真实决策过程。xat 当前是私有仓库，受现有许可证约束，不称“开源项目”；代码链接需要相应仓库权限。本文只总结机制，不转载私有源码。

## 1. 先把项目定位讲准确

**适用岗位：** Python 后端、测试开发；AI 应用工程可把它作为 AI 协作开发与确定性验证的案例，而不是模型或 Agent 项目。

**可练习的 90 秒介绍，需按本人实际责任调整：**

“xat 是我与 AI 一起重构的个人 HTTP 业务测试框架。我希望保留可迁移的测试工程骨架，让业务脚本负责请求构造和断言，把环境特有的管理平台、执行引擎和内部协议留在接入层。目前实现了 unittest 用例基类、HTTP 薄封装、用例发现与命令行运行，以及日志、显式缓存和 JSON 访问视图。0.4.0 增加按文件启动独立 Python 进程的并发运行。我会重点解释三个取舍：为什么复用 unittest 生命周期，为什么进程隔离仍不能隔离业务数据，以及缓存怎样避免跨实例和可变返回值串扰。验证要覆盖成功、故意错误、导入失败、清理失败和子进程崩溃。当前还没有远程执行平台、单文件超时或生产规模收益证据。”

不要在现场一次讲完所有模块。面试官问 Python 深度时选缓存或 JsonView；问测试工程时选生命周期与 oracle；问执行架构时选发现、进程调度与结果判定。

## 2. 已实现能力与源码定位

以下链接均固定到上述基线，不随 main 变化而改写本次结论。

| 模块 | 已实现机制 | 能证明什么 / 不能宣称什么 |
| --- | --- | --- |
| [case.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/case.py) | `BaseCase(unittest.TestCase)`；每方法独立 context；输入映射深拷贝；原生断言、fixture、addCleanup | 生命周期复用与对象状态边界；不是自研断言引擎或测试项目生成器 |
| [http.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/http.py) | `request` 返回原始 Response；默认 timeout=10、禁重定向；Session 由调用方提供并关闭 | 保留协议及业务判断；没有自动重试、自动成功断言或 HTTP 结果缓存 |
| [cli.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/cli.py) | 多路径预验证；递归发现；resolve 去重和目录循环检测；包导入与普通文件动态导入；当前模块 BaseCase 子类筛选 | 理解导入、身份、路径与收集边界；不执行任意目录中的所有 Python 类 |
| [_parallel.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/_parallel.py) / [_worker.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/_worker.py) | 线程池限制文件任务；每文件新 Python 子进程；临时输出和 JSON 计数校验；崩溃显式失败 | 线程负责调度、进程执行业务；不是同文件方法并行、远程引擎或安全沙箱 |
| [cache.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/cache.py) | signature 参数归一化、wraps、typed LRU、接收者身份键、存入/取出 deepcopy | 缓存语义与可变对象隔离；不保证 single-flight、TTL、跨进程共享或外部数据新鲜性 |
| [json_view.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/json_view.py) | dict/list 可变视图；属性/下标/迭代等协议；copy/deepcopy；保留名用下标 | Python 数据模型与别名关系；不是 JSON schema 校验器、只读快照或 ORM |
| [log.py](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/xat/log.py) | 标准 logging / LoggerAdapter；前缀、级别、调用位置、格式及终端颜色；只替换自有 handler | 可嵌入库的日志边界；不是分布式 tracing、自动脱敏或集中日志平台 |
| [pyproject.toml](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/pyproject.toml) | setuptools 构建、requests 依赖、Python >=3.11 声明、xatrun console script | 包入口与交付方式；最低版本声明不等于每个版本都已运行验收 |

## 3. 一条执行链，连起语言与系统知识

1. `xatrun PATH...` 或 `python -m xat PATH...` 进入 CLI；旧 `xat run PATH` 不保留别名。
2. 先验证所有入口，发现文件并按规范化绝对路径去重。显式文件只运行该文件，目录默认匹配 `test*.py`。
3. `-c 1` 在当前进程收集和执行；`-c N` 且 N>1 时，每个文件在新解释器中自行导入、构造用例和运行，同文件方法仍串行。
4. 用例准备、断言、清理与 skip/expectedFailure 等由 unittest 管理。HTTP 请求的网络异常向上传递，4xx/5xx 留给业务测试判断。
5. 并发父进程检查退出码、报告字段和计数类型；缺报告、崩溃或矛盾结果记为 worker error，不能当成功或零用例。
6. 输出按文件完成顺序整块展示，临时文件最终删除。没有运行中实时日志，也没有持久化逐用例报告。

**边界追问：** resolve 解决同一路径别名及符号链接去重，不等于按文件内容去重，也不是硬链接 inode 去重。动态导入会运行模块顶层代码，运行器只应执行可信测试目录；路径哈希是命名防碰撞手段，不是安全审查。

## 4. 哪些价值可以说，哪些需要补证据

可以从代码直接说明：减少用例重复搭建骨架；保持断言和业务协议由使用者控制；用文件进程减少模块全局状态相互污染；失败不被静默吞掉；把可迁移组件与环境专属能力拆开。

尚不能写成量化成果：执行快了多少倍、节省多少人天、覆盖多少线上服务、降低多少缺陷率、支持多少并发。文件进程启动有成本，任务分布和下游负载决定收益，应在固定输入与同等正确性下测量。仓库中的小样本验证不能替代生产容量结论。

面试官问“为什么不用 pytest”时，可答：本项目选择复用 unittest 的已有语义并控制框架范围；pytest 的 fixture/参数化/插件生态可能更适合另一类需求。应比较接入成本、团队存量用例与扩展需求，不宣称自研一定优于成熟工具。

## 5. 证据分层与下一次演示

- **已核验代码：** 上述固定提交的模块和测试。实现行为与限制分别见 [RUNNER](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/docs/RUNNER.md)、[CASE_LOG_CACHE](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/docs/CASE_LOG_CACHE.md)、[NAMING_JSON_LOGGING](https://github.com/captainamari/xat/blob/2f471b32667658704de6a2a28576638a0e43305f/docs/NAMING_JSON_LOGGING.md)。
- **仓库既有验证记录：** Linux / Python 3.12.14 / requests 2.34.2 下，源码和独立安装 wheel 各 80 项通过，业务 demo 10 场景及错误总价检出、并发重叠、崩溃和中断验证。这里保留为仓库报告，不能写成个人现场独立复验。
- **本轮整理复验（2026-10-23）：** Linux / Python 3.12.14 下，editable 安装运行 80 项测试，13.413 秒，全部通过；构建并安装 wheel 后，在源码目录外清除 PYTHONPATH、确认从 site-packages 导入，再运行同一套 80 项，13.460 秒，全部通过。wheel 的 10 个包内 .py 文件与固定提交逐字节一致，未打包 tests/demo。这是整理时的环境结果，不代表本人已现场独立完成；这 80 项包含本地订单服务的 10 场景集成验证：正常/错误总价注入分别在串行 1、并发 3 下运行，错误总价能被检出，结束后订单资源清空；不能再把 10 场景额外加成 90 项测试。
- **未覆盖：** Windows/macOS、其他 Python 运行时、真实公司服务、生产容量及远程 CI。Python 3.11 语法解析不能替代运行时验收。
- **尚未实现：** 单文件超时、强制终止后的业务补偿、子用例派生进程树管理、远程后端切换、逐用例持久化报告、自动重试、分布式资源锁。

建议自己演示三个反例：① setup 中拿到资源后失败，已登记 cleanup 是否执行；②两个逻辑相等但身份不同的实例缓存是否串用、修改返回值是否污染下次命中；③子进程无结果退出是否仍让整体失败。先写预期再执行，保存命令、版本、输入和实际结果，别只截图绿色汇总。

## 6. 深入回答入口

- [Python 机制中的 xat 专项追问](../topics/python-go-runtime-and-os.md#xat-python)
- [项目介绍与设计取舍中的 xat 回答](../topics/project-depth-and-tradeoffs.md#xat-project)
- [AI 代码与测试可信度中的 xat 示例](../topics/ai-assisted-development-and-testing.md#xat-validation)

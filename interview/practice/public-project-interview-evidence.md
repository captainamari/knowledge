# 项目公开版证据：事实、回答与验证边界

核验日期：2026-10-23。公开项目使用公开技术资料；XAT 按项目所有者本次要求核对最新实现，仅整理可公开的通用设计解释，不附私有代码、日志、内部路径或访问链接。工作沟通和个人隐私不进入材料。公开仓库能证明某个实现存在，不自动证明个人独立贡献、亲自运行或生产收益。

## XAT 0.5.0：结果可信度与 HTTP 扩展

核验基线：2026-10-23 当日最新主线的 0.5.0，实现与专项测试静态阅读，未独立执行。项目来源经所有者授权核对；本公开版不提供非公开源码定位或访问链接。[公开项目页](https://captain-site-lake.vercel.app/projects/xat/)仍描述 0.4.0，可用于历史目标与公开职责，不是当前版本能力清单。

### 已核对实现

- 统一运行请求与结构化运行结果；Python 接口不直接退出宿主，由 CLI 映射退出码。方法、运行、HTTP 与业务状态区分。
- 通过 unittest 结果回调收集，不重写原生用例生命周期。同方法多错误保留多个事件；类 fixture、导入及 worker/运行失败不伪造已执行方法。
- JSON 格式版本、字段与一致性校验；同目录临时文件后替换；worker 报告身份、完整性和退出状态复核。缺报告或崩溃暴露为不完整失败，报告写入失败不覆盖已有用例结果。
- 默认当前进程串行；并发模式采用文件级独立 Python 进程，线程池负责调度；中断保留可取得结果、暴露未完成，不能承诺强杀后的业务补偿。
- 原 HTTP 接口仍返回原生响应；可选客户端提供请求准备、单次传输和响应包装扩展。默认自有 Session 与外部注入资源的关闭责任分开，流响应须显式释放。
- 新增方法与 HTTP 关联日志、分类汇总和 full/summary/off 模式，当前默认 full。日志不应消费流或改变原请求返回/异常。

### 实现边界与待改进

没有自动重试、总运行截止时间、完整远程执行协议或业务数据隔离保证；HTTP 模型不是远程序列化任务。请求数据只做特定字段的顶层复制，不承诺深层不可变。日志没有自动脱敏/截断，summary 与 traceback 也可能泄露数据；日志关联不是分布式 tracing。报告原子替换不是数据库事务或全量容灾承诺。项目不在此宣称开源、生产规模或跨平台验收。

### 验证证据分层

- **本轮完成：** 实现与测试静态交叉阅读，确认上述机制及边界；没有重新执行项目测试。
- **最新仓库报告：** 111 项源码与隔离 wheel 验证通过，是项目报告，不改写为本轮复测或用户亲自执行。
- **旧记录：** 公开页面 80 项属于 0.4.0；0.5.0 较早阶段记录 101 项，不是本次读取的最新总数。
- **仍未确认：** 远端 CI 通过、Windows/macOS、Python 3.11 运行时、真实公司接口或生产性能。本轮未取得该提交的 CI 通过证据，不能据此说 CI 已绿。

**可支撑：** 测试开发/Python 工具工程的结果模型、生命周期、进程隔离、报告校验、HTTP 所有权与日志副作用讨论。**需本人补证：** 独立解释与演示、真实决策和排障过程；源码存在不自动证明个人已熟练掌握。公开职责仍是通用能力提炼、边界与取舍、与 AI 协作重构和评审，不改写为独立完成全部代码。

## notification-hub：Python 服务与结果语义

固定版本：[7c6ef039047e9adae7c6ca14d4e32204f352957c](https://github.com/captainamari/notification-hub/tree/7c6ef039047e9adae7c6ca14d4e32204f352957c)。

- [项目说明](https://github.com/captainamari/notification-hub/blob/7c6ef039047e9adae7c6ca14d4e32204f352957c/README.md)：小型自托管通知网关，统一 HTTP 入口，服务端路由，Apprise 作为投递引擎。
- [请求入口](https://github.com/captainamari/notification-hub/blob/7c6ef039047e9adae7c6ca14d4e32204f352957c/app/main.py)：鉴权依赖；线程池调用同步发送；未知渠道、无可用配置及全量投递失败映射到不同错误。
- [投递实现](https://github.com/captainamari/notification-hub/blob/7c6ef039047e9adae7c6ca14d4e32204f352957c/app/notifier.py)：分别记录成功、失败、跳过，部分成功返回 partial；没有成功时抛异常。request_id 不是持久幂等键。
- [限流实现](https://github.com/captainamari/notification-hub/blob/7c6ef039047e9adae7c6ca14d4e32204f352957c/app/security.py)：带锁的进程内滑动窗口；不代表跨实例统一配额。
- [已有测试](https://github.com/captainamari/notification-hub/blob/7c6ef039047e9adae7c6ca14d4e32204f352957c/tests/test_notifier.py)：包含未知渠道、无配置以及成功渠道与未配置渠道并存时的 partial 检查；替换了真实投递函数，不能证明供应商送达。

**可支撑：** 解释分层、错误契约、依赖边界及限流作用域。**需本人补证：** 实际决策过程、独立演示、真实测量与修改记录。**不能据此宣称：** 多租户平台、消息队列、持久重试、恰好一次或真实业务规模。

## ai-research-copilot：分阶段建模与持久化边界

固定版本：[242e34596624d55ab2263e2710000f299e7f2fbd](https://github.com/captainamari/ai-research-copilot/tree/242e34596624d55ab2263e2710000f299e7f2fbd)。

- [项目说明](https://github.com/captainamari/ai-research-copilot/blob/242e34596624d55ab2263e2710000f299e7f2fbd/README.md)：分阶段的研究工具；研究问题 API 与界面、本地存储、问题/假设/来源/证据/日志对象。README 阶段表仍将 Phase 1 标作进行中，不据功能清单宣称完整阶段验收。
- [存储实现](https://github.com/captainamari/ai-research-copilot/blob/242e34596624d55ab2263e2710000f299e7f2fbd/src/research_copilot/research_os/storage.py)：按对象类型读写 JSON，支持保存、查询、筛选和更新；写入临时文件后替换正式文件。完整读改写没有并发事务保护。
- [已有测试](https://github.com/captainamari/ai-research-copilot/blob/242e34596624d55ab2263e2710000f299e7f2fbd/tests/test_local_json_storage.py)：保存读取、筛选、更新及不同模型文件隔离；不把这些顺序测试解释为并发正确性证明。

**可支撑：** 小步交付、数据建模、存储抽象及演进取舍。**需本人补证：** 学习触发点、自己推动过的改变和实验。**不能据此宣称：** 已完成完整 RAG、Agent、自动研究闭环或高并发持久化系统。

## 本轮核验范围

本轮读取公开项目资料，并按授权核对 XAT 最新实现与测试；未运行上述项目、未调用真实供应商、未执行部署或性能测试。文档里的新增故障实验均待实践。仓库中存在测试与本次运行通过是两种不同证据。

完整答案见[项目表达主题](../topics/project-depth-and-tradeoffs.md#interviewer-three-questions)。不要把证据卡直接背成个人履历；每次面试按真实职责与目标 JD 选择内容。


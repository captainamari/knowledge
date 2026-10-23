# 公开项目证据：事实、回答与验证边界

核验日期：2026-10-23。只使用公开技术资料；不从私有代码、工作沟通或个人背景补入未公开信息。公开仓库能证明某个实现存在，不自动证明个人独立贡献、亲自运行或生产收益。

## XAT：测试开发与 Python 工具工程的优先案例

来源是无需登录可读的[个人公开项目页](https://captain-site-lake.vercel.app/projects/xat/)，页面更新于 2026-10-23，本文读取的是其描述的 0.4.0 快照，不称之为当前代码最新版本，不引用私有源码。

页面公开说明：本人负责通用能力提炼、边界与设计取舍、与 AI 协作重构及实现评审；框架复用 unittest 生命周期，以文件级独立进程隔离执行，提供 HTTP 薄封装、参数归一化缓存、JSON 视图和日志工具。页面报告 Linux / Python 3.12 下源码及独立 wheel 的 80 项回归，以及错误总价与资源清理验证。这是公开报告，不是本轮重新运行，也不是跨平台或生产收益证据。

**可支撑：** 以测试工程为主线的架构、资源所有权、Python 语义和失败判定讨论。**需本人补证：** 现场解释、真实决策过程及能独立复现的反例。**不额外推断：** 独立完成所有代码、生产规模、未公开新版本能力或跨公司落地效果。

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

本轮读取公开说明、代码与部分测试文件，未运行上述项目、未调用真实供应商、未执行部署或性能测试。文档里的新增故障实验均待实践。仓库中存在测试与本次运行通过是两种不同证据。

完整答案见[项目表达主题](../topics/project-depth-and-tradeoffs.md#interviewer-three-questions)。不要把证据卡直接背成个人履历；每次面试按真实职责与目标 JD 选择内容。

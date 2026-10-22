# 后端基础：网络、系统设计、数据库与算法练习

## 岗位与背景

适用岗位：后端开发、测试开发及需要后端能力的AI应用工程。原始题目材料发表于2024年4月，未明确公司、具体岗位、职级和完整JD，因此不归入某家公司真实面试。技术解释核验于2026-10-22，版本见各专题。以下保留20项题意，不宣称是官方题库或整理者原创出题。

系统设计中的用户/设备规模属于题目条件；活跃率、吞吐、预算、延迟和故障模型未给出，回答时应先澄清。

## 网络8题

| 原题号 | 本库ID | 题意 | 详解 |
| --- | --- | --- | --- |
| 1 | N1 | HTTPS的通信安全机制 | [N1](../topics/networking-and-protocols.md#n1) |
| 2 | N2 | TCP三次握手与两次/四次的区别 | [N2](../topics/networking-and-protocols.md#n2) |
| 3 | N3 | UDP是否需要握手 | [N3](../topics/networking-and-protocols.md#n3) |
| 4 | N4 | TIME_WAIT的用途 | [N4](../topics/networking-and-protocols.md#n4) |
| 5 | N5 | 如何理解TCP“拆包粘包” | [N5](../topics/networking-and-protocols.md#n5) |
| 6 | N6 | TCP可靠性与业务幂等 | [N6](../topics/networking-and-protocols.md#n6) |
| 7 | N7 | QQ使用TCP还是UDP | [N7](../topics/networking-and-protocols.md#n7) |
| 8 | N8 | Linux Keepalive与应用心跳 | [N8](../topics/networking-and-protocols.md#n8) |

## 系统设计6题

| 原题号 | 本库ID | 题意 | 主题归属 |
| --- | --- | --- | --- |
| 1 | A1 | 数十亿用户规模的用户系统 | [系统设计、容量估算](../topics/backend-systems.md#a1) |
| 2 | A2 | 千万设备规模消息推送 | [系统设计、长连接、消息可靠性](../topics/backend-systems.md#a2) |
| 3 | A3 | 消息中间件的不重不丢 | [持久化、确认、重试与幂等](../topics/backend-systems.md#a3) |
| 4 | A4 | URL输入到页面呈现的过程 | [网络、浏览器、服务链路](../topics/backend-systems.md#a4) |
| 5 | A5 | InnoDB B+树容量估算 | [数据库、索引、页与记录大小](../topics/backend-systems.md#a5) |
| 6 | A6 | 财务对账系统设计 | [数据模型、一致性、差错处理](../topics/backend-systems.md#a6) |

## 数据库、分布式与算法6题

| 原题号 | 本库ID | 题意 | 主题归属 |
| --- | --- | --- | --- |
| 1 | B1 | 接雨水算法 | [算法、不变量、复杂度](../topics/backend-systems.md#b1) |
| 2 | B2 | MySQL ACID与MVCC/Redo/Undo | [数据库、事务、故障恢复](../topics/backend-systems.md#b2) |
| 3 | B3 | SQL查询完整执行链路 | [数据库、优化与执行](../topics/backend-systems.md#b3) |
| 4 | B4 | Raft一致性机制 | [分布式、复制、故障模型](../topics/backend-systems.md#b4) |
| 5 | B5 | Hive实现原理 | [数据处理、查询执行](../topics/backend-systems.md#b5) |
| 6 | B6 | 秒级精度、跨度2年且不丢任务的延时队列 | [持久化调度、恢复、幂等](../topics/backend-systems.md#b6) |

## AI应用工程：背景不完整的补充线索

另有一份Agent方向面试讨论，原始15题图片未取得，只有评论可读；不并入上面的20题或安全后台17题，不把评论改写成已核实的实际问法。仅保留学习方向：

- 上下文预算、聊天历史与跨会话记忆：具体题目与项目条件未说明。
- FSM、LangGraph、ReAct和Chain的控制流取舍：各题与术语的对应关系未核实。
- Skill、工具或插件封装：定义和版本未明确，不能套用某厂商规范。
- 工厂模式、本地配置/部署、后台搭建：实际环境未说明。
- 最长有效括号、股票交易类算法：股票题的交易次数/手续费等变体未知，不补造完整题目。
- 第9项题意未知，无法据此给出题目或答案。

这些线索适用于AI应用学习，不代表已核实某企业正式岗位要求。已有可复用内容从[AI应用工程](../topics/ai-application-engineering.md)与[项目取舍](../topics/project-depth-and-tradeoffs.md)进入；等明确题目条件后才新增对应题卡。

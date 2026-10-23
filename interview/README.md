# 面试知识与实践库

以**主题**保存可复用知识，以**岗位路线**安排学习优先级，以**项目/练习证据**证明理解；岗位案例保留题号、背景与覆盖边界。不按每篇推文重复复制答案，也不为三个岗位各复制一套内容。

本库主要服务 Python 后端、AI 应用工程、测试开发的日常积累。没有取得某个具体职位的完整 JD，因此岗位侧重点是整理者建议，不是公司官方要求；看到新 JD 后再调整优先级。

## 目录的职责

- `topics/`：回答框架、机制、取舍、追问、易错点与一手依据；相近问题合在一张主题卡。
- `cases/`：岗位背景、题意与主题映射；未知公司/职级不猜测，背景不完整不补造原题。
- `sources/`：仅保留宝玉AI运用能力讨论及其署名、阅读边界。
- `practice/`：小实验、可运行实现、实测结果与个人证据卡。明确区分已执行、文档核验和待练习。

## 主题入口

- [项目表达、开源贡献与设计取舍](topics/project-depth-and-tradeoffs.md)：新增面试官三问、公开项目目标答案与深入追问。
- [AI辅助开发与测试可信度](topics/ai-assisted-development-and-testing.md)
- [AI应用工程：业务适配、工具、评测与文档处理](topics/ai-application-engineering.md)
- [Python、Go与操作系统运行机制](topics/python-go-runtime-and-os.md)

- [网络协议：连接与业务可靠性](topics/networking-and-protocols.md)
- [系统设计、数据库、分布式与算法](topics/backend-systems.md)

- [测试开发：RAG评测、WebSocket与HTTP](topics/test-engineering-rag-and-protocols.md)
- [三数之和：算法与测试验证](topics/three-sum-and-algorithm-validation.md)

## 岗位与面试背景入口

- [游戏安全后台开发：17项问题](cases/security-backend-interview.md)
- [后端基础：网络、系统设计、数据库与算法20题](cases/backend-foundations-practice.md)
- [测试开发：RAG、算法与网络面试练习](cases/testing-engineer-interview.md)
- [宝玉：AI运用能力讨论与精选回复](sources/dotey-ai-ability-discussion.md)

前两组已整理的37题保留，背景不完整的Agent讨论只列学习线索。测试开发新增材料只明确4个主题，不是逐字题单；扩展问法和答案由本库整理。宝玉回复区仍区分直接读取与二手精选。

- [面试官视角：架构、主动推动与复杂问题三问](cases/interviewer-project-evidence.md)：原帖观点与整理者扩展分开，答案按主题维护。

## 三条岗位阅读路线

这些路线引用同一份正文，不是三套重复资料。

### Python 后端

先运行机制与OS，再网络/数据一致性与系统设计，最后项目取舍。练到能解释一次请求的边界、失败与恢复路径，能用测量区分计算、等待和竞争。资深候选人进一步说明容量假设、迁移与回滚，而不只讲语言语法。

### AI 应用工程

先AI开发与测试可信度，再Python并发及服务基础，最后项目的质量、费用、延迟与工具权限取舍。不能只会调用模型API，也不必把所有问题都引向Agent；对岗位真正负责的系统可靠性作答。

### 测试开发

先测试判定依据、分层验证和缺陷检出，再运行机制/网络/数据边界，最后可复现并发问题与质量门禁。除了“有多少测试”，还要能说明测试为什么可信、失败如何定位、误报和执行成本如何控制。

## 可运行练习

- [三数之和Python实现与测试](practice/three_sum.py)：10个具名案例、97,656个穷举数组、1,000个固定种子随机数组及变形检查通过；[解释与验证边界](topics/three-sum-and-algorithm-validation.md)。

- [接雨水Python实现与测试](practice/trapping_rainwater.py)：9个具名案例、21,845个穷举数组、1,000个固定种子随机数组及变形检查已执行通过；[测试记录](practice/trapping-rainwater-test-report.md)。
- [运行时实测范围与个人证据模板](practice/evidence-and-study-log.md)：区分实测、文档核验与尚未执行的练习。

## 项目证据与胜任度自测

- [XAT 0.4.0 历史实现与复验记录](practice/xat-project-evidence.md)：固定旧版本的 Python 机制深挖与 80 项实际复验；不作为当前能力或最新测试总数。最新 0.5.0 见下方证据卡与目标答案。

- [公开项目证据卡](practice/public-project-interview-evidence.md)：XAT 0.5.0 授权核验的通用设计、notification-hub 与 ai-research-copilot；区分当前实现、历史报告、本人贡献与待验证能力。
- [从会讲项目到能胜任](practice/project-interview-readiness.md)：优秀候选人目标、证据差距自测、六个基础练习与 XAT 0.5.0 专项验收。不以资料缺失推断个人不会，也不保证面试满分。

## 日常积累方法

1. 读岗位题目，标记“能举真实例子 / 只会概念 / 不会”。不从一篇面经推断所有岗位的题目分布。
2. 每题先练60—90秒主干，再准备可深入3—5分钟的证据。不要一次塞入所有关键词。
3. 每次20—30分钟可拆为：5分钟不看笔记作答、10—15分钟阅读或实验、5分钟重讲。按个人时间调整，不是自动新增日程。
4. 复盘问题定义、机制、证据、边界四项，每轮选一个薄弱点补实验，不用自评分数预测录用概率。
5. 用[练习与证据模板](practice/evidence-and-study-log.md)保存自己的结果。没做过就说待实践，学习项目不得包装成生产经历，不编造指标。

## 收录与修正原则

- 题意、面试背景、整理者扩展和个人经历分开；不批量转载长文。
- “面试官期待”是一种能力评估视角，不代表获知了实际评分标准。
- 技术结论注明实现和版本；事实核验使用一手资料，来源就近，实验环境另列。
- 背景不完整时只记录已知条件。面试回忆、评论和客观事实分开，不强行补齐所谓完整题库。
- 新问题优先补已有主题并保留背景、修正与冲突。保留原题顺序的入口，但答案正文只维护一份。

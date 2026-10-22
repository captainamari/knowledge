# 游戏安全后台开发：项目与语言机制面试练习

## 岗位与背景

- 面试背景：一份候选人自述的腾讯游戏安全后台开发一面回忆，采集于2026-10-22；未获得正式JD或面试官评分表，公司、轮次来自个人回忆而非官方确认。
- 适用方向：Python后端、后台开发；AI应用与测试开发可复习其中质量、运行机制和项目取舍。不能因候选人做Agent项目就将本场改称Agent岗。
- 保留17项题意及题序。回答、追问和实践是学习整理，不是官方题库，也不声称原创出题。学业/实习问题有校招语境，社招按实际可到岗情况调整。
- 自述中涉及学历比较、AI编码比例和情绪评价不作为公司能力标准或统计事实。

## 问题与答案入口

| 编号 | 问题概括 | 阅读位置 |
|---|---|---|
| 1 | 自我介绍 | [主题详解](../topics/project-depth-and-tradeoffs.md#q1-自我介绍) |
| 2 | 介绍项目 | [主题详解](../topics/project-depth-and-tradeoffs.md#q2-介绍项目) |
| 3 | 展开一个有技术深度的点 | [主题详解](../topics/project-depth-and-tradeoffs.md#q3-选择一个技术深点) |
| 4 | 项目为什么要做 | [主题详解](../topics/project-depth-and-tradeoffs.md#q4-项目初衷) |
| 5 | AI 编码参与程度 | [主题详解](../topics/ai-assisted-development-and-testing.md#q5-ai-编码参与程度) |
| 6 | AI 代码如何满足需求 | [主题详解](../topics/ai-assisted-development-and-testing.md#q6-怎样验证-ai-代码满足需求) |
| 7 | AI 测试如何证明有效 | [主题详解](../topics/ai-assisted-development-and-testing.md#q7-怎样证明-ai-生成的测试有效) |
| 8 | 使用 AI 的开发流程 | [主题详解](../topics/ai-assisted-development-and-testing.md#q8-你的-ai-开发工作流) |
| 9 | Python 机制 | [运行时专题](../topics/python-go-runtime-and-os.md#q9-python-机制) |
| 10 | Go 机制 | [运行时专题](../topics/python-go-runtime-and-os.md#q10-go-机制) |
| 11 | 最熟悉的基础方向 | [主题详解](../topics/project-depth-and-tradeoffs.md#q11-你最熟悉哪类基础知识) |
| 12 | OS 视角下的 Python 执行 | [运行时专题](../topics/python-go-runtime-and-os.md#q12-运行-python-文件时操作系统与解释器做了什么) |
| 13 | Agent 能力接近时的个人优势 | [主题详解](../topics/project-depth-and-tradeoffs.md#q13-agent-能力接近时你的优势是什么) |
| 14 | 开源贡献深挖 | [主题详解](../topics/project-depth-and-tradeoffs.md#q14-介绍开源贡献) |
| 15 | 理解原方案的理由 | [主题详解](../topics/project-depth-and-tradeoffs.md#q15-为什么原来选择那套方案) |
| 16 | 学业与实习时间安排 | [主题详解](../topics/project-depth-and-tradeoffs.md#q16-学业与实习安排) |
| 17 | 基础知识的实际作用 | [运行时专题](../topics/python-go-runtime-and-os.md#q17-基础知识对实际开发有什么意义) |


[反问：了解业务、团队与质量要求](../topics/project-depth-and-tradeoffs.md#反问了解岗位而不是反向考试)。

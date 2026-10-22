# 接雨水练习测试记录

- 对应练习：[后端基础B1：接雨水](../topics/backend-systems.md#b1)。算法与测试为学习整理。
- 运行日期：2026-10-22 UTC。
- 解释器：Python 3.12.14。
- 运行命令：`python interview/practice/trapping_rainwater.py`（仓库根目录）；也可在 practice 目录运行 `python trapping_rainwater.py`。
- 依赖：仅 Python 标准库，不需要网络或服务。
- 实际输出：`PASS: 9 named cases; 21845 exhaustive arrays; 1000 seeded random arrays with oracle + 3 metamorphic checks each`。
- 具名案例：空数组、单柱、两柱、单调递减、等高、简单水槽、两组经典数组、大整数水槽；同时检查具名输入不被修改。
- 穷举：长度 0—7，柱高 0—3，共 21,845 个输入，与独立逐点扫描的 O(n²) oracle 比较。
- 随机：seed=20261022，1000 个长度 0—99、柱高 0—99 的数组；对拍后再检查反转不变、所有柱子统一加 7 不变、所有柱子乘 3 后水量乘 3。
- 边界：契约只接受非负整数、单位柱宽的一维模型；没有测试二维/负数/异步流式输入，也没有测试类型错误处理。通过有限测试不等于形式化证明。
- 这份记录只对应本文件算法练习，不表示数据库、消息队列、Hive、Raft 或大规模系统已实现或压测。

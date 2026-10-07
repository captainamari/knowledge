# 从 Magpie 学前端：交互可靠性、状态边界与技术选型

> 用途：下一次实现前端页面时，作为设计、编码和验收清单。
> 整理日期：2026-10-07。源码固定到 [yetone/magpie @ 6b6113a](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb)；后续版本可能不同。
> 本文区分源码事实与可迁移建议；没有进行运行时性能基准，也没有执行 Magpie 的测试。建议是对实现的归纳，不代表作者表达过同样的设计动机。

## 先记住这五件事

1. 先定义状态和失败行为，再选渲染工具：服务端数据、本地草稿、界面状态、请求状态需要不同生命周期。
2. 把焦点、滚动位置、输入草稿当作功能要求。页面“数据对了”不等于交互完成。
3. 乐观更新必须设计失败回滚、连续操作和旧响应；请求顺序问题与使用 Vue / React 无关。
4. 高频更新要合并绘制、控制不可见页面的工作量，并明确请求与订阅由谁关闭。
5. 原生 DOM 省掉一部分构建和框架成本，也需要自己维护渲染、生命周期和组件约定。按项目成本选型，不从单个案例推出普遍结论。

## 1. 源码中的架构是什么

[GUI 架构说明](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/docs/subsystems/gui-shell.md)给出的链路：

```text
Wails v3 桌面宿主（托盘 / 面板 / 窗口）
                     或 magpie web 浏览器入口
                               ↓
         同一套 HTML + CSS + 原生 JavaScript 资源
                               ↓
             同源 JSON API：GET 读取 / POST 写入
                               ↓
                 Go 后端与嵌入的静态资源
```

- GUI 页面没有 Vue / React，也没有 GUI bundler；Go 使用 embed 提供资源。无 bundler 不等于项目没有任何 JavaScript 依赖，浏览器测试仍使用 Node.js / Playwright。
- app.js 使用状态对象、DOM helper、请求 helper 和显式 render 函数；部分视图拆到 routing.js、library.js、plugins.js、sessions.js。[状态与 API](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L1-L115)
- index.html 按固定顺序加载脚本，因此脚本之间的全局依赖和初始化顺序需要维护。[脚本入口](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/index.html#L495-L502)
- Go 给页面内静态脚本和样式引用添加内容哈希，减少新页面混用旧资源的问题。[versionedPage](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/api.go#L615-L641)

**可迁移建议：** 即使不引入框架，也尽早划清 API、状态、视图、交互和资源生命周期的边界。构建步骤少，与代码边界清楚，是两个独立目标。

## 2. 更新页面时，保住用户正在做的事

### 2.1 识别哪些节点可以重建

Magpie 的 renderAgents 会对列表执行 replaceChildren 再创建行；这说明它不是所有位置都做细粒度 DOM patch。[renderAgents](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L246-L267)

整块重建容易理解，却可能丢失节点身份及附着其上的状态：输入选区、焦点、滚动锚点、图片显示状态和第三方控件实例。Magpie 为此有额外补偿，例如重建前暂存并复用图标节点，避免重新创建图片时闪烁。[keepIcons](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L134-L146)

**实现时：**
- 展示型小列表可以先采用简单重建；含输入、拖拽和焦点的区域优先保留稳定节点。
- 用业务 ID 标识列表项，不把当前数组下标当实体身份。
- 只有测量证明必要时才优化；先记录更新频率、列表规模、布局成本和长任务。
- 如果“重建之后补救”的代码越来越多，重新评估 keyed patch、组件化或框架的收益。

### 2.2 刷新数据不能覆盖草稿

load 会保护刷新期间刚写入的偏好，并避免在 provider editor 或 sync form 打开时重建编辑界面。[读取与编辑保护](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L2917-L2952)

建议明确四种状态：

| 状态 | 例子 | 谁负责改变 |
| --- | --- | --- |
| 服务端确认状态 | 已保存设置、列表顺序 | 成功响应或受控刷新 |
| 本地草稿 | 正在输入但未保存的表单 | 用户编辑、明确丢弃、保存成功 |
| 界面状态 | 展开项、选中项、焦点、滚动 | 用户交互与视图生命周期 |
| 请求状态 | pending、错误、请求版本 | 请求层 |

不要把服务端返回值直接覆盖整个页面状态。刷新可以更新展示数据，同时保留 dirty 草稿；确实发生冲突时，明确提示用户如何处理。

### 2.3 焦点与滚动是验收项

排序后，Magpie 会尝试将键盘焦点恢复到对应 provider 的操作柄，并使用 preventScroll。[排序与焦点](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L4695-L4727)

它还维护点击位置及周围节点的屏幕坐标，在重绘和尺寸变化时修正滚动位置；其实现包含 ResizeObserver 和 requestAnimationFrame。[滚动保持](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L19612-L19680)

**借鉴原则，谨慎复制实现：**
- 最先尝试稳定 DOM、合理布局和明确的滚动容器。
- 焦点恢复定位到业务实体；避免每次刷新都抢走焦点。
- 程序化滚动必须服务于明确交互，例如定位搜索结果；后台刷新不要把阅读位置拉走。
- 如果必须保存锚点，明确失效条件、内容缩短时的边界和观察器清理。
- 按鼠标、键盘、窄屏以及目标浏览器分别验收。

## 3. 异步写入：顺滑体验必须有正确性兜底

### 3.1 乐观更新的完整闭环

setPick 的非 native 分支先显示所选值，再发送 POST；成功后采用服务端状态；失败时在版本仍匹配的条件下回滚。序号用于避免较早响应覆盖较晚操作。native 分支走不同流程，不能把这一模式概括为所有写入。[setPick](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L4195-L4254)

排序逻辑也包含本地先改顺序、失败恢复以及“后一次操作优先”的序号检查。[arrangeProvider](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L4695-L4727)

**需要额外想清楚：**
- 序号只能防止旧响应改坏客户端显示，不能保证服务端按用户意图顺序提交。
- 对同一实体并发写，按业务选择串行队列、版本号 / 条件更新或冲突处理；取消 fetch 不等于服务端取消提交。
- 乐观值未必是已确认值。连续操作都失败时，简单回滚到“上一次屏幕值”可能回到一个从未保存的状态。
- 失败后若无法判断服务端是否已提交，显示未确认状态并重新读取权威值；不要把超时解释成一定没有写入。
- 让旧请求的错误提示也遵守作用域，避免错误气泡误导当前操作。
- 低风险且可逆的切换适合乐观更新；删除、支付等高后果操作需要更保守的确认策略。

### 3.2 示例：只读请求的旧响应保护

以下为说明概念而新写的伪代码，不是 Magpie 源码，也不是可直接投产的完整实现。

```js
let generation = 0;
let active = null;

async function refresh(query) {
  const mine = ++generation;
  active?.abort();
  const controller = new AbortController();
  active = controller;
  setLoading(true);

  try {
    const next = await readData(query, { signal: controller.signal });
    if (mine !== generation) return;
    updateServerSnapshot(next); // 不覆盖独立保存的 dirty 草稿
  } catch (error) {
    if (mine === generation && error.name !== "AbortError") showError(error);
  } finally {
    if (mine === generation) setLoading(false);
  }
}

function dispose() {
  ++generation; // 让已返回但尚未应用的结果也失效
  active?.abort();
}
```

取消请求用于减少无用工作；版本判断用于保证旧结果不再应用。写入请求还需要前述服务端并发策略，不能照搬这个只读示例。

## 4. 高频数据：分开采集与绘制

routing.js 将多次绘制请求合并到一帧，并在页面不可见时跳过绘制。[rAF 合并](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/routing.js#L1948-L1957)

它通过带 after 序号的长轮询接收路由数据，维护有界的最近记录，并在失败后等待重试；服务端 wait 的超时是 25 秒。[客户端轮询](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/routing.js#L2401-L2469)、[服务端等待](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/trace.go#L258-L271)

**可迁移建议：**
- 数据可以多次到达，UI 每帧只绘制一次最新快照。
- 限制历史记录容量，防止长开页面持续增长。
- 分别决定“隐藏时停止绘制”与“隐藏时停止网络请求”。它们并不等价；上述片段不能证明隐藏时停止轮询。
- 给轮询 / 订阅明确 owner 和 dispose：取消请求、定时器、rAF、事件监听与观察器。
- 网络失败区分可重试与不可重试错误；结合业务使用退避与抖动，并保留恢复入口。
- 重连时处理游标过期、服务重启、重复事件和漏事件。
- SSE、WebSocket、长轮询各有部署与恢复成本；按数据频率和双向通信需求选择，不能仅凭流畅动画推断采用了哪种协议。

## 5. 导航、错误与安全也要统一

show 在离开部分编辑视图前检查 dirty 状态，允许取消导航；之后才更新可见视图、标题和 URL。[导航流程](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L19692-L19754)

API helper 统一处理 GET / POST、204、JSON 解析、非 JSON 错误及部分业务错误；el helper 的普通文本使用 textContent。[API 与 DOM helper](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L71-L115)

**实现时：**
- 让点击侧栏、打开新建、关闭弹窗和返回等离开草稿的入口共用规则。
- 取消离开后，URL、当前页和草稿仍应一致；异步确认期间重复导航也要测试。
- 明确区分加载中、成功空数据、加载失败、旧数据仍可用。读取失败不能被解释成空列表。
- 普通不可信内容使用 textContent；需要富文本时建立消毒和允许列表。一个安全 helper 不代表所有 HTML 插入点都安全。
- DOM 拼接中的属性、URL、CSS selector 也有各自的校验 / 转义规则，不要只考虑正文文本。
- 统一弹窗焦点、背景不可交互、Escape、关闭动画与重新打开的行为。

## 6. 如果用 Vue / React，怎么迁移这些经验

这些是职责的映射，不要求复刻 Magpie 的 API 或文件结构。

| 问题 | 原生 DOM 中承担的位置 | Vue / React 中的落点 |
| --- | --- | --- |
| 状态到视图 | 显式 render 与 DOM 操作 | 模板 / JSX、组件状态与 props |
| 稳定的列表身份 | 业务 ID、复用节点 | 稳定的 key 与组件边界 |
| 草稿存活 | 单独 draft、避免重建 | 独立草稿状态、避免无意 remount |
| 请求竞态 | seq、取消、写入队列 | composable / hook / 请求层中的同类策略 |
| 副作用清理 | 手写 dispose | watcher / effect cleanup 与卸载处理 |
| 焦点与滚动 | DOM 引用和行为约定 | ref / 模板 ref 加同样的行为约定 |
| 高频数据 | rAF 调度与可见性判断 | 数据层节流、组件边界、必要时 rAF |

React 的 re-render 是重新计算输出，不等于销毁并重建整个 DOM；提交阶段只应用必要变化。Vue 列表也需要正确 key 来维持节点身份。框架能帮助组织和更新 UI，但不会自动理解“哪个请求结果应该获胜”或“这个草稿不应被覆盖”。[React 渲染与提交](https://react.dev/learn/render-and-commit)、[Vue 列表与 key](https://vuejs.org/guide/essentials/list.html)

React effect 和 Vue watcher 都提供清理机制，但开发者仍需正确注册取消与清理逻辑。[React useEffect](https://react.dev/reference/react/useEffect)、[Vue watcher 清理](https://vuejs.org/guide/essentials/watchers.html#side-effect-cleanup)

### 技术选型时问这些问题

**可以评估原生 DOM 的情况：**
- 页面及交互边界明确，组件复用量有限；
- 团队愿意维护明确的状态、渲染、销毁约定；
- 简单资源交付和宿主集成很重要；
- 真实交互测试能覆盖手动 DOM 操作风险。

**框架收益可能更大的情况：**
- 多人协作、视图数量多，跨页组件与复杂表单持续增加；
- 大量条件渲染、列表更新和生命周期管理；
- 需要稳定的组件库、可访问性实践、路由和调试生态；
- 手写的节点复用、清理和状态同步已经变成一套隐式框架。

评估总成本：构建 / 依赖维护 + 运行时成本 + 开发效率 + 测试成本 + 长期演进。Magpie 的 app.js 在该快照中为 1,043,281 字节、约 20,289 行；这是原始文件规模，不是压缩后传输量，更不是启动时间、内存或交互性能数据。没有同场景实测，不能声称它比 Vue / React 更快或更轻。

## 7. 从 AI 工程复盘借鉴的质量护栏

Magpie 的 [LESSONS.md](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/LESSONS.md)记录了真实问题与返工。以下是适合前端任务的归纳：

- 按报告者的真实输入、平台和操作路径复现，不用看起来相似的样例替代。
- 共享逻辑出错时检查所有同类入口；新 API 也要更新其他页面的测试 fixture。
- 测试“用户编辑后再同步 / 刷新”，保护已有内容。
- 区分通过、失败和未运行。构建通过不代表交互验证完成，取消的 CI 不算通过。
- 修改后在最终提交重新验证；保留执行过哪些测试的记录。
- 将无关问题拆开处理，避免一次改动混入多个目标。
- AI 可以降低写代码的成本，正确性仍需要可复现的证据与明确的验收规则。

该项目提供 Chromium / WebKit UI 测试；架构文档还明确指出其 CI Test workflow 不运行这套 GUI 测试，不能看到 CI 绿灯就假设 UI 已验证。本文只阅读相关实现与说明，没有执行这些测试。[验证说明](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/docs/subsystems/gui-shell.md#verification)

## 8. 下次实现页面时直接使用的清单

### 开始前
- [ ] 列出服务端状态、草稿、界面状态和请求状态。
- [ ] 给每个状态指定 owner、写入入口和失效条件。
- [ ] 定义实体 ID、列表规模、刷新频率和性能预算。
- [ ] 写清楚加载 / 空 / 错误 / 重试 / 未保存 / 保存中 / 成功状态。
- [ ] 为主要交互确定焦点和滚动行为。
- [ ] 基于项目规模与维护能力选择原生 DOM、Vue 或 React。

### 编码时
- [ ] 集中处理请求错误，不把读取失败变为空数据。
- [ ] 只读请求防止过期响应覆盖当前视图。
- [ ] 写入定义并发顺序、失败恢复和结果不确定时的重读。
- [ ] 草稿独立于服务端快照，刷新不覆盖正在输入的内容。
- [ ] 所有离开草稿的入口经过统一判断。
- [ ] 列表使用稳定身份；避免无意重建输入节点。
- [ ] 普通不可信内容按文本插入，审核富文本与 URL 入口。
- [ ] 高频更新批处理；明确不可见页面是否继续取数。
- [ ] 每个订阅、监听、定时器、请求和观察器都有清理路径。

### 验收时
- [ ] 快速连续点击 / 保存 / 排序，故意制造响应乱序。
- [ ] 较早失败、较晚成功，以及连续两次失败。
- [ ] 请求超时、非 JSON 错误、成功空结果和重试恢复。
- [ ] 输入到一半刷新或切走；取消离开后草稿和 URL 保持一致。
- [ ] 重绘后键盘焦点、输入选区、滚动位置与图片不异常。
- [ ] 打开 → 关闭 → 动画中重新打开弹窗。
- [ ] 隐藏后恢复页面、网络重连、长时间停留，不累积后台任务。
- [ ] 窄屏、长文本、所有支持语言、目标浏览器与无障碍键盘路径。
- [ ] 记录最终提交、实际运行的检查、失败和未验证部分。

## 9. 推荐阅读顺序

1. [GUI shell](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/docs/subsystems/gui-shell.md)：先理解宿主、资源和 API 边界。
2. [app.js 入口](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L1-L146)：状态、请求、DOM helper。
3. [setPick](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L4195-L4254) 与 [arrangeProvider](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L4695-L4727)：异步写入和交互反馈。
4. [load](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L2917-L2952) 与 [show](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/app.js#L19692-L19754)：编辑保护和导航。
5. [routing.js](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/internal/gui/assets/routing.js#L1948-L1957)：批处理绘制，再读长轮询路径。
6. [LESSONS.md](https://github.com/yetone/magpie/blob/6b6113aa7ad892bb4c710850eeaffcf5172c6deb/LESSONS.md)：把实现技巧补全为可验证的工程流程。

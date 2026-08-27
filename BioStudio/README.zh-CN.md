<h1 align="center">BioStudio</h1>
<p align="center">面向真实工作的开源 AI 工作台</p>


## BioStudio 有什么不同？
**BioStudio 不是又一个 AI 聊天窗口，而是一套面向真实工作的 AI 工作台。** 它以 AI 重塑个人的工作带宽，让多项任务得以并行推进、持续运转并始终处于掌控之中，将个人生产力从单线执行提升为多线协同。
| 核心价值 | 能力说明 |
| --- | --- |
| **多 Workspace 支持** | 在同一工作台中统筹多个 Workspace；文件、Sessions、Git 与项目 Skills 各自归位，让不同项目的上下文彼此独立，又能随时无缝切换。 |
| **多工作流并行** | 让多个 Workspace、Session、Subagent 与后台任务协同推进，将个人工作从单线执行拓展为多线并行，同时保持每条工作流独立、清晰、互不阻塞。 |
| **全程可控、结果可验** | 从 Plan、Todo 到工具调用、上下文、费用与任务状态，全过程透明可见；随时干预或终止执行，并以真实文件和 Diff 验证最终成果。 |
| **从一次对话到持续工作** | 让 Memory 沉淀项目经验、Skills 复用专业能力、Cron 驱动自动化任务、Channels 连接外部入口、Apps 承载完整体验，将一次协作延伸为持续演进的工作体系。 |
| **Workspace 即应用** | 将界面、数据、AI 与自动化汇聚在同一个 Workspace 中，把个人工作方法沉淀为可直接使用、持续演进并可作为模板分享的 AI 应用。 |
## 能力全景
### 核心能力
| 能力 | 说明 |
| --- | --- |
| **AI 工作流** | 多个 Session、Subagent 与后台任务并行运行；通过 Plan、Goal 和 Workflow 应对不同复杂度的任务。 |
| **过程监督** | 集中查看 Plan、Todo、工具调用、上下文占用、Token 使用量、费用消耗和任务状态，实时掌握每个 Session 的执行进度与资源成本，并随时追加指令、调整方向或终止执行。 |
| **Token 成本优化** | 对支持 Prompt Cache 的模型充分复用稳定上下文，实测缓存命中率长期保持在 **96% 以上**，显著减少重复 Token 消耗与长会话成本。 |
| **成果预览** | 直接检查代码、Markdown、PDF、图片、音视频、Word、Excel、PowerPoint、HTML、Plans 与 Diffs。 |
| **Git 工作台** | 查看变更和历史 Diff，管理暂存区、分支与提交，并生成 Conventional Commit 信息。 |
| **Memory** | 跨 Session 延续重要项目经验，在后续工作中按需找回任务结果、关键决策和相关文件。 |
| **Skills** | 将专业方法沉淀为可复用能力，并按全局或 Workspace 范围安装、管理和调用。 |
| **Cron 定时任务** | 让日报、巡检和资料汇总等任务按计划自动运行，并在绑定 Session 中保留完整执行过程。 |
| **Channels 外部入口** | 通过连接器接入微信、Slack、Webhook 等外部请求，并在 BioStudio 中继续管理和处理对应 Sessions。 |
| **模型配置** | 内置 Anthropic、OpenAI、Google Gemini、DeepSeek、智谱 GLM、通义千问（Qwen）、Kimi（月之暗面）、OpenRouter、GitHub Copilot 和 Ollama（本地模型），也支持自定义兼容服务；不同 Session 可独立选择模型与推理强度。 |
| **Web Search** | 支持 DuckDuckGo、Brave、Tavily、Exa、Web IQ 和自托管 SearXNG，为 Agent 提供实时网络信息。 |
### 特色能力
| 能力 | 说明 |
| --- | --- |
| **截图标注发 AI** | 在任意 Preview 中圈选并标注具体问题，把截图与指令直接交给支持视觉的模型。 |
| **Session 内后台任务** | Agent 可将耗时较长的命令和 Subagent 任务转入后台持续运行，释放当前 Session 的交互通道；用户无需等待任务结束，即可继续在同一对话中处理其他工作，并随时查看进度或单独取消。 |
| **HTML Apps** | 让 Agent 快速创建接入 AI、Workspace 文件和持久数据的交互式应用，用于展示、分析和处理数据。 |
| **安全与完整网页模式** | 未知 HTML 默认安全打开；可信页面可启用完整网页能力、保留当前版本授权并使用开发者工具。 |
| **音频转写** | 播放和可视化音频，一键流式转写，再由 AI 整理为会议纪要、访谈总结或行动项。 |
| **SkillHub** | 搜索、筛选并审阅 Skill 包，安装到全局或指定 Workspace，再通过 `@skill-name` 明确调用。 |
| **内置 AI Apps** | 五子棋支持 AI 对手与对局恢复；英语学习提供分级阅读、生词复习、AI 教师、对话和写作练习。 |
## 快速命令集
在输入框键入 `/`，可以快速切换 Agent 的工作方式。普通对话适合直接处理问题；当任务需要自主推进、多人协作式拆解、持续运行或专项审查时，可以使用下面的命令。
### 执行型命令
**`/goal <目标>` — 围绕结果自主推进**
适合目标明确、但实现步骤较多的复杂任务。Agent 会按照 **Plan → Work → Verify** 的闭环持续规划、执行和验证，而不是完成一轮回复就停止；直到目标通过验证，或由你主动终止。
**`/workflow <任务>` — 编排多个 Subagent 协同完成**
适合可以拆成调研、实现、测试、审阅等独立工作包的任务。主 Agent 负责分析依赖、维护 Todo 和调度进度，将可并行的步骤交给不同 Subagent，并持续汇总结果直至任务完成。
**`/review [关注点]` — 对当前改动进行专项审查**
适合在提交或推送前检查代码质量。命令会覆盖工作区中的未提交改动和已提交但尚未推送的内容，并派出独立的 CodeReviewer，从正确性、安全性、可维护性或你指定的关注点出发，按严重度给出文件位置和修改建议。
**`/loop <循环目标>` — 把目标变成持续运行的循环**
适合新闻追踪、定期汇总、质量巡检和持续改进。Agent 会先把循环目标整理成可确认的执行计划，再创建定时调度；后续每次运行都围绕同一目标自主工作并保留完整 Session 上下文。
### 会话管理命令
**`/compact` — 压缩当前 Session 的上下文**
当长对话逐渐接近上下文上限时，提炼并保留关键任务信息，释放更多可用空间。压缩完成后，界面会同步更新当前上下文占用。
**`/clear` — 清空当前消息列表**
移除当前界面中的已有消息，快速恢复干净的对话视图。
## HTML App：把 Workspace 变成应用
HTML App 是 BioStudio 区别于普通 AI 工作台的重要能力。用户只需描述目标，Agent 就可以在 Workspace 中创建一个交互界面，并让它调用 AI、读取和整理文件、保存状态、展示数据。
这意味着 Workspace 不再只是文件和对话的容器，也可以成为数据看板、报告中心、知识浏览器、表单或专用处理工具。HTML App 与 Workspace 中的数据、Skills、Memory 和 Cron 组合后，可以形成一套持续运行、按需演进的轻量 AI 应用。
### 示例：News Tracker Workspace
| 环节 | 工作方式 |
| --- | --- |
| **获取** | Cron 每天收集指定主题的最新新闻。 |
| **处理** | Agent 完成去重、归类、摘要和趋势判断。 |
| **沉淀** | 新闻、来源和分析结果持续保存到 Workspace。 |
| **展示** | HTML App 将结果呈现为可检索、可筛选的 Dashboard。 |
| **演进** | 随时让 Agent 增加数据源、筛选方式、图表或分析维度。 |
HTML App、数据文件和项目 Skills 可以随 Workspace 文件夹一起分享，成为可复用的应用模板。其他用户导入后，配置自己的 Provider 与数据来源，并重新创建所需的定时任务，就可以继续使用和定制。
> **分享的不再只是一份静态结果，而是一套可以重新运行、持续演进的工作方法。**
## 快速开始
### 1. 安装 BioStudio
前往 [最新版本页面](https://github.com/EchoWorker/EchoAIStore/releases/tag/biostudio-latest)，下载适用于 **Windows x64** 或 **macOS Apple Silicon** 的安装包。正式版已经内置 EchoAI，无需额外部署服务。
### 2. 接入你的 AI
首次启动向导会引导你选择 Provider、填写凭据并设置默认模型。你可以连接 OpenAI、Anthropic 等兼容服务，也可以使用已有的 GitHub Copilot 权限登录。完成验证后，模型即可用于对话、文件处理、语音整理和 HTML App。
### 3. 建立第一个 Workspace
选择一个本地文件夹作为 Workspace。建议从已有资料或项目目录开始，例如：
- 一组调研材料、会议记录和数据表；
- 一个需要继续开发或审阅的 Git 项目；
- 一个用于日报、新闻追踪或知识整理的独立目录。
Workspace 会把文件、Sessions、Git、项目 Skills 和 Agent 产出组织在同一上下文中。原始资料与生成结果都留在你选择的目录里，可以直接打开和检查。
### 4. 交付第一个成果
在右侧对话中描述目标，不必先拆解成具体命令。例如：
> **把这个 Workspace 里的调研材料整理成一份季度汇报 PPT。先规划内容结构，再生成文件，完成后让我逐页检查。**
执行过程中，你可以查看 Plan、Todo、工具调用和文件变化，也可以随时补充要求。任务完成后，直接在 Preview 中打开成果，并通过 Git Diff 检查实际改动。
### 5. 开始并行工作
第一个任务运行后，无需等待它结束。新建另一个 Session，就可以继续整理录音、分析数据或修改代码；不同任务会各自运行，状态互不干扰。
熟悉基本流程后，还可以进一步：
- 用 **SkillHub** 安装适合当前工作的专业能力；
- 用 **Cron** 把日报、巡检和资料汇总变成定时任务；
- 用 **HTML App** 为 Workspace 增加 Dashboard、表单和数据处理界面；
- 用 **Channels** 从微信、Slack 或 Webhook 接收外部任务。
## 反馈与许可证
[提交问题或功能建议](https://github.com/EchoWorker/BioStudio/issues) · [查看最新版本](https://github.com/EchoWorker/EchoAIStore/releases/tag/biostudio-latest)
BioStudio 采用 [AGPL-3.0-or-later](https://github.com/EchoWorker/BioStudio/blob/main/LICENSE) 许可证。

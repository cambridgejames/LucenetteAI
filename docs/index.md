# 聆雪AI Lucenette · 文档站

> ⚠️ **项目现状**：处于**设计阶段**，全部功能模块尚未实现。本文档体系（v0.5）由原 README.md 拆分而来，正文原样保留，等待逐步细化。

## 实现状态

| 模块 | 设计文档 | 实现状态 |
|------|:---:|:---:|
| 00 全局共识 | ✅ 初稿 | — |
| 01 跨模块契约 | 🚧 部分初稿 | — |
| M01 用户交互层 | ✅ 初稿 | ⬜ 未实现 |
| M02 主LLM核心 | ✅ 初稿 | ⬜ 未实现 |
| M03 思维子系统 | ✅ 初稿 | ⬜ 未实现 |
| M04 记忆系统 | 🚧 仅占位 | ⬜ 未实现 |
| M05 调度与路由层 | ✅ 初稿 | ⬜ 未实现 |
| M06 能力插件 | 🚧 部分初稿 | ⬜ 未实现 |
| M07 执行机构层 | 🚧 仅占位 | ⬜ 未实现 |
| M08 管理面服务 | ✅ 初稿 | ⬜ 未实现 |
| M09 异常与健康巡检 | ✅ 初稿 | ⬜ 未实现 |

> 图例：✅ 已有初稿 · 🚧 占位/待细化 · ⬜ 未开始。唯一状态源：[04-delivery/work-packages.md](04-delivery/work-packages.md)。

## 文档结构

```text
docs/
├── 00-global/                   全局共识（所有人必读）
│   ├── glossary.md              术语表
│   ├── design-principles.md     设计原则
│   ├── architecture-overview.md 总体架构（原 README 第一章 + 第十一章）
│   ├── tech-stack.md            技术栈选型（原 README 第十章）
│   └── adr/                     架构决策记录
├── 01-contracts/                跨模块契约（先冻结，后实现）
│   ├── standard-command.md      标准指令格式 + 优先级体系（原 README 3.5/3.6）
│   ├── message-envelope.md      输入调度器消息包络
│   ├── mgmt-api.md              管理面 API
│   ├── metrics-api.md           指标接口
│   ├── tool-registry.md         能力注册协议
│   └── device-descriptor.md     设备描述符协议
├── 02-modules/                  模块规格（一份 = 一个工作包）
│   ├── M01-user-interaction.md  用户交互层（原 README 第七章）
│   ├── M02-core-brain.md        主LLM核心（原 README 第二章 2.1–2.2 + 第八章）
│   ├── M03-think-subsystem.md   思维子系统（原 README 第二章 2.3）
│   ├── M04-memory.md            记忆系统
│   ├── M05-scheduler.md         调度与路由层（原 README 第三章 3.1–3.4）
│   ├── M06-game-plugin.md       游戏插件系统（原 README 第六章 + 9.2）
│   ├── M06-smart-home.md        智能家居控制器（原 README 9.1）
│   ├── M06-tts.md / M06-l2d.md  TTS / Live2D
│   ├── M07-executors.md         执行机构层
│   ├── M08-management-plane.md  管理面服务（原 README 第五章）
│   └── M09-exception-health.md  异常与健康巡检（原 README 第四章）
├── 03-standards/                工程规范
│   ├── coding-style.md          代码风格
│   ├── module-doc-template.md   模块文档模板
│   └── testing-acceptance.md    测试与验收
├── 04-delivery/
│   └── work-packages.md         工作包看板
└── rfcs/                        新点子提案
```

## 阅读指引

- 初次了解：00-global/architecture-overview.md → design-principles.md；
- 准备接包：03-standards/ → 对应 Mxx 文档 → 相关 01-contracts/；
- 提出新想法：rfcs/。


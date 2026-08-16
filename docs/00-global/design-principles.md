# 设计原则

> **设计哲学**：*She listens like snow. She connects like a net.*
> **架构核心**：顶层决策，底层自主；单向控制，末端自治；显意识响应，潜意识思考；能力皆插件，管理不侵入；话题可编排，思维可引导。
> **项目代号**：聆雪 Lucenette

本文档汇总全项目的设计原则。任何模块的细化与实现不得违背以下原则；若确需违背，须先记录 ADR（见 [adr/](adr/)）。

## 原则清单

| # | 原则 | 一句话说明 | 出处 |
|---|------|-----------|------|
| 1 | LLM 只负责生成，不负责判断时机 | 主动性由思维子系统与调度器赋予，而非依赖模型自觉 | [architecture-overview.md](architecture-overview.md) 第一章 |
| 2 | 显意识响应，潜意识思考 | 双核架构：事件驱动的主LLM核心 + 24小时循环的思维子系统 | [architecture-overview.md](architecture-overview.md) 第一章 |
| 3 | 顶层决策，底层自主 | 底层模块自主运行，接受顶层单向覆盖 | [M05-scheduler.md](../02-modules/M05-scheduler.md) 第三章 |
| 4 | 单向控制，末端自治 | 中间调度器只做路由，末端调度器自带仲裁与执行 | [M05-scheduler.md](../02-modules/M05-scheduler.md) 第三章 |
| 5 | 能力皆插件，皆可开关 | 内置能力与外部设备统一注册，支持运行时启停 | [M02-core-brain.md](../02-modules/M02-core-brain.md) 第二章 |
| 6 | 管理不侵入数据面 | 管理面单向定时拉取，管理操作不影响实时链路 | [M08-management-plane.md](../02-modules/M08-management-plane.md) 第五章 |
| 7 | 话题可编排，思维可引导 | 话题树由管理面动态配置，引导潜意识探索方向 | [M03-think-subsystem.md](../02-modules/M03-think-subsystem.md) 第二章 2.3 |

## 版本历史

- v0.4（2026-05-29）：原 README 完整版；
- v0.5：文档拆分，建立 docs/ 文档体系，原文原样迁移。

> 📌 待细化：为每条原则补充反例与冲突裁决规则（例如能力开关与异常自动禁用的优先级）。


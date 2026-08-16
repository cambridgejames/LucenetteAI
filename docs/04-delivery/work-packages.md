# 工作包看板

> 本看板是发包状态的唯一数据源。README 与 docs/index.md 中的状态矩阵均与本表同步维护。
> 图例：✅ 已有初稿 · 🚧 占位/待细化 · ⬜ 未开始（实现）。

## 状态总表

| 包号 | 工作包 | 规格文档 | 依赖 | 文档状态 | 实现状态 |
|------|--------|----------|------|:---:|:---:|
| WP-00 | 全局共识（术语/原则/架构/技术栈/ADR） | docs/00-global/ | — | 🚧 | — |
| WP-01 | 跨模块契约冻结 | docs/01-contracts/ | WP-00 | 🚧 | — |
| WP-S | 工程规范（风格/模板/验收） | docs/03-standards/ | — | 🚧 | — |
| WP-M01 | 用户交互层 | M01-user-interaction.md | WP-01, WP-M02 | ✅ 初稿 | ⬜ |
| WP-M02 | 主LLM核心 | M02-core-brain.md | WP-01 | ✅ 初稿 | ⬜ |
| WP-M03 | 思维子系统 | M03-think-subsystem.md | WP-M02, WP-M04 | ✅ 初稿 | ⬜ |
| WP-M04 | 记忆系统 | M04-memory.md | WP-01 | 🚧 占位 | ⬜ |
| WP-M05 | 调度与路由层 | M05-scheduler.md | WP-01 | ✅ 初稿 | ⬜ |
| WP-M06 | 能力插件×4（TTS/Live2D/游戏/家居） | M06-*.md | WP-M05, WP-01 | 🚧 部分初稿 | ⬜ |
| WP-M07 | 执行机构层 | M07-executors.md | WP-M05, WP-01 | 🚧 占位 | ⬜ |
| WP-M08 | 管理面服务 | M08-management-plane.md | WP-01 | ✅ 初稿 | ⬜ |
| WP-M09 | 异常与健康巡检 | M09-exception-health.md | WP-01 | ✅ 初稿 | ⬜ |

## 发包顺序建议

1. WP-00 / WP-01 / WP-S（共识 + 契约 + 规范，必须先完成）；
2. WP-M02 → WP-M04 / WP-M03（核心大脑）；
3. WP-M05 → WP-M06 / WP-M07（调度与能力）；
4. WP-M08 / WP-M09（运维）；
5. WP-M01（用户交互最后对接）。

## 交付要求

- 按 [module-doc-template.md](../03-standards/module-doc-template.md) 第 10 节任务书执行；
- PR 附带验收清单自查结果（细则见 testing-acceptance.md）；
- 文档与代码同步变更。

## 变更记录

- v0.5：文档拆分，建立看板。


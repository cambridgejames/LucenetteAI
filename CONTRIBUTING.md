# 贡献指南

感谢你对聆雪 Lucenette 的关注！本项目当前处于**设计阶段**，以下贡献类型均受欢迎：

- 新的AI角色设计
- 对话质量评估算法
- 安全过滤机制的改进
- 使用案例和文档
- 架构设计文档的细化（docs/ 各章节）
- 模块工作包的实现（见 [docs/04-delivery/work-packages.md](docs/04-delivery/work-packages.md)）

## 如何接包（初稿）

1. 阅读 [docs/index.md](docs/index.md) 与工作包看板，认领未开始的工作包；
2. 阅读该工作包对应的模块规格（docs/02-modules/）、相关契约（docs/01-contracts/）与工程规范（docs/03-standards/）；
3. 按 [模块文档模板](docs/03-standards/module-doc-template.md) 第 10 节任务书执行；
4. 提交 PR：内附验收清单自查结果；文档与代码须同步变更。

> 正式验收流程（测试要求、DoD 清单）待 [docs/03-standards/testing-acceptance.md](docs/03-standards/testing-acceptance.md) 细化后生效。

## 提出新想法（RFC）

本项目是设计先行项目，新想法请先走 [docs/rfcs/](docs/rfcs/) 提案流程（动机 → 方案 → 接口影响 → 验收标准），讨论通过后进入工作包看板或 ADR 记录。

## 文档规范

- 文档与代码同仓、同步演进：代码变更必须连带更新对应模块文档；
- 正文使用中文，代码注释与标识符使用英文；
- 架构决策记录 ADR（docs/00-global/adr/）。


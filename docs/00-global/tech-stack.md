<!--
⚠️ 迁移说明：本文档由原 README.md（v0.4）原样拆分而来，未改动正文内容，仅调整归属（文档体系 v0.5）。
来源：原 README 第十章。
章节编号暂沿用原 README，细化时统一重排。
-->

# 技术栈选型参考

## 第十章：技术栈选型参考

| 模块 | 推荐技术 | 部署位置 | 备注 |
|------|----------|----------|------|
| 主LLM推理 | oobabooga + LLaMA 3 8B Instruct（量化） | 本地RTX 4090 | 支持流式与结构化输出 |
| 思维子系统LLM | 同上，可复用或使用更轻量模型 | 本地GPU | 多节点复用同一模型实例 |
| TTS | 自训练VITS变体模型 | 本地GPU | 需支持流式合成 |
| ASR | Whisper / Faster-Whisper | 本地/云端 | 需支持实时流转写 |
| L2D | Live2D Cubism SDK + Unity | 本地渲染 | WebSocket接收动作指令 |
| 短期记忆 | Redis | 本地 | 低延迟读写 |
| 长期记忆 | ChromaDB / Milvus | 本地 | 向量检索，支持RAG |
| 设备注册中心 | FastAPI + SQLite | 本地 | RESTful API |
| 能力注册中心 | FastAPI + SQLite | 本地 | 能力清单管理 |
| 中间调度器 | Rust / Go 高性能服务 | 本地 | 低延迟消息路由 |
| 末端调度器 | 嵌入式Python / Go | 嵌入式设备/本地 | 网络通信，独立部署 |
| 异常调度子模块 | Python / Go | 本地 | 异常收集、分级、日志 |
| 健康巡检子模块 | Python | 本地 | 定时任务，指标采集 |
| 管理面API | FastAPI | 本地 | 管理面接口 |
| 数据采集器 | Python | 本地 | 定时拉取，适配聚合 |
| 话题树管理器 | FastAPI + SQLite | 本地 | 话题树结构与权重管理 |
| 监控面板 | React + ECharts | 本地Web | 仪表盘可视化 |
| 设备通信协议 | HTTP / WebSocket / MQTT | 局域网 | 根据设备能力选择 |
| 游戏SDK | Neuro Game SDK（TypeScript/Rust/C#） | 游戏侧集成 | 开源可用 |
| 容器化 | Docker Compose | 本地服务器 | 统一管理所有服务 |

---

> 📌 **细化清单（待讨论）**
> - 每项选型补充备选方案与取舍理由（建议 ADR 化）。

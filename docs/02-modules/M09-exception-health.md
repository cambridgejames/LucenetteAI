<!--
⚠️ 迁移说明：本文档由原 README.md（v0.4）原样拆分而来，未改动正文内容，仅调整归属（文档体系 v0.5）。
来源：原 README 第四章。
章节编号暂沿用原 README，细化时统一重排。
-->

# 异常处理与健康巡检子系统（M09）

## 第四章：异常处理与健康巡检子系统

### 4.1 设计目标

复杂分布式系统的核心风险在于：任一子模块的故障都可能导致不可预测的级联行为。异常处理与健康巡检子系统是聆雪的“免疫系统”，负责：

- **统一异常收集**：各子模块仅需上报异常，不负责处理异常
- **分级响应**：根据异常严重程度，触发不同级别的拟人化表现或通知
- **主动巡检**：定期扫描各子系统健康状态，在异常发生前预警
- **日志持久化**：所有异常记录统一存储，支持事后排查

### 4.2 子系统架构

```mermaid
graph TB
    subgraph 异常来源["🚨 异常来源"]
        SubmoduleError[子模块运行时错误]
        HealthCheck[健康巡检子模块<br/>定期主动扫描]
        ExternalAlert[外部告警<br/>设备离线/网络中断等]
    end

    subgraph 异常调度子模块["⚠️ 异常调度子模块"]
        ErrorCollector[异常收集器<br/>统一接收异常报文]
        ErrorClassifier[异常分类器<br/>按严重程度/类型分类]
        ErrorLogger[系统日志记录器<br/>持久化存储]
        ReactionEngine[反应决策引擎<br/>生成控制标签]
    end

    subgraph 输出["📤 输出"]
        L2D_Error[L2D异常表现<br/>priority=10]
        TTS_Error[TTS语音提醒<br/>priority=10]
        Notify[移动端推送通知]
        LogDB[日志数据库]
    end

    subgraph 中间调度器["⚡ 中间调度器"]
        PriorityRoute[优先级路由<br/>异常标签天然获得最高优先级]
    end

    SubmoduleError --> ErrorCollector
    HealthCheck --> ErrorCollector
    ExternalAlert --> ErrorCollector

    ErrorCollector --> ErrorClassifier
    ErrorClassifier --> ErrorLogger
    ErrorClassifier --> ReactionEngine

    ErrorLogger --> LogDB
    ErrorLogger -->|供管理面拉取| LogDB

    ReactionEngine -->|异常表现标签| PriorityRoute
    ReactionEngine -->|语音提醒标签| PriorityRoute
    ReactionEngine -->|推送通知| Notify

    PriorityRoute --> L2D_Error
    PriorityRoute --> TTS_Error
```

### 4.3 异常分级与对应表现

| 级别 | 触发条件示例 | L2D表现 | 语音/通知 | 用户感知 |
|------|------------|---------|-----------|----------|
| **轻微** | GPU占用>90%、单模块响应延迟>3s | “脸红”/“发热”表情 | 主动语音：“我有点热” | 拟人化轻微不适 |
| **中等** | 某模块连续3次报错、设备离线 | “印堂发黑”/“皱眉” | 语音告知具体问题 | 明确的问题提示 |
| **严重** | 核心模块崩溃、LLM推理连续失败 | “晕厥”/“故障”动画 | 推送通知用户，尝试自动恢复 | 立即通知，需关注 |
| **致命** | 系统无法自恢复 | 最小核心存活模式 | 全渠道通知 | 需立即人工干预 |

### 4.4 健康巡检子模块工作流程

```mermaid
sequenceDiagram
    participant HC as 🔍 健康巡检子模块
    participant LLM as 🧠 主LLM
    participant Think as 🧠 思维子系统
    participant Scheduler as ⚡ 中间调度器
    participant TTS as 🔊 TTS
    participant Error as ⚠️ 异常调度子模块

    loop 定期巡检（默认每30秒）
        HC->>LLM: 拉取状态指标
        LLM-->>HC: 返回CPU/GPU占用等

        HC->>Think: 拉取状态指标
        Think-->>HC: 返回周期状态、节点数等

        HC->>Scheduler: 拉取状态指标
        Scheduler-->>HC: 返回队列长度、吞吐量等

        HC->>TTS: 拉取状态指标
        TTS-->>HC: 返回合成延迟、缓冲区状态

        HC->>HC: 综合评估健康度

        alt 检测到异常
            HC->>Error: 上报异常报文
            Error->>Error: 分类/记录/生成反应
            Error->>L2D: 异常表现（priority=10）
        else 一切正常
            HC->>HC: 记录正常日志，等待下一轮
        end
    end
```

---

> 📌 **细化清单（待讨论）**
> - 指标接口契约细化时抽至 01-contracts/metrics-api.md；
> - 异常分级需给出可观测的量化阈值。

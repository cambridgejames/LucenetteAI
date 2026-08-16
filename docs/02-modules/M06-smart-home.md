<!--
⚠️ 迁移说明：本文档由原 README.md（v0.4）原样拆分而来，未改动正文内容，仅调整归属（文档体系 v0.5）。
来源：原 README 第九章 9.1（含第九章标题）。
章节编号暂沿用原 README，细化时统一重排。
-->

# 智能家居控制器（M06-smart-home）

## 第九章：关键交互时序

### 9.1 用户语音指令驱动智能家居

```mermaid
sequenceDiagram
    participant User as 👤 用户
    participant ASR as 🎤 ASR
    participant InputSch as ⚡ 输入调度器
    participant LLM as 🧠 主LLM核心
    participant Intent as 🔗 意图分析器
    participant MidSch as ⚡ 中间调度器
    participant LightSch as 💡 灯光调度器
    participant Light as 💡 智能灯泡

    User->>ASR: “聆雪，把客厅灯光调暗一点”
    ASR->>InputSch: 实时文本流
    InputSch->>LLM: 仲裁后输入
    LLM->>LLM: 生成回复文本 + 控制标签
    LLM-->>Intent: 文本副本（旁挂异步）
    LLM->>MidSch: 控制标签：{target:smart_home, action:dim_light, params:{room:“客厅”, level:50}}

    par 并行处理
        Intent->>Intent: 解析意图
        Intent->>MidSch: 意图指令（priority=8）
    and
        MidSch->>MidSch: 格式统一 → 排序
        MidSch->>LightSch: 按target路由
    end

    LightSch->>LightSch: 过滤 → 仲裁 → 去重
    LightSch->>Light: 执行调暗指令
    Light->>LightSch: 状态反馈
    LightSch->>MidSch: 执行结果回传
    MidSch->>LLM: 状态更新通知
```


---

> 📌 **细化清单（待讨论）**
> - 设备发现/心跳机制待设计；
> - 命令集与虚拟设备组合抽象见 [01-contracts/device-descriptor.md](../../01-contracts/device-descriptor.md)；
> - 第九章 9.2 见 M06-game-plugin.md。

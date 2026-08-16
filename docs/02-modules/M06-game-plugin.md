<!--
⚠️ 迁移说明：本文档由原 README.md（v0.4）原样拆分而来，未改动正文内容，仅调整归属（文档体系 v0.5）。
来源：原 README 第六章 + 第九章 9.2。
章节编号暂沿用原 README，细化时统一重排。
-->

# 游戏插件系统（M06-game-plugin）

## 第六章：游戏插件系统详细架构

### 6.1 双模式自适应策略

| 游戏类型 | 特征 | 控制路径 | 典型游戏 |
|----------|------|----------|----------|
| **反射型游戏** | 需要毫秒级响应，高频操作 | 专用游戏AI自主运行 + LLM宏观决策 | OSU!、空洞骑士、赛博朋克2077 |
| **思考型游戏** | 不需要实时响应，可从容决策 | LLM通过Function Calling直接操作 | 猜词游戏、策略游戏、文字冒险 |

### 6.2 游戏插件系统架构

```mermaid
graph TB
    subgraph 上层决策["🧠 上层决策"]
        LLM_Game[主LLM核心]
        GameReverseAPI[反向调用接口<br/>超时默认逻辑]
    end

    subgraph 游戏类型判断["🎮 游戏类型判断"]
        GameTypeSwitch{游戏SDK上报状态<br/>自动判断类型}
    end

    subgraph 反射型游戏["⚡ 反射型游戏"]
        DedicatedAI[专用游戏AI<br/>自主运行]
        ReflexController[反射控制器<br/>毫秒级响应]
    end

    subgraph 思考型游戏["🧠 思考型游戏"]
        SDKAdapter[SDK适配器]
        FunctionList[Function Calling列表]
    end

    subgraph 执行层["🎯 执行层"]
        GameExecutor[游戏执行器<br/>键鼠/手柄模拟]
    end

    LLM_Game -->|控制标签| GameTypeSwitch
    LLM_Game -->|响应请求| GameReverseAPI
    GameTypeSwitch -->|Boss战/平台跳跃等| DedicatedAI
    GameTypeSwitch -->|选关/策略/对话等| SDKAdapter

    DedicatedAI --> ReflexController
    ReflexController -->|自主操作| GameExecutor

    SDKAdapter --> FunctionList
    FunctionList -->|LLM选择函数| GameExecutor

    DedicatedAI -->|遇到决策点| GameReverseAPI
    GameReverseAPI -->|超时未响应| DedicatedAI

    LLM_Game -.->|最高优先级覆盖| ReflexController
```

---


<!-- ─── 章节分隔（来源不同） ─── -->

### 9.2 游戏场景（反射型游戏）

```mermaid
sequenceDiagram
    participant Game as 🎮 空洞骑士
    participant GameAI as ⚡ 专用游戏AI
    participant MidSch as ⚡ 中间调度器
    participant LLM as 🧠 主LLM核心
    participant TTS as 🔊 TTS

    Note over Game,TTS: 常态：游戏AI自主运行
    Game->>GameAI: 游戏状态（Boss攻击前摇）
    GameAI->>MidSch: 自主指令：闪避
    MidSch->>Game: 执行闪避

    Note over Game,TTS: LLM并行介入：生成战术指导
    LLM->>MidSch: 控制标签：{action:“say”, text:“小心它的回旋斩！”}
    LLM->>TTS: 文本流：“小心它的回旋斩！”
    TTS->>Game: 语音播放（不阻塞游戏操作）

    Note over Game,TTS: 最高优先级覆盖：紧急闪避
    LLM->>MidSch: priority=10：{target:keyboard, action:dodge, direction:left}
    MidSch->>Game: 覆盖游戏AI指令，强制闪避
    MidSch->>GameAI: 通知：上层已接管
    GameAI->>GameAI: 基于新状态重新决策

    Note over Game,TTS: 反向调用：选关决策
    Game->>GameAI: 关卡结束，需选择下一关
    GameAI->>LLM: 反向调用请求
    LLM->>GameAI: 选择关卡（或超时默认随机）
    GameAI->>Game: 加载选定关卡
```

---

> 📌 **细化清单（待讨论）**
> - Neuro Game SDK 集成细节待补充；
> - 思考型游戏的 Function Calling 列表需枚举。

# 消息包络协议（契约）

> 📌 占位：定义输入调度器三类消息（用户 / 思维子系统 / 系统内部）的统一包络格式。细化时定稿。

## 相关现状

- 输入调度器设计（消息暂存 / 超时降级 / 唤醒决策 / 强制唤醒）见 [M03-think-subsystem.md](../02-modules/M03-think-subsystem.md) 2.3.8。

## 待定义

- 包络字段：id / source / type / priority / timestamp / payload / ttl；
- 三类消息的优先级语义与超时降级规则；
- 紧急消息强制唤醒的判定条件与打断策略。


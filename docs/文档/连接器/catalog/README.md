# Connector 认证目录

> GIP 认证分级 · [17 §5.6](../../准备/2026-06-16/17-集成平台化战略(GIP).md)

| 级别 | 要求 |
|------|------|
| **Bronze** | Blueprint + Contract Test + mock 通过 |
| **Silver** | + 1 家 Shadow 零 drift + Revert 实测 |
| **Gold** | + ≥2 tenant + 对账 SLA |

文件命名：`{system}/{vendor}.yaml`（例：`erp/kingdee-read.yaml`）

对外销售只承诺 **Silver+** Pack。

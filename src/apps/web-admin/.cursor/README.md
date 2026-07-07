# .cursor · web-admin 独立 AI 工作流（可迁出）

## 是什么

web-admin 专用 Cursor 规则包：**独立步步流** + **绝对门禁**（不绑定 FactoryOS 后端）。

## 子路径

| 路径 | 用途 |
|------|------|
| `INDEX.md` | 工作流入口 |
| `rules/` | WEB-00/01 绝对门禁 · Dev/Test workflow |
| `factoryos/` | WEB-STEP0 · DEV/TEST/VERIFY-GATES · REDLINES |
| `templates/` | plan · step-stop 模板 |

## 门禁

- 口令：`【WebDev模式启动】` · `【WebTest模式启动】` · `【WebVerify回合】Step N`
- 落盘：`_web_pipeline/<date>/`
- 校验：`scripts/check_boundary_lock.py`

## 变更纪律

1. 改规则/门禁 → 用户「确认结构变更」
2. **迁出**：复制本目录 → 目标项目 `.cursor/`

## 相关文档

- [contracts/WEB-ARCHITECTURE-LOCK.yaml](../contracts/WEB-ARCHITECTURE-LOCK.yaml)
- [ARCHITECTURE.md](../ARCHITECTURE.md)
- [ENGINEERING.md](../ENGINEERING.md)

# 产品原型与战略文档入口

## 本轮合成真源（2026-07-14 · 全库通读 · 兜底核对 v1.1 / v2.1）

| 文档 | 版本 | 用途 |
|------|------|------|
| **[Ax-OS-平台定位与战略白皮书-v1.0.md](./Ax-OS-平台定位与战略白皮书-v1.0.md)** | **v1.1** | 是什么/不是什么 · 商业价值 · 业务策略 · 执行方案 · 设计思路 |
| **[Ax-OS-产品PRD完整版-可还原原型-v2.0.md](./Ax-OS-产品PRD完整版-可还原原型-v2.0.md)** | **v2.1** | 完整 PRD：32 墨刀页规格 · 热区 · Token · API · 验收 · 可供设计 AI 还原原型并落地功能 |

**兜底判定**：战略表述清晰完整；PRD 与 `factoryos-v2` 双向零遗漏；合用可还原原型并落地功能。

---

## 历史分册（已被 v2.0 PRD 吸收 · 可对照）

| 文件 | 说明 |
|------|------|
| `Ax-OS-产品原型说明书-v1.0.md` | 早期标准原型说明（页数较少） |
| `Ax-OS-产品设计稿-v1.0.md` | 高保真/Figma 结构扩展 |
| `Ax-OS-墨刀完整PRD-v1.1.md` | 墨刀专用 34 页规格（已并入 PRD v2.0） |

---

## 可点线框预览

```bash
open docs/设计/modao/ax-os-prototype.html
open docs/设计/factoryos-v2/kpi_dashboard.html   # 五域线框真源（27 页）
```

| 目录 | 说明 |
|------|------|
| `factoryos-v2/` | **线框真源**（对齐 PRD v2.0） |
| `factoryos-v2-bak1/` | 历史备份 |
| `modao/` | 墨刀流程/手册 |
| `figma/` | Token + HTML Kit + **[Cursor-Figma接入手册](./figma/Cursor-Figma接入手册.md)**（MCP 主链） |
| `ax-os-ui/` | 登录定稿 **V4**；V3 / 早期 dashboard IA 已废止 |

---

**搭建顺序**：读白皮书（定位）→ 读 PRD v2.0（建页）→ 对照 `factoryos-v2` HTML → 登录对齐 `ax-os-login-v4-smart-hub.png`。

**Cursor 产品 Agent**：新对话发送 `【PM模式启动】` + 目标 → 细则 [`.cursor/factoryos/PM-GATES.md`](../../.cursor/factoryos/PM-GATES.md)（默认只读；改 Figma 须「可以改 Figma」）。人审三门裁定：`G-FREEZE → G-SHADOW → G-WRITE-APPROVE`。

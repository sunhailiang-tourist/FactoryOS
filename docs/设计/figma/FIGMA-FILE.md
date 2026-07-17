# Figma 文件登记

| 项 | 值 |
|----|-----|
| **团队** | FactoryOS · `team::1658790803485036225` |
| **正式原型** | [Ax-OS-管理台原型-HiFi-v1](https://www.figma.com/design/sAXQZcWCKymcCwPl1kRMeN) · `sAXQZcWCKymcCwPl1kRMeN` |
| **来源** | `factoryos-v2` + `login_v4.html` → html-to-design · 2026-07-15 P0 产品意图补全 |
| FigJam | [Ax-OS-流程图-v1.0](https://www.figma.com/board/x4eS1zdZCeucLavjVthzAN) |
| 废弃 | `PsgQYgwsLH1Vz2Z6LGLk8i` |

## 真源

PRD **v2.1** · 白皮书 **v1.1** · `factoryos-v2` · 登录 V4

## 演示方式

Figma → **Present** → 选起点：

| Flow | 起点 | 用途 |
|------|------|------|
| **P0 · 意图钉死** | P0 · 定位与铁律 | 演示前先钉方向/铁律/四动词/Pack |
| A · 首家接入 | W-01 登录 V4 | Connect→…→Prove→Freeze→Export |
| B · 日常报工 | H-00 产线入口 | H5 报工主线 |
| C · 第二家 Import | W-10 Import 向导 | Package→…→Prove→回 Studio |
| D · Gate/合规 | S-05 门禁地图 | 人审三门 |
| E · H5 三态 | H-三态 · shadow | shadow → false → true |
| F · Prove 负路径 | P0 · Prove 负路径 | 未满 14d / 未双签禁用 |

半透明青蓝块 = `PROTO · …` 热区（分支跳转）。**Studio 步进勿点整帧**，点底部 PROTO。

## 帧清单

**核心 22**：W-01～W-14（Studio 六步独立帧）+ H-00～H-07  
**Import 六步**：Connect/Package/Override/Delta/Prove/Deploy（已拉开横向间距）  
**附页**：S-01～S-08 · O-01 · O-02  

**P0 产品意图（2026-07-15）**：

| 帧 | 钉什么 |
|----|--------|
| P0 · 定位与铁律 | 是/不是 · 演示铁律 · MVP 四动词 · Starter-A Pack |
| P0 · operator→Studio 403 | RBAC：operator 进 Studio 403 |
| P0 · Prove 负路径 | 未满 14d / Drift / 缺 business_owner → 开写禁用 |
| H-三态 · shadow / false / true | H5 三态可指认 |

**画布标注（CALL）**：Connect=Starter-A Pack · 租户=Path A+Pool · Map=四动词 · 证据链=Plan→Confirm→Rule→Execute→Connector→Audit

## PRD §十五自检（P0 后）

| 项 | 状态 |
|----|------|
| 22 核心页齐全；主线 A/B 可点 | ✅ |
| 五域 IA | ✅ |
| Studio 六步名 + Prove 在 Freeze 前 | ✅ |
| Prove：14d / Contract Test / 双签 / 禁用 | ✅（正路径 + 负路径独立帧） |
| H5 三态 + H-04 无 ERP 成功 | ✅（三态独立帧可指认） |
| secrets_ref / operator 403 | ✅（Connect 文案 + 403 帧） |
| 哈森 Path A + Pool / Starter-A | ✅（CALL 标注 + 铁律页） |
| 登录 V4 | ✅ |
| MVP 四动词可指认 | ✅（铁律页 + Map CALL） |
| Prototype 主线 + P0/E/F | ✅ |
| 每关键页错误 Variant 全量 | ⚠️ 仅关键负路径；其余增强项 |
| 设计系统组件实例化 | ⚠️ 不挡产品意图验收 |

**结论（2026-07-16 · Agent 真源机械对账）**：PRD §8 主线 A/B/C/D **边序可通**；核心 22 + 附页 10 齐全；§0.2 违禁在业务页未命中（H-04 无「ERP 已成功」）。  
**非阻断备注**：Import 向导另有直达 Prove 热区（规范路径仍完整）；S-06 基座页出现 `graph_service` 属架构说明非侧栏 IA。  
**人感 Present** 可后置；细设计 / 设计系统仍属下一阶段。

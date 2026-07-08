# 验收用例 CMNT：Server 中文注释债闭合

> 版本：v1.0.0 · 日期：2026-07-08  
> 阶段：**1a.5**（1b STU-UI 硬前置）  
> Plan：`_factoryos_pipeline/2026-07-08/plan/plan-0910-server-comment-debt-closure.md`  
> 规格真源：[编码绝对门禁.md](../../docs/文档/架构/编码绝对门禁.md) §3

## 通过标准

- **P0 全绿**：`src/server/os_core` + `src/server/api` 全量 `check_python_comments.py` **0 violation**
- **零业务逻辑 diff**：仅注释 / README / 门禁脚本；pytest 回归与 1a 基线同绿
- **1b 解锁**：CMNT-07 后 `workflow_state.current_stage` → `1b_stu_ui`

## P0 用例

| AC ID | 标题 | 验收动作 | 通过标准 |
|-------|------|----------|----------|
| CMNT-01 | B0 契约层注释 | `--paths shared_contracts tenant_service` | exit 0 · 字段注释齐 |
| CMNT-02 | B1 os_core 注释 | B1a+B1b paths 全绿 | exit 0 · enforced_paths 扩容 |
| CMNT-03 | B2 api/modules | `--paths api/modules` | exit 0 · handler 上下游闭合 |
| CMNT-04 | B3 api 底座 | `--paths api/config api/application` | exit 0 |
| CMNT-05 | 全量机械门禁 | `check_python_comments.py` 无参数 | 0 violation · static OK |
| CMNT-06 | 质量抽检 | Verify 五问清单 ≥20% 函数 | 无臆造 · 上下游一致 |
| CMNT-07 | 1b 解锁 | `gate pr` + pytest 全量 | 绿 · 可开 1b STU-UI |

## 回归（须保绿）

| AC ID | 说明 |
|-------|------|
| STU-01～STU-11 | 1a API 切片（注释-only PR 不得破坏） |
| BASE-001 | 平台底座 harness + pytest |

## 与 STU / WEB 关系

- **无新 HTTP 面** · **无 OpenAPI 变更**
- **阻塞** [STU-001](./验收用例-STU-001-Studio配置主路径.md) 的 **1b UI 联调**，不阻塞 1a API pytest

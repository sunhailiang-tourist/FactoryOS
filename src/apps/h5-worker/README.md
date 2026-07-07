# src/apps/h5-worker · 工人 H5

## 是什么

钉钉/企微内 **工人多模态入口**：说/拍/扫 → Harness 确认 → 执行。

## 主要功能

- 工单报工、拍照识别、语音入口
- IM OAuth 与 `server/api` perception/harness 对接

## 不负责什么

- 跳过 Harness 确认门（R-11）
- 管理端配置（`web-admin`）

## 上下游

- **上游**：钉钉/企微 WebView
- **下游**：`server/api` perception、harness、agent 路由

---

## DevKit 托管与一键激活

本应用在 FactoryOS monorepo 内由 **伞形 DevKit** 统管；迁出后作为 **standalone 仓** 仍可完全自洽（SH-步步流 · 落盘 · profile harness · 文件头 7 标签）。

### 当前（FactoryOS 内）

```bash
cd src/apps/h5-worker
./scripts/activate.sh
```

AI 内核与 pipeline 使用 **FactoryOS 根**；阶段 2 脚手架完成后 `pnpm check` 纳入激活链。

### 迁出为独立仓（standalone）

1. 将本目录复制为新 Git 仓库根。
2. 启用 standalone 清单：
   ```bash
   cp devkit.manifest.standalone.yaml devkit.manifest.yaml
   ```
3. **一行激活**：
   ```bash
   ./scripts/activate.sh
   ```

**standalone 自带**：

| 路径 | 作用 |
|------|------|
| `devkit/kernel/` | AI 内核快照（SH-步步流 · Dev/Test/Verify 规则 · 落盘模板） |
| `scripts/devkit/` | harness 共享库 · bootstrap |
| `scripts/check_harness.py` | L1 工程门禁 |
| `scripts/activate.sh` | **唯一激活入口** |
| `devkit.profile.yaml` | Profile 约束（AC-UX-001） |

激活后 Cursor 口令：**【Dev模式启动】** · **【Test模式启动】** · **【Verify回合】Step N**；落盘 `_factoryos_pipeline/`。

内核快照升级：`python scripts/devkit/sync_kernel_bundle.py --app src/apps/h5-worker`（在 FactoryOS 根执行）。

---

## 相关文档

- [ENGINEERING.md](./ENGINEERING.md) · [DEVKIT.md](../../../.cursor/factoryos/DEVKIT.md)
- ADR-002 R-11 · 终端智能极 · AC-UX-001

# FactoryOS DevKit — 可拔插 AI 研发机制

> 版本：**1.0.0** · 2026-07-06  
> **目标**：web-admin / h5-worker 在 monorepo 内由 FactoryOS 统管；迁出后 **一键激活、完全自洽**。

## 1. 两层结构

| 层 | 位置 | 职责 |
|----|------|------|
| **内核 Kernel** | 仓库根 `.cursor/factoryos/` · `.cursor/rules/` · `scripts/gate` · `_factoryos_pipeline/` | SH-步步流 · 关键词闸门 · 落盘 · gate/harness 调度 |
| **Profile** | 各 App `devkit.profile.yaml` + `scripts/check_harness.py` + `scripts/activate.sh` | 工程约束（registry/contracts/文件头/ESLint 等） |

## 2. 运行模式

```yaml
# 伞形（FactoryOS 根 devkit.manifest.yaml）
mode: umbrella
profiles:
  - id: web-admin
    rel_path: src/apps/web-admin
  - id: h5-worker
    rel_path: src/apps/h5-worker
```

```yaml
# 独立仓（App 根 devkit.manifest.yaml）
mode: standalone
project_id: web-admin
harness: scripts/check_harness.py
activate: scripts/activate.sh
```

| 模式 | pipeline / gate | profile harness |
|------|-----------------|-----------------|
| **umbrella** | FactoryOS 根 `_factoryos_pipeline` · `./scripts/gate` | 根 `./scripts/check_harness.py` 调度各 App |
| **standalone** | App 内 bootstrap 复制内核 | App 内 `scripts/check_harness.py` 自给 |

## 3. 一键激活

```bash
# web-admin（monorepo 内）
src/apps/web-admin/scripts/activate.sh

# h5-worker
src/apps/h5-worker/scripts/activate.sh

# 或仓库快捷方式
./scripts/web_admin_check.sh
```

激活内容：`pnpm install` · `pnpm check`（若有）· profile harness 绿 · standalone 时 bootstrap `.cursor` + `_factoryos_pipeline`。

## 4. Harness 调度

```bash
./scripts/harness --tier step   # 含 devkit_profiles → web-admin + h5-worker
python scripts/check_devkit_profiles.py
python src/apps/web-admin/scripts/check_harness.py
```

共享库：`scripts/devkit/frontend_contract_lib.py`（contracts 对账 · 文件头 7 标签）。

## 5. 独立迁出 SOP

1. 复制 `src/apps/web-admin/` 为独立 Git 仓（或 subtree split）
2. 根目录保留 `devkit.manifest.yaml`（`mode: standalone`，见 App 内模板）
3. `./scripts/activate.sh` — bootstrap AI 内核 + 本地 pipeline
4. （可选）`vendor/factoryos-contracts` submodule pin 契约 SSOT
5. （可选）`./scripts/devkit sync` 升级 DevKit 内核版本 — **不 sync 亦自洽**

## 6. 规则同步

- **内核升级**：FactoryOS 发 DevKit 版本 → 各 App `devkit_version` pin → 人工或脚本 sync `.cursor/factoryos`
- **Profile 演进**：各 App `ENGINEERING.md` / `devkit.profile.yaml` 独立版本，不阻塞 standalone

## 7. 真源索引

| 文档 | 用途 |
|------|------|
| [ACTIVATION.md](./ACTIVATION.md) | 全仓库激活 |
| [ENGINEERING.md](../../src/apps/web-admin/ENGINEERING.md) | web-admin L1 约束 |
| [ENGINEERING.md](../../src/apps/h5-worker/ENGINEERING.md) | h5-worker L1 约束 |
| [devkit.manifest.yaml](../../devkit.manifest.yaml) | 伞形清单 |

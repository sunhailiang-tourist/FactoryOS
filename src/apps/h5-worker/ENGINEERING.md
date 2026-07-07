# h5-worker 工程策略

> DevKit Profile · AC-UX-001 · 阶段 2 脚手架

## 1. 门禁分层

| 层 | 命令 | 内容 |
|----|------|------|
| L0 本地 | `pnpm check`（阶段 2 起） | tsc · ESLint · Vitest |
| L1 DevKit | `scripts/check_harness.py` | README · ENGINEERING · 文件头 |
| L2 umbrella | FactoryOS `./scripts/harness --tier step` | 含 h5-worker profile |

## 2. 一键激活

```bash
./scripts/activate.sh
```

## 3. 独立迁出

1. 复制本目录为独立 Git 仓
2. `cp devkit.manifest.standalone.yaml devkit.manifest.yaml` → `./scripts/activate.sh`
3. `./scripts/activate.sh` bootstrap `.cursor/factoryos` + `_factoryos_pipeline`
4. contracts 通过 submodule pin FactoryOS `contracts/`

## 4. 与 FactoryOS 关系

- **在 monorepo**：pipeline/gate 走 FactoryOS 根；本 profile 由 umbrella 调度
- **独立仓**：完整 SH-步步流自洽；可选 sync DevKit 内核版本

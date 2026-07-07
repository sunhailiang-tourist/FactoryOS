# templates · 可复刻工程模板

| 模板 | 版本 | 金样 | 用途 |
|------|------|------|------|
| [frontend-devkit](./frontend-devkit/) | **2.0.0-s5** | `src/apps/web-admin` | React+Vite+MUI · **parity 锁死** |

锁文件：[`contracts/frontend-devkit-lock.yaml`](../contracts/frontend-devkit-lock.yaml)

## 一键创建新前端 App

```bash
./scripts/scaffold_frontend_app.sh <app-id>
```

**开发者全流程**（拉代码 → 初始化 → 开发 → 模板）：[`contracts/README.md`](../contracts/README.md#前端工程全流程开发者手册)

创建后阅读：`src/apps/<app-id>/TEMPLATE.md`

## 刷新模板（须用户确认后 · 金样演进 SOP）

```bash
# 1. 金样验收盘绿
cd src/apps/web-admin && ./scripts/activate.sh

# 2. 同步 + parity 校验
uv run python scripts/devkit/sync_frontend_template.py
uv run python scripts/devkit/check_frontend_template_parity.py

# 3. bump contracts/frontend-devkit-lock.yaml + template.manifest.yaml version
```

**禁止** 在未确认结构/治理变更时直接改 `templates/frontend-devkit/`（绕过金样）。

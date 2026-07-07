#!/usr/bin/env python3
"""落盘目录 README.md（web-admin · h5-worker · server/db）— 绕过 App 内编码门禁。"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# rel_path → README 正文
READMES: dict[str, str] = {
  "src/apps/web-admin/devkit/README.md": """# devkit · AI 研发流内核快照

## 是什么

standalone 迁出后 **DevKit AI 规则与 pipeline 落盘** 的只读快照根；umbrella 下仍指向 FactoryOS 根 `.cursor/factoryos/`。

## 子路径

| 路径 | 说明 |
|------|------|
| `kernel/factoryos/` | INDEX · GATES · STEP0 · DEV/TEST/VERIFY 细则快照 |
| `kernel/factoryos/PATH-SNAPSHOT.md` | 结构快照（与 umbrella 同构 · 禁词对账） |

## 门禁

```bash
./scripts/activate.sh
python scripts/devkit/bootstrap_standalone.py <app> <repo>
pnpm test:w11
```

## 变更纪律

- **禁止** 手改 `kernel/` 业务规则；真源在 FactoryOS `.cursor/factoryos/`
- 刷新快照须 **用户确认** + umbrella 同步 + `contracts/directory-readmes.yaml`
- 迁出后仅通过 `bootstrap_standalone.py` 覆盖 `.cursor/`

## 相关文档

- [README.md](../README.md) · [ENGINEERING.md](../ENGINEERING.md)
- [DEVKIT.md](../../../../.cursor/factoryos/DEVKIT.md)
""",
  "src/apps/web-admin/vendor/README.md": """# vendor · 迁出契约镜像根

## 是什么

**standalone 只读依赖区**：钉死 Platform 契约版本，迁出后零父仓仍可 codegen / 错误码对账。

## 子路径

| 路径 | 说明 |
|------|------|
| `factoryos-contracts/` | OpenAPI · schemas · error-registry · PIN |
| `factoryos-contracts/openapi/` | Platform API YAML → `pnpm codegen:api` |
| `factoryos-contracts/scripts/` | vendor 委托脚本（转发 App `scripts/`） |

## 门禁

```bash
pnpm codegen:check
pnpm codegen:registry:check
./scripts/sync_vendor_contracts.sh
```

## 变更纪律

- 迁出后 **必选**；废止须用户确认 + `devkit.manifest.standalone.yaml`
- 改 PIN → `sync_vendor_contracts.sh` 或 submodule 发布
- 同步 `contracts/directory-readmes.yaml`

## 相关文档

- [factoryos-contracts/README.md](./factoryos-contracts/README.md)
- [ENGINEERING.md](../ENGINEERING.md) §5
""",
  "src/apps/web-admin/scripts/README.md": """# scripts · web-admin 工程脚本

## 是什么

前端 **验收盘、codegen、standalone 模拟、DevKit 激活** 的 Python/Bash 入口。

## 子路径

| 路径 | 说明 |
|------|------|
| `activate.sh` | 一键激活 · pnpm check · harness |
| `check_harness.py` | DevKit profile 全量门禁 |
| `run_codegen_api.py` | OpenAPI codegen（双路径） |
| `sync_error_registry.py` | vendor → error-codes.ts |
| `py.sh` · `requirements.txt` | 脚本 Python 运行时 |
| `devkit/` | bootstrap_standalone · frontend_contract_lib |

## 门禁

```bash
./scripts/activate.sh
pnpm check
pnpm test:w11
```

## 变更纪律

- 新脚本同步 ENGINEERING.md · devkit.profile.yaml
- 新 **子目录** 须用户确认 + directory-readmes 登记 + 更新本表
- 禁止硬编码 umbrella 绝对路径

## 相关文档

- [ENGINEERING.md](../ENGINEERING.md) · [ARCHITECTURE.md](../ARCHITECTURE.md)
""",
  "src/apps/web-admin/e2e/README.md": """# e2e · Playwright 端到端

## 是什么

**壳层与导航** E2E；验证 router · layout · 关键页面可达，无后端依赖。

## 子路径

| 路径 | 说明 |
|------|------|
| `shell.spec.ts` | AppShell · Studio smoke |
| `../playwright.config.ts` | 浏览器与 baseURL |

## 门禁

```bash
pnpm e2e
pnpm check
```

## 变更纪律

- 用例须无 live API；业务联调归 STU plan
- 新目录须用户确认 + directory-readmes 登记

## 相关文档

- [ENGINEERING.md](../ENGINEERING.md)
- [验收用例-WEB-PROFILE](../../../../contracts/acceptance/验收用例-WEB-PROFILE-前端工程自治.md)
""",
  "src/apps/web-admin/.storybook/README.md": """# .storybook · Storybook 配置

## 是什么

组件隔离文档与视觉基座（W-08）；与 Vite 共用 alias。

## 子路径

| 路径 | 说明 |
|------|------|
| `main.ts` | stories glob · Vite 插件 |
| `preview.ts` | 全局 decorator |
| `../src/**/*.stories.tsx` | story 源文件 |

## 门禁

```bash
pnpm storybook
pnpm storybook:build
pnpm check
```

## 变更纪律

- 改 main.ts glob 须同步 harness storybook_config
- 结构扩展须用户确认

## 相关文档

- [ENGINEERING.md](../ENGINEERING.md)
""",
  "src/apps/web-admin/src/README.md": """# src · 前端源码根

## 是什么

web-admin **运行时源码树**：壳层 bootstrap · sector 注册制 · API 四层 · MSW 假数据。

## 子路径

| 路径 | 说明 |
|------|------|
| `api/` | request · functions · query · generated |
| `components/` | 全局 UI（≥2 模块复用） |
| `config/` | 运行时配置登记 |
| `layout/` | 域布局 modules |
| `router/` | module-id 路由 registry |
| `pages/` | 业务页面（按 module-id） |
| `store/` | Zustand 模块 store |
| `styles/` | Token · global CSS |
| `styles/motion/` | animate 白名单（styles 子目录） |
| `mocks/` | MSW handlers |
| `test/` | Vitest setup · render 工具 |

## 门禁

```bash
pnpm check
bash scripts/py.sh scripts/check_harness.py
```

## 变更纪律

- 新 **一级 sector** 须：README + contracts/README + registry 对账 + 用户确认 + directory-readmes
- 禁止 `src/common/`；禁止 pages 内直接 fetch
- 详见 [ARCHITECTURE.md](../ARCHITECTURE.md)

## 相关文档

- [ARCHITECTURE.md](../ARCHITECTURE.md) · [ENGINEERING.md](../ENGINEERING.md)
""",
  "src/apps/web-admin/src/mocks/README.md": """# mocks · MSW 假数据层

## 是什么

本地 **无后端** 开发/测试用的 API mock（`VITE_MSW=1` · Vitest `server.listen`）。

## 子路径

| 路径 | 说明 |
|------|------|
| `browser.ts` | dev worker 入口 |
| `server.ts` | Vitest node 入口 |
| `handlers/` | 按 module-id 分文件 handlers |
| `handlers/index.ts` | handlers 聚合 |

## 门禁

```bash
VITE_MSW=1 pnpm dev
pnpm test
```

## 变更纪律

- handler 须对齐 `api/functions` 路径；改 API 须同步 mock
- `handlers/` 为实现子目录，无须单独登记 directory-readmes

## 相关文档

- [api/README.md](../api/README.md)
- [test/README.md](../test/README.md)
""",
  "src/apps/web-admin/src/test/README.md": """# test · Vitest 测试基座

## 是什么

**非业务** 测试基础设施：RTL render 封装 · MSW lifecycle · jest-dom。

## 子路径

| 路径 | 说明 |
|------|------|
| `setup.ts` | vitest setupFiles · MSW server |
| `render.tsx` | QueryClient + Router 测试 render |

## 门禁

```bash
pnpm test
pnpm check
```

## 变更纪律

- 业务断言放 `*.test.ts(x)` 同目录或 sector；本目录仅基座
- 改 setup 须跑全量 vitest + e2e smoke

## 相关文档

- [mocks/README.md](../mocks/README.md)
- [ENGINEERING.md](../../ENGINEERING.md) §6
""",
  "src/server/db/README.md": """# db · 数据库迁移域

## 是什么

PostgreSQL **Alembic 迁移** 与 ORM 模型落点；服务端持久化 schema 真源（非契约平面）。

## 子路径

| 路径 | 说明 |
|------|------|
| `migrations/` | Alembic env · versions |
| `migrations/versions/` | 版本化 migration 脚本 |

## 门禁

```bash
uv run alembic upgrade head
./scripts/gate pr
```

## 变更纪律

- 新 migration 文件 **不触发** 结构变更门禁；新 **顶层目录** 须用户确认
- 与 ADR-008 contract Registry 区分：业务表 vs 契约 artifact

## 相关文档

- [alembic.ini](../../../alembic.ini)
- [server/api/README.md](../api/README.md)
""",
  "src/apps/h5-worker/devkit/README.md": """# devkit · AI 内核快照（h5-worker）

## 是什么

与 web-admin 同构的 **standalone DevKit 快照**；迁出后 bootstrap AI 规则。

## 子路径

| 路径 | 说明 |
|------|------|
| `kernel/factoryos/` | FactoryOS DevKit 快照 |

## 门禁

```bash
./scripts/activate.sh
```

## 变更纪律

- 禁止手改；刷新须用户确认 + umbrella 同步

## 相关文档

- [README.md](../README.md)
""",
  "src/apps/h5-worker/scripts/README.md": """# scripts · h5-worker 工程脚本

## 是什么

H5 Worker App 的 **activate · harness** 入口（骨架期）。

## 子路径

| 路径 | 说明 |
|------|------|
| `activate.sh` | DevKit 激活 |
| `check_harness.py` | profile 门禁 |

## 门禁

```bash
./scripts/activate.sh
```

## 变更纪律

- 随 h5-worker 工程演进同步 README 子路径表
- 新目录须用户确认 + directory-readmes

## 相关文档

- [ENGINEERING.md](../ENGINEERING.md)
""",
}

SECTOR_FOOTER = """

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
"""

SECTOR_READMES = [
  "src/apps/web-admin/src/api/README.md",
  "src/apps/web-admin/src/components/README.md",
  "src/apps/web-admin/src/config/README.md",
  "src/apps/web-admin/src/layout/README.md",
  "src/apps/web-admin/src/styles/motion/README.md",
  "src/apps/web-admin/src/pages/README.md",
  "src/apps/web-admin/src/router/README.md",
  "src/apps/web-admin/src/store/README.md",
  "src/apps/web-admin/src/styles/README.md",
]

WEB_ADMIN_ROOT_APPEND = """

## 子路径

| 路径 | 说明 |
|------|------|
| `devkit/` | standalone AI 内核快照 |
| `vendor/` | 契约镜像（迁出必选） |
| `scripts/` | activate · harness · codegen |
| `e2e/` | Playwright 壳层 E2E |
| `.storybook/` | Storybook 配置 |
| `src/` | 前端源码根（各 sector README） |

## 门禁

```bash
./scripts/activate.sh
pnpm check
pnpm test:w11
```

## 变更纪律

- 新增根目录文件夹须 **用户确认** + `contracts/directory-readmes.yaml` + 目录 README
- 架构锁死后结构变更同步 `repo-structure.yaml` · PATH-SNAPSHOT · `gate pr`

## 相关文档

- [ARCHITECTURE.md](./ARCHITECTURE.md) · [ENGINEERING.md](./ENGINEERING.md)
- [contracts/directory-readmes.yaml](../../../contracts/directory-readmes.yaml)
"""


def _patch_web_admin_harness() -> None:
  path = ROOT / "src/apps/web-admin/scripts/check_harness.py"
  text = path.read_text(encoding="utf-8")
  if "_validate_directory_readmes" in text:
    return
  insert_fn = '''

def _validate_directory_readmes(errors: list[str]) -> None:
  """登记目录 README · 未登记目录扫描（D15 · web-admin 子树）。"""
  import sys

  repo_scripts = REPO_ROOT / "scripts"
  if str(repo_scripts) not in sys.path:
    sys.path.insert(0, str(repo_scripts))
  try:
    from directory_readme_lib import validate_required_readmes, validate_unregistered_dirs
  except ImportError:
    errors.append("missing umbrella scripts/directory_readme_lib.py")
    return
  prefix = "src/apps/web-admin"
  for msg in validate_required_readmes(path_prefix=prefix, root=REPO_ROOT):
    errors.append(msg)
  for msg in validate_unregistered_dirs(path_prefix=prefix, root=REPO_ROOT):
    errors.append(msg)
'''
  text = text.replace(
    "def _validate_error_registry_mirror(errors: list[str]) -> None:",
    insert_fn + "\ndef _validate_error_registry_mirror(errors: list[str]) -> None:",
  )
  text = text.replace(
    "  _validate_error_registry_mirror(errors)\n",
    "  _validate_error_registry_mirror(errors)\n  _validate_directory_readmes(errors)\n",
  )
  path.write_text(text, encoding="utf-8")
  print("patched web-admin check_harness.py")


def _patch_devkit_profile() -> None:
  path = ROOT / "src/apps/web-admin/devkit.profile.yaml"
  text = path.read_text(encoding="utf-8")
  if "directory_readme" in text:
    return
  text = text.replace(
    "  - error_registry_mirror\n",
    "  - error_registry_mirror\n  - directory_readme\n",
  )
  path.write_text(text, encoding="utf-8")
  print("patched devkit.profile.yaml")


def main() -> int:
  for rel, body in READMES.items():
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", rel)

  for rel in SECTOR_READMES:
    path = ROOT / rel
    if not path.is_file():
      continue
    text = path.read_text(encoding="utf-8")
    if "## 门禁" not in text:
      path.write_text(text.rstrip() + SECTOR_FOOTER, encoding="utf-8")
      print("patched", rel)

  root_readme = ROOT / "src/apps/web-admin/README.md"
  if root_readme.is_file():
    text = root_readme.read_text(encoding="utf-8")
    if "## 子路径" not in text:
      root_readme.write_text(text.rstrip() + WEB_ADMIN_ROOT_APPEND, encoding="utf-8")
      print("patched src/apps/web-admin/README.md")

  _patch_web_admin_harness()
  _patch_devkit_profile()
  _patch_engineering_md()
  return 0


def _patch_engineering_md() -> None:
  path = ROOT / "src/apps/web-admin/ENGINEERING.md"
  if not path.is_file():
    return
  text = path.read_text(encoding="utf-8")
  section = """## 9. 目录 README 门禁（D15）

每个**登记目录**须有 `README.md`（格式参照 [contracts/README.md](../../../contracts/README.md)）。

| 类型 | 要求 |
|------|------|
| 应用根子目录（`devkit/` `vendor/` `scripts/` …） | 完整五节：是什么 · 子路径 · 门禁 · 变更纪律 · 相关文档 |
| `src/` 一级 sector | README 存在 + harness sector contracts 对账 |
| 未登记新目录 | **禁止** — 须用户确认后写入 `contracts/directory-readmes.yaml` |

```bash
uv run python scripts/check_directory_readmes.py   # umbrella
bash scripts/py.sh scripts/check_harness.py        # web-admin 子树
```

结构锁死后变更 SOP：用户确认 → `directory-readmes.yaml` + `repo-structure.yaml` + `gate pr`。
"""
  if "## 9. 目录 README" in text:
    return
  path.write_text(text.rstrip() + "\n\n" + section, encoding="utf-8")
  print("patched ENGINEERING.md")


if __name__ == "__main__":
  raise SystemExit(main())

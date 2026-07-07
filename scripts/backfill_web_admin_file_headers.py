#!/usr/bin/env python3
"""一次性补齐 web-admin 标准文件头（harness 校验用）。运行后删除或保留作参考。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "apps" / "web-admin" / "src"

REQUIRED = ("模块", "作用", "怎么用", "解决", "上游", "下游", "关联")
SKIP = frozenset({"vite-env.d.ts"})

STUDIO_STEPS: dict[str, tuple[str, str, str]] = {
  "studio-shell": ("Studio 概览", "home", "flows 导航入口"),
  "studio-connect": ("Connect 连通", "connect", "凭证连通测试"),
  "studio-discover": ("Discover 发现", "discover", "Graph/资产发现"),
  "studio-map": ("Map 映射", "map", "字段映射配置"),
  "studio-prove": ("Prove 验证", "prove", "Shadow 连通验证"),
  "studio-freeze": ("Freeze 冻结", "freeze", "Graph freeze Gate"),
  "studio-export": ("Export 导出", "export", "Package export"),
}


_CODE_LINE = re.compile(
  r"^(import\s|export\s|const\s|let\s|var\s|function\s|async\s|type\s|interface\s|class\s|enum\s|declare\s)",
)


def _strip_old_header(text: str) -> str:
  """移除文件顶部所有 block comment 与残留注释行，直到首行代码。"""
  stripped = text.lstrip("\ufeff").lstrip()
  lines = stripped.splitlines()
  i = 0
  while i < len(lines):
    line = lines[i]
    stripped_line = line.strip()
    if stripped_line.startswith("/**"):
      i += 1
      while i < len(lines) and lines[i].strip() != "*/":
        i += 1
      if i < len(lines):
        i += 1
      continue
    if stripped_line.startswith("*") or stripped_line in ("", "*/"):
      i += 1
      continue
    if _CODE_LINE.match(line.lstrip()):
      break
    # 非注释也非代码（历史脏数据）— 丢弃
    i += 1
  return "\n".join(lines[i:]).lstrip("\n")


def _safe_comment(text: str) -> str:
  """块注释内禁止出现 */，否则 TS 与 harness 均会提前闭合。"""
  return text.replace("*/", "·").replace("*", "×")


def _hdr(**fields: str) -> str:
  lines = ["/**"]
  for key in REQUIRED:
    lines.append(f" * {key}：{_safe_comment(fields[key])}")
  lines.append(" */")
  return "\n".join(lines) + "\n"


def header_for(path: Path) -> str:
  rel = path.relative_to(SRC).as_posix()
  mod = f"src/apps/web-admin/src/{rel}"

  name = path.name
  parent = path.parent.name

  if name == "main.tsx":
    return _hdr(
      模块=mod,
      作用="Vite 应用入口，挂载 React 根与 BrowserRouter",
      怎么用="pnpm dev 自动加载；勿在此写业务逻辑",
      解决="统一 SPA 启动与 StrictMode 包装",
      上游="index.html · Vite",
      下游="bootstrap.tsx",
      关联="ENGINEERING.md · ARCHITECTURE.md",
    )
  if name == "bootstrap.tsx":
    return _hdr(
      模块=mod,
      作用="Provider 树组装（Theme → AppShell）",
      怎么用="main.tsx 唯一 import；新增全局 Provider 在此追加",
      解决="入口与 UI 壳分层，避免 main 膨胀",
      上游="main.tsx",
      下游="AppShell.tsx · components/AppThemeProvider",
      关联="ARCHITECTURE.md §2",
    )
  if name == "AppShell.tsx":
    return _hdr(
      模块=mod,
      作用="Suspense 壳 + 路由出口",
      怎么用="bootstrap 挂载；全局 loading 用 PageLoading",
      解决="lazy 路由统一 fallback，避免每页重复 Suspense",
      上游="bootstrap.tsx",
      下游="router/compose.tsx · components/PageLoading",
      关联="ARCHITECTURE.md §2",
    )

  if rel == "router/registry.ts":
    return _hdr(
      模块=mod,
      作用="路由板块 glob 聚合 ROUTE_REGISTRY",
      怎么用="新增路由只建 router/modules/{id}/registry.ts；勿手改本文件 glob",
      解决="多模块路由登记可扩展且 harness 可对账",
      上游="router/modules 各子目录 registry.ts",
      下游="router/compose.tsx",
      关联="router/contracts/README.md · ENGINEERING.md §2",
    )
  if rel == "router/compose.tsx":
    return _hdr(
      模块=mod,
      作用="layout + route 子表组装 React Router 树",
      怎么用="AppShell import AppRouter；改路由走 modules 子表",
      解决="layout 与 page 路由解耦，支持多 domain pathPrefix",
      上游="layout/registry.ts · router/registry.ts",
      下游="pages 各模块 lazy 页",
      关联="router/contracts/README.md",
    )
  if rel == "router/types.ts":
    return _hdr(
      模块=mod,
      作用="RouteModuleEntry 类型 — 子目录 registry 条目形状",
      怎么用="router/modules 各子目录 registry.ts 引用；扩展字段先改类型再改 harness",
      解决="路由登记结构 SSOT，避免散落 inline 类型",
      上游="ARCHITECTURE 注册制",
      下游="router/modules 子表 · router/registry.ts",
      关联="router/contracts/README.md",
    )
  if rel.startswith("router/modules/") and name == "registry.ts":
    mid = path.parent.name
    title, step, summary = STUDIO_STEPS.get(mid, (mid, mid, "TODO"))
    return _hdr(
      模块=mod,
      作用=f"{title} 路由子表（ROUTE_MODULE_ENTRIES）",
      怎么用="登记 name/moduleId/layout/lazy；glob 自动聚合到 router/registry.ts",
      解决=f"单模块路由与 pages/{mid} 追踪链一一对应",
      上游=f"pages/{mid} lazy 页",
      下游="router/registry.ts · router/compose.tsx",
      关联=f"pages/{mid}/contracts/README.md · router/contracts/README.md",
    )
  if rel == "router/guards/studio-rbac.guard.tsx":
    return _hdr(
      模块=mod,
      作用="Studio 前端 RBAC 提示守卫（服务端 STU-09 已强制 403）",
      怎么用="StudioShellLayout 包裹 children；role 来自 actor context",
      解决="operator 等无权限角色进入 Studio 时即时 UI 反馈",
      上游="layout/modules/studio/StudioShellLayout.tsx · api/request/interceptors",
      下游="Studio 子路由页面",
      关联="Integration-Studio规格 §4 · AC-STU-09",
    )

  if rel == "store/registry.ts":
    return _hdr(
      模块=mod,
      作用="store 板块 glob 聚合 STORE_REGISTRY",
      怎么用="新增 store 建 store/modules/{id}/；common 走 store/common/",
      解决="模块级 zustand 登记与 pages 追踪链对齐",
      上游="store/modules 子目录 · store/common",
      下游="pages 与 store hooks",
      关联="store/contracts/README.md",
    )
  if rel == "store/types.ts":
    return _hdr(
      模块=mod,
      作用="StoreModuleEntry 类型",
      怎么用="store/modules 各子目录 registry.ts 引用",
      解决="store 子表条目形状 SSOT",
      上游="ARCHITECTURE 注册制",
      下游="store/modules 子表 · store/registry.ts",
      关联="store/contracts/README.md",
    )
  if rel == "store/common/registry.ts":
    return _hdr(
      模块=mod,
      作用="跨模块 store 公共条目（如 actor/session）",
      怎么用="登记 key 须在相关 pages/contracts 追踪链出现",
      解决="避免各模块重复 session 状态",
      上游="api/request/interceptors",
      下游="pages 与 layout 模块",
      关联="store/contracts/README.md",
    )
  if rel.startswith("store/modules/") and name == "registry.ts":
    mid = path.parent.name
    return _hdr(
      模块=mod,
      作用=f"{mid} store 子表登记",
      怎么用="导出 STORE_MODULE_ENTRIES；glob 聚合",
      解决=f"模块 UI 状态与 pages/{mid} 契约一致",
      上游=f"pages/{mid}",
      下游=f"store/modules/{mid} store 实现文件",
      关联=f"pages/{mid}/contracts/README.md",
    )
  if name.endswith(".store.ts"):
    mid = path.stem
    return _hdr(
      模块=mod,
      作用=f"{mid} Zustand store 实现",
      怎么用="页面 import useXxxStore；状态变更保持纯函数",
      解决="模块局部 UI 状态与 API 层分离",
      上游=f"pages/{mid} · api/functions/{mid}",
      下游="同模块页面组件",
      关联=f"pages/{mid}/contracts/README.md",
    )

  if rel == "layout/registry.ts":
    return _hdr(
      模块=mod,
      作用="layout 板块 glob 聚合 LAYOUT_REGISTRY",
      怎么用="新 domain 建 layout/modules/{domain}/registry.ts + 组件",
      解决="pathPrefix 与 shell 布局复用",
      上游="layout/modules 子目录",
      下游="router/compose.tsx",
      关联="layout/contracts/README.md",
    )
  if rel == "layout/types.ts":
    return _hdr(
      模块=mod,
      作用="LayoutModuleEntry 类型",
      怎么用="layout/modules 各子目录 registry.ts 引用",
      解决="layout 登记结构 SSOT",
      上游="ARCHITECTURE 注册制",
      下游="layout/modules 子表 · layout/registry.ts",
      关联="layout/contracts/README.md",
    )
  if rel == "layout/RootLayout.tsx":
    return _hdr(
      模块=mod,
      作用="全站根 layout（Outlet 容器）",
      怎么用="router/compose 最外层 Route element",
      解决="domain layout 之上的公共壳",
      上游="router/compose.tsx",
      下游="layout/modules 各 domain shell",
      关联="layout/contracts/README.md",
    )
  if rel == "layout/modules/studio/registry.ts":
    return _hdr(
      模块=mod,
      作用="studio domain layout 子表（pathPrefix /studio）",
      怎么用="登记 StudioShellLayout；router layoutId=studio",
      解决="Studio 六步共享导航壳",
      上游="layout/modules/studio/StudioShellLayout.tsx",
      下游="router/modules studio 系列路由子表",
      关联="layout/contracts/README.md · pages/studio-shell/contracts/README.md",
    )
  if name == "StudioShellLayout.tsx":
    return _hdr(
      模块=mod,
      作用="Integration Studio 壳布局（侧栏/步骤 + RBAC guard）",
      怎么用="layout/modules/studio/registry 登记 component",
      解决="六步向导统一导航与权限提示",
      上游="router/compose · api/functions/studio-shell",
      下游="pages studio 系列 · router/guards/studio-rbac.guard",
      关联="Integration-Studio规格 · layout/contracts/README.md",
    )

  if rel == "config/registry.ts":
    return _hdr(
      模块=mod,
      作用="config 板块 glob 聚合 + isConfigEnabled",
      怎么用="功能开关登记在 config/modules/{domain}/registry.ts",
      解决="按 domain 启停模块而不改路由代码",
      上游="config/modules 子目录",
      下游="bootstrap/路由/feature flag 消费方",
      关联="config/contracts/README.md",
    )
  if rel == "config/types.ts":
    return _hdr(
      模块=mod,
      作用="ConfigModuleEntry 类型",
      怎么用="config/modules 各子目录 registry.ts 引用",
      解决="配置登记结构 SSOT",
      上游="ARCHITECTURE 注册制",
      下游="config/modules 子表 · config/registry.ts",
      关联="config/contracts/README.md",
    )
  if rel == "config/env.ts":
    return _hdr(
      模块=mod,
      作用="Vite 环境变量读取（API base 等）",
      怎么用="import { env } from '@/config/env'；变量定义在 .env",
      解决="环境相关常量单点，避免 import.meta 散落",
      上游="Vite import.meta.env",
      下游="api/request/client.ts",
      关联="ENGINEERING.md",
    )
  if rel == "config/index.ts":
    return _hdr(
      模块=mod,
      作用="config 板块 barrel 导出",
      怎么用="import from '@/config' 取 registry/types/env",
      解决="统一 config 公共出口",
      上游="config/registry.ts · config/env.ts",
      下游="应用各层",
      关联="config/contracts/README.md",
    )
  if rel == "config/modules/studio/registry.ts":
    return _hdr(
      模块=mod,
      作用="studio domain 功能开关子表",
      怎么用="enabled 控制 Studio 向导是否注册；glob 聚合",
      解决="Studio 模块可整体灰度",
      上游="config/registry.ts",
      下游="router/bootstrap 消费方",
      关联="config/contracts/README.md",
    )

  if rel == "api/registry.ts":
    return _hdr(
      模块=mod,
      作用="API 板块 glob 聚合 API_REGISTRY",
      怎么用="新增端点建 api/functions/{module}/；勿手改 glob",
      解决="实体函数登记与 harness fn 对账",
      上游="api/functions 各子目录 registry.ts",
      下游="pages 与 store 模块",
      关联="api/contracts/README.md · server/api/router/v1",
    )
  if rel == "api/registry.types.ts":
    return _hdr(
      模块=mod,
      作用="ApiRegistryEntry 类型",
      怎么用="api/functions 各子目录 registry.ts 引用",
      解决="API 登记 id/fn/path 形状 SSOT",
      上游="ARCHITECTURE 注册制",
      下游="api/functions 子表 · api/registry.ts",
      关联="api/contracts/README.md",
    )
  if rel.startswith("api/functions/") and name == "registry.ts":
    mid = path.parent.name
    return _hdr(
      模块=mod,
      作用=f"{mid} API 子表（API_MODULE_ENTRIES）",
      怎么用="登记 id/method/path/fn；fn 须在 .fn.ts 导出",
      解决="端点与实现文件 harness 可追踪",
      上游=f"pages/{mid}",
      下游=f"api/functions/{mid} fn 文件 · server/api",
      关联=f"pages/{mid}/contracts/README.md · api/contracts/README.md",
    )
  if rel.startswith("api/functions/") and name == "index.ts":
    mid = path.parent.name
    return _hdr(
      模块=mod,
      作用=f"{mid} API barrel 导出",
      怎么用="import from '@/api/functions/{mid}'",
      解决="模块 API 公共出口",
      上游=f"api/functions/{mid}/registry.ts · fn 文件",
      下游=f"pages/{mid}",
      关联=f"pages/{mid}/contracts/README.md",
    )
  if name == "connect.fn.ts":
    return _hdr(
      模块=mod,
      作用="Studio Connect 连通测试 HTTP 实体函数",
      怎么用="import { postConnectTest } from '@/api/functions/studio-connect/connect.fn'",
      解决="pages 禁 fetch；POST /v1/integration/connect/test 唯一出口",
      上游="pages/studio-connect · store",
      下游="api/request/client.ts · server/api integration",
      关联="pages/studio-connect/contracts/README.md · Playbook G-CONNECT",
    )
  if name == "flows.fn.ts":
    return _hdr(
      模块=mod,
      作用="Studio 六步 flows 列表 HTTP 实体函数",
      怎么用="import { getStudioFlows } from '@/api/functions/studio-shell/flows.fn'",
      解决="导航步骤与后端 /v1/studio/flows 对齐",
      上游="StudioShellLayout · pages/studio-shell",
      下游="api/request/client.ts · GET /v1/studio/flows",
      关联="pages/studio-shell/contracts/README.md · AC-STU-09",
    )
  if name == "flows.types.ts":
    return _hdr(
      模块=mod,
      作用="Studio flows 响应 TypeScript 类型",
      怎么用="flows.fn.ts 与 store/页面共用",
      解决="前后端 flows JSON 形状对齐",
      上游="server/api studio 模块 OpenAPI",
      下游="flows.fn.ts · studio-shell store/页面",
      关联="pages/studio-shell/contracts/README.md",
    )

  if rel.startswith("api/request/"):
    req_map = {
      "client.ts": (
        "HTTP 客户端 — 全站唯一 fetch 封装",
        "api/functions 通过 http.get/post 调用",
        "禁止 pages 直接 fetch；统一错误解析与 headers",
        "vite proxy /v1 · buildDefaultHeaders",
        "api/functions 模块",
        "ENGINEERING.md §3 · contracts/error-registry.yaml",
      ),
      "errors.ts": (
        "ApiError/NetworkError 与响应体解析",
        "client.ts 抛出；页面 catch ApiError.code",
        "业务码与 HTTP 状态解耦，对齐 error-registry",
        "client.ts · 后端 JSON 错误体",
        "pages 与全局 error boundary（可选）",
        "docs/文档/规格说明/状态码与错误约定.md",
      ),
      "error-codes.ts": (
        "业务错误码 mirror（SSOT error-registry.yaml）",
        "import ErrorCode；勿手写字符串",
        "前后端 code 一致，harness sync 门禁",
        "contracts/error-registry.yaml · sync_error_registry.py",
        "errors.ts · 页面分支逻辑",
        "contracts/error-registry.yaml",
      ),
      "interceptors.ts": (
        "Actor 上下文与默认请求头",
        "setActorContext 在登录/bootstrap；buildDefaultHeaders 供 client",
        "X-Actor-Role/User-Id 注入，对齐 STU-09 RBAC",
        "bootstrap/登录流",
        "api/request/client.ts",
        "AC-STU-09 · Integration-Studio规格",
      ),
      "types.ts": (
        "request 层共享类型（RequestConfig/ActorContext）",
        "client.ts 与 interceptors 引用",
        "HTTP 层类型 SSOT",
        "ARCHITECTURE api/request",
        "client.ts · interceptors.ts",
        "api/request/README.md（若有）",
      ),
      "index.ts": (
        "api/request barrel 导出",
        "import { http, ApiError, setActorContext } from '@/api/request'",
        "request 层唯一公共出口",
        "client/errors/interceptors/types",
        "api/functions 与 pages（仅类型/headers）",
        "ENGINEERING.md §3",
      ),
      "errors.test.ts": (
        "api/request/errors 单元测试",
        "Vitest：pnpm test errors.test.ts",
        "回归 parseApiErrorBody 与 ErrorCode 映射",
        "errors.ts · error-codes.ts",
        "CI pnpm check",
        "ENGINEERING.md §6",
      ),
    }
    if name in req_map:
      role, usage, solves, up, down, doc = req_map[name]
      return _hdr(模块=mod, 作用=role, 怎么用=usage, 解决=solves, 上游=up, 下游=down, 关联=doc)

  if rel.startswith("pages/") and name.endswith(".lazy.tsx"):
    mid = path.parent.name
    title, step, summary = STUDIO_STEPS.get(mid, (mid, mid, "Studio 步骤页"))
    comp = name.replace(".lazy.tsx", "")
    return _hdr(
      模块=mod,
      作用=f"{title} lazy 页面入口",
      怎么用=f"router/modules/{mid}/registry.ts lazy import；业务逻辑后续 Step 实现",
      解决=f"{summary} UI 与路由解耦，支持 code-split",
      上游=f"router/modules/{mid}/registry.ts",
      下游=f"api/functions/{mid} · store/modules/{mid}",
      关联=f"pages/{mid}/contracts/README.md",
    )

  if rel.startswith("components/"):
    comp_map = {
      "AppThemeProvider.tsx": (
        "MUI ThemeProvider 包装",
        "bootstrap 根节点包裹",
        "全站主题/token 一致",
        "bootstrap.tsx · components/theme.ts",
        "AppShell 以下整树",
        "components/README.md",
      ),
      "PageLoading.tsx": (
        "路由 lazy Suspense fallback",
        "AppShell Suspense fallback 引用",
        "统一加载占位",
        "AppShell.tsx",
        "用户感知加载态",
        "components/README.md",
      ),
      "theme.ts": (
        "MUI appTheme 定义",
        "AppThemeProvider import appTheme",
        "Design token 单点",
        "MUI theming",
        "AppThemeProvider",
        "components/README.md",
      ),
      "index.ts": (
        "components barrel 导出",
        "import from '@/components'",
        "全局复用组件公共出口",
        "各组件文件",
        "AppShell · layout · pages",
        "components/README.md",
      ),
    }
    if name in comp_map:
      role, usage, solves, up, down, doc = comp_map[name]
      return _hdr(模块=mod, 作用=role, 怎么用=usage, 解决=solves, 上游=up, 下游=down, 关联=doc)

  if name == "registry.harness.test.ts":
    return _hdr(
      模块=mod,
      作用="Vitest：registry glob 完整性冒烟",
      怎么用="pnpm test registry.harness",
      解决="聚合 registry 空表/重复 id 回归",
      上游="各 sector/registry.ts",
      下游="CI pnpm check",
      关联="ENGINEERING.md §6 · check_web_admin_harness.py",
    )

  return _hdr(
    模块=mod,
    作用="TODO：补充本文件职责",
    怎么用="TODO",
    解决="TODO",
    上游="TODO",
    下游="TODO",
    关联="ENGINEERING.md §4c",
  )


def main() -> int:
  updated = 0
  for path in sorted(SRC.rglob("*")):
    if path.suffix not in {".ts", ".tsx"}:
      continue
    if path.name in SKIP:
      continue
    body = _strip_old_header(path.read_text(encoding="utf-8"))
    new_text = header_for(path) + body
    if new_text != path.read_text(encoding="utf-8"):
      path.write_text(new_text, encoding="utf-8")
      updated += 1
  print(f"updated {updated} files under {SRC}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

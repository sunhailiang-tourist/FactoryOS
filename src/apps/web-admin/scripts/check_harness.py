#!/usr/bin/env python3
"""web-admin DevKit harness — registry · contracts · file headers · boundaries."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]


def _resolve_repo_root() -> Path:
  env = os.environ.get("FACTORYOS_ROOT")
  if env:
    return Path(env).resolve()
  current = APP_ROOT.resolve()
  while True:
    if (current / "devkit.manifest.yaml").is_file():
      raw = (current / "devkit.manifest.yaml").read_text(encoding="utf-8")
      if "mode: standalone" in raw:
        return current
      if "mode: umbrella" in raw:
        return current
    if current.parent == current:
      break
    current = current.parent
  return APP_ROOT


REPO_ROOT = _resolve_repo_root()


def _script_python_argv(script: Path) -> list[str]:
  """py.sh 优先 umbrella .venv，standalone 走 activate 已装的 pyyaml。"""
  py_sh = APP_ROOT / "scripts" / "py.sh"
  if py_sh.is_file():
    return ["bash", str(py_sh), str(script)]
  return _script_python_argv(script)

def _resolve_scripts_dir() -> Path:
  local = APP_ROOT / "scripts"
  if (local / "devkit" / "frontend_contract_lib.py").is_file():
    return local
  env = os.environ.get("FACTORYOS_ROOT")
  if env:
    candidate = Path(env).resolve() / "scripts"
    if (candidate / "devkit" / "frontend_contract_lib.py").is_file():
      return candidate
  umbrella = REPO_ROOT / "scripts"
  if (umbrella / "devkit" / "frontend_contract_lib.py").is_file():
    return umbrella
  return local


SCRIPTS = _resolve_scripts_dir()

_BOUNDARY_LIB = APP_ROOT / "scripts" / "boundary_lock_lib.py"
if _BOUNDARY_LIB.is_file():
  import importlib.util
  _spec = importlib.util.spec_from_file_location("boundary_lock_lib", _BOUNDARY_LIB)
  _boundary = importlib.util.module_from_spec(_spec)
  assert _spec and _spec.loader
  _spec.loader.exec_module(_boundary)
else:
  _boundary = None


if str(SCRIPTS) not in sys.path:
  sys.path.insert(0, str(SCRIPTS))

from devkit.frontend_contract_lib import (
  API_ID,
  CONFIG_ID,
  HEADER_EXCLUDE_FILENAMES,
  REQUIRED_FILE_HEADER_LABELS,
  STORE_KEY,
  compute_route_path,
  contract_mentions,
  load_layout_prefixes,
  missing_sections,
  parse_file_header,
  parse_registry_index,
  parse_route_entry,
  parse_tracking_table,
  REQUIRED_MODULE_SECTIONS,
  REQUIRED_SECTOR_SECTIONS,
)

WEB_ADMIN = APP_ROOT
SRC = APP_ROOT / "src"

FORBIDDEN_DIR_NAMES = {"shared"}
SCAN_SUFFIXES = {".ts", ".tsx"}
FETCH_PATTERN = re.compile(r"\bfetch\s*\(")
FN_EXPORT_PATTERN = re.compile(
  r"export\s+(?:async\s+)?function\s+(\w+)",
  re.MULTILINE,
)
API_ENTRY_FN_PATTERN = re.compile(r'\bfn:\s*"(\w+)"')
ROUTE_LAYOUT_PATTERN = re.compile(r'layoutId:\s*"([^"]+)"')
LAZY_IMPORT_PATTERN = re.compile(r'import\s*\(\s*"(@/pages/[^"]+)"\s*\)')
QUERY_FN_IMPORT = re.compile(
  r'from\s+["\']@/api/functions|import\s+["\']@/api/functions|from\s+["\']\.\./.*functions'
)
QUERY_RQ_IMPORT = re.compile(r'from\s+["\']@tanstack/react-query|import\s+["\']@tanstack/react-query')

SECTOR_REGISTRY_DIRS: tuple[tuple[str, str, str], ...] = (
  ("router", "modules", "module-id"),
  ("store", "modules", "module-id"),
  ("layout", "modules", "domain-id"),
  ("config", "modules", "config-id"),
  ("api", "functions", "module-id"),
  ("i18n", "modules", "namespace"),
  ("rbac", "modules", "domain"),
)


def _rel(path: Path) -> str:
  try:
    return str(path.relative_to(REPO_ROOT))
  except ValueError:
    try:
      return str(path.relative_to(APP_ROOT))
    except ValueError:
      return str(path)


def _list_subdir_ids(sector: str, subdir: str) -> set[str]:
  base = SRC / sector / subdir
  if not base.is_dir():
    return set()
  return {p.name for p in base.iterdir() if p.is_dir()}


def _validate_file_headers(errors: list[str]) -> None:
  """每个 .ts/.tsx 顶部须含编码绝对门禁标准文件头。"""
  if not SRC.is_dir():
    return
  labels = " · ".join(REQUIRED_FILE_HEADER_LABELS)
  for path in sorted(SRC.rglob("*")):
    if path.suffix not in SCAN_SUFFIXES:
      continue
    if path.name in HEADER_EXCLUDE_FILENAMES:
      continue
    if path.name.endswith(".d.ts"):
      continue
    if "api/generated" in path.as_posix():
      continue
    text = path.read_text(encoding="utf-8")
    header, missing = parse_file_header(text)
    if header is None:
      errors.append(
        f"{_rel(path)} missing file header (/** … */ at top; required: {labels})"
      )
      continue
    if "FORBIDDEN_COMMENT_CLOSE" in missing:
      errors.append(
        f"{_rel(path)} file header line contains */ (breaks TS block comment; "
        f"use {{id}} or 子目录, not glob star-slash)"
      )
      continue
    if missing:
      errors.append(
        f"{_rel(path)} file header missing: {', '.join(missing)} "
        f"(required: {labels})"
      )


def _validate_sector_contracts(errors: list[str]) -> None:
  for sector, subdir, id_label in SECTOR_REGISTRY_DIRS:
    sector_root = SRC / sector
    reg_file = sector_root / "registry.ts"
    contract = sector_root / "contracts" / "README.md"
    if not reg_file.is_file():
      continue
    if not contract.is_file():
      errors.append(f"missing {sector}/contracts/README.md (板块根 registry 须配契约)")
      continue
    text = contract.read_text(encoding="utf-8")
    for section in missing_sections(text, REQUIRED_SECTOR_SECTIONS):
      errors.append(f"{sector}/contracts/README.md missing section {section}")
    disk_ids = _list_subdir_ids(sector, subdir)
    if sector == "store":
      disk_ids.discard("common")  # store/common 非 modules 子表
    doc_ids = parse_registry_index(text)
    for missing in sorted(disk_ids - doc_ids):
      errors.append(
        f"{sector}/contracts/README.md 登记索引缺少 {id_label} `{missing}` "
        f"(已存在 {sector}/{subdir}/{missing}/)"
      )
    for stale in sorted(doc_ids - disk_ids):
      errors.append(
        f"{sector}/contracts/README.md 登记索引多余 {id_label} `{stale}` "
        f"(无 {sector}/{subdir}/{stale}/ 目录)"
      )


def _validate_module_contracts(
  errors: list[str],
  module_ids: set[str],
  pages_dir: Path,
  router_modules: Path,
  layout_prefixes: dict[str, str],
) -> None:
  api_functions = SRC / "api" / "functions"
  store_modules = SRC / "store" / "modules"

  for module_id in sorted(module_ids):
    contract_path = pages_dir / module_id / "contracts" / "README.md"
    if not contract_path.is_file():
      errors.append(f"missing pages/{module_id}/contracts/README.md")
      continue

    contract_text = contract_path.read_text(encoding="utf-8")
    for section in missing_sections(contract_text, REQUIRED_MODULE_SECTIONS):
      errors.append(f"pages/{module_id}/contracts/README.md missing section {section}")

    tracking = parse_tracking_table(contract_text)
    route_reg = router_modules / module_id / "registry.ts"
    if not route_reg.is_file():
      continue
    route = parse_route_entry(route_reg.read_text(encoding="utf-8"))
    expected_path = compute_route_path(route, layout_prefixes)

    checks: tuple[tuple[str, str, str], ...] = (
      ("module-id", str(route.get("moduleId") or module_id), module_id),
      ("route name", str(route.get("name") or ""), ""),
      ("path", expected_path, ""),
      ("layout", str(route.get("layoutId") or ""), ""),
      ("i18n namespace", module_id, module_id),
      ("rbac permission", str(route.get("permission") or ""), ""),
    )
    for key, expected, fallback in checks:
      actual = tracking.get(key, fallback)
      if not actual:
        errors.append(f"pages/{module_id}/contracts/README.md 追踪链缺少 `{key}`")
        continue
      if key == "layout":
        if not actual.startswith(expected):
          errors.append(
            f"pages/{module_id}/contracts/README.md layout mismatch: "
            f"doc={actual!r} registry={expected!r}"
          )
      elif actual != expected:
        errors.append(
          f"pages/{module_id}/contracts/README.md {key} mismatch: "
          f"doc={actual!r} registry={expected!r}"
        )

    perm = str(route.get("permission") or "")
    if not perm:
      errors.append(f"router/modules/{module_id}/registry.ts missing permissions")

    store_reg = store_modules / module_id / "registry.ts"
    if store_reg.is_file():
      store_text = store_reg.read_text(encoding="utf-8")
      for key in STORE_KEY.findall(store_text):
        if not contract_mentions(contract_text, key):
          errors.append(
            f"pages/{module_id}/contracts/README.md 未登记 store key `{key}` "
            f"(见 store/modules/{module_id}/registry.ts)"
          )

    api_reg = api_functions / module_id / "registry.ts"
    if api_reg.is_file():
      api_text = api_reg.read_text(encoding="utf-8")
      for api_id in API_ID.findall(api_text):
        if not contract_mentions(contract_text, api_id):
          errors.append(
            f"pages/{module_id}/contracts/README.md 未登记 api id `{api_id}` "
            f"(见 api/functions/{module_id}/registry.ts)"
          )




def _validate_query_layer_boundary(errors: list[str]) -> None:
  """pages 禁直引 api/functions 与 @tanstack/react-query（W-03）。"""
  pages_dir = SRC / "pages"
  if not pages_dir.is_dir():
    return
  for path in pages_dir.rglob("*"):
    if path.suffix not in SCAN_SUFFIXES:
      continue
    content = path.read_text(encoding="utf-8")
    if QUERY_FN_IMPORT.search(content):
      errors.append(
        f"pages must not import @/api/functions directly: {_rel(path)} — use @/api/query/hooks"
      )
    if QUERY_RQ_IMPORT.search(content):
      errors.append(
        f"pages must not import @tanstack/react-query directly: {_rel(path)} — use @/api/query/hooks"
      )


def _validate_i18n_modules(errors: list[str], module_ids: set[str]) -> None:
  """每个 pages module-id 须有 i18n/modules/{id}/ 双语文案。"""
  i18n_modules = SRC / "i18n" / "modules"
  if not i18n_modules.is_dir():
    errors.append("missing src/i18n/modules/")
    return
  if not (SRC / "i18n" / "modules" / "_platform" / "zh-CN.json").is_file():
    errors.append("missing i18n/modules/_platform/zh-CN.json")
  for module_id in sorted(module_ids):
    zh = i18n_modules / module_id / "zh-CN.json"
    en = i18n_modules / module_id / "en-US.json"
    if not zh.is_file():
      errors.append(f"missing i18n/modules/{module_id}/zh-CN.json")
    if not en.is_file():
      errors.append(f"missing i18n/modules/{module_id}/en-US.json")


def _validate_rbac_studio(errors: list[str], module_ids: set[str]) -> None:
  """rbac MODULE_PERMISSIONS 与 router module-id 一致。"""
  reg = SRC / "rbac" / "modules" / "studio" / "registry.ts"
  if not reg.is_file():
    errors.append("missing rbac/modules/studio/registry.ts")
    return
  text = reg.read_text(encoding="utf-8")
  for module_id in sorted(module_ids):
    if f'"{module_id}"' not in text:
      errors.append(f"rbac/modules/studio/registry.ts missing module-id {module_id!r}")


def _validate_codegen_fresh(errors: list[str]) -> None:
  """OpenAPI → generated 同步（W-01）。"""
  script = APP_ROOT / "scripts" / "check_codegen_fresh.py"
  if not script.is_file():
    errors.append("missing scripts/check_codegen_fresh.py")
    return
  import subprocess

  result = subprocess.run(
    _script_python_argv(script),
    cwd=APP_ROOT,
    capture_output=True,
    text=True,
  )
  if result.returncode != 0:
    msg = (result.stderr or result.stdout or "codegen check failed").strip().splitlines()[0]
    errors.append(msg)



def _validate_architecture_tooling(errors: list[str]) -> None:
  """W-06～W-10 架构基座文件存在性。"""
  if not (APP_ROOT / "playwright.config.ts").is_file():
    errors.append("missing playwright.config.ts (W-06)")
  if not (APP_ROOT / "e2e").is_dir():
    errors.append("missing e2e/ directory (W-06)")
  elif not list((APP_ROOT / "e2e").glob("*.spec.ts")):
    errors.append("e2e/ has no *.spec.ts (W-06)")

  if not (APP_ROOT / "scripts" / "check_bundle_size.py").is_file():
    errors.append("missing scripts/check_bundle_size.py (W-07)")

  storybook_main = APP_ROOT / ".storybook" / "main.ts"
  if not storybook_main.is_file():
    errors.append("missing .storybook/main.ts (W-08)")
  elif not list(SRC.rglob("*.stories.tsx")):
    errors.append("no *.stories.tsx under src/ (W-08)")

  forms_index = SRC / "components" / "forms" / "index.ts"
  if not forms_index.is_file():
    errors.append("missing components/forms/index.ts (W-09)")
  if not (SRC / "components" / "ApiErrorBanner.tsx").is_file():
    errors.append("missing components/ApiErrorBanner.tsx (W-09)")









def _validate_resource_chain(errors: list[str]) -> None:
  """api.id · route.name · module-id · MSW 三角对账（S4）。"""
  import subprocess
  import sys

  script = APP_ROOT / "scripts" / "check_resource_chain.py"
  if not script.is_file():
    errors.append("missing scripts/check_resource_chain.py")
    return
  result = subprocess.run(
    _script_python_argv(script),
    cwd=APP_ROOT,
    capture_output=True,
    text=True,
  )
  if result.returncode != 0:
    msg = (result.stderr or result.stdout or "resource chain failed").strip().splitlines()[-1]
    errors.append(msg)

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

def _validate_error_registry_mirror(errors: list[str]) -> None:
  """vendor error-registry ↔ error-codes.ts（standalone 自给）。"""
  script = APP_ROOT / "scripts" / "check_error_registry_sync.py"
  if not script.is_file():
    errors.append("missing scripts/check_error_registry_sync.py")
    return
  import subprocess

  result = subprocess.run(
    _script_python_argv(script),
    cwd=APP_ROOT,
    capture_output=True,
    text=True,
  )
  if result.returncode != 0:
    msg = (result.stderr or result.stdout or "error registry check failed").strip().splitlines()[-1]
    errors.append(msg)

def _validate_standalone_ready(errors: list[str]) -> None:
  """W-11 standalone 迁出前置（vendor · simulate · 双路径）。"""
  script = APP_ROOT / "scripts" / "check_standalone_ready.py"
  if not script.is_file():
    errors.append("missing scripts/check_standalone_ready.py (W-11)")
    return
  import subprocess

  result = subprocess.run(
    _script_python_argv(script),
    cwd=APP_ROOT,
    capture_output=True,
    text=True,
  )
  if result.returncode != 0:
    msg = (result.stderr or result.stdout or "standalone_ready failed").strip().splitlines()[0]
    errors.append(msg)


def _errors() -> list[str]:
  errors: list[str] = []

  if not (APP_ROOT / "devkit.profile.yaml").is_file():
    errors.append("missing devkit.profile.yaml")

  if not (WEB_ADMIN / "ARCHITECTURE.md").is_file():
    errors.append("missing ARCHITECTURE.md")

  if not (WEB_ADMIN / "ENGINEERING.md").is_file():
    errors.append("missing ENGINEERING.md (工程策略真源)")

  if SRC.is_dir():
    if (SRC / "common").is_dir():
      errors.append("forbidden src/common/ — use @/components/ or sector */common/")
    for path in SRC.rglob("*"):
      if path.is_dir() and path.name in FORBIDDEN_DIR_NAMES:
        errors.append(f"forbidden directory name {path.name!r}: {_rel(path)}")

  pages_dir = SRC / "pages"
  router_modules = SRC / "router" / "modules"
  page_ids: set[str] = set()
  if pages_dir.is_dir():
    for child in pages_dir.iterdir():
      if child.is_dir():
        page_ids.add(child.name)

  router_ids: set[str] = set()
  if router_modules.is_dir():
    for child in router_modules.iterdir():
      if child.is_dir():
        router_ids.add(child.name)

  for pid in sorted(page_ids - router_ids):
    errors.append(f"pages/{pid} has no router/modules/{pid}/registry.ts")
  for rid in sorted(router_ids - page_ids):
    errors.append(f"router/modules/{rid} has no pages/{rid}/")

  layout_prefixes = load_layout_prefixes(SRC / "layout" / "modules")
  module_ids = router_ids & page_ids
  _validate_module_contracts(errors, module_ids, pages_dir, router_modules, layout_prefixes)
  _validate_i18n_modules(errors, module_ids)
  _validate_rbac_studio(errors, module_ids)
  _validate_sector_contracts(errors)
  _validate_file_headers(errors)
  _validate_query_layer_boundary(errors)
  _validate_codegen_fresh(errors)
  _validate_architecture_tooling(errors)
  _validate_standalone_ready(errors)
  _validate_error_registry_mirror(errors)
  _validate_directory_readmes(errors)
  _validate_resource_chain(errors)
  _validate_boundary_lock(errors)

  for module_id in sorted(module_ids):
    lazy_pages = list(pages_dir.glob(f"{module_id}/*.lazy.tsx"))
    if not lazy_pages:
      errors.append(f"pages/{module_id}/ missing *.lazy.tsx entry")

    reg_file = router_modules / module_id / "registry.ts"
    if reg_file.is_file():
      text = reg_file.read_text(encoding="utf-8")
      for lazy_path in LAZY_IMPORT_PATTERN.findall(text):
        rel = lazy_path.removeprefix("@/")
        candidate = SRC / f"{rel}.tsx"
        if not candidate.is_file():
          errors.append(
            f"router lazy import target missing: {lazy_path} → {_rel(candidate)} ({_rel(reg_file)})"
          )

  layout_ids = {p.name for p in (SRC / "layout" / "modules").iterdir() if p.is_dir()} if (
    SRC / "layout" / "modules"
  ).is_dir() else set()

  if router_modules.is_dir():
    for reg in router_modules.glob("*/registry.ts"):
      text = reg.read_text(encoding="utf-8")
      for layout_id in ROUTE_LAYOUT_PATTERN.findall(text):
        if layout_id not in layout_ids:
          errors.append(f"layoutId {layout_id!r} not in layout/modules/ ({_rel(reg)})")

  api_functions = SRC / "api" / "functions"
  if api_functions.is_dir():
    for reg in api_functions.glob("*/registry.ts"):
      text = reg.read_text(encoding="utf-8")
      if "API_MODULE_ENTRIES" not in text:
        errors.append(f"{_rel(reg)} must export API_MODULE_ENTRIES")
      fn_names = API_ENTRY_FN_PATTERN.findall(text)
      fn_dir = reg.parent
      fn_sources = "\n".join(p.read_text(encoding="utf-8") for p in fn_dir.glob("*.fn.ts"))
      exported = set(FN_EXPORT_PATTERN.findall(fn_sources))
      for fn_name in fn_names:
        if fn_name not in exported:
          errors.append(f"api registry fn {fn_name!r} missing in {_rel(fn_dir)}/*.fn.ts")

  if pages_dir.is_dir():
    for path in pages_dir.rglob("*"):
      if path.suffix not in SCAN_SUFFIXES:
        continue
      if FETCH_PATTERN.search(path.read_text(encoding="utf-8")):
        errors.append(f"pages must not call fetch directly: {_rel(path)}")

  for sector, glob_marker in (
    ("router", "import.meta.glob"),
    ("store", "import.meta.glob"),
    ("layout", "import.meta.glob"),
    ("config", "import.meta.glob"),
    ("api", "import.meta.glob"),
  ):
    reg = SRC / sector / "registry.ts"
    if reg.is_file():
      if glob_marker not in reg.read_text(encoding="utf-8"):
        errors.append(f"{_rel(reg)} must use {glob_marker} auto-aggregation")

  pkg = WEB_ADMIN / "package.json"
  if pkg.is_file():
    import json

    scripts = json.loads(pkg.read_text(encoding="utf-8")).get("scripts") or {}
    for script_name in ("lint", "test", "check", "build", "e2e", "storybook:build"):
      if script_name not in scripts:
        errors.append(f"package.json missing script: {script_name}")
    check_cmd = str(scripts.get("check") or "")
    for token in ("build", "size:check", "e2e"):
      if token not in check_cmd:
        errors.append(f"package.json check script must include {token!r} step")

  return errors




def _validate_boundary_lock(errors: list[str]) -> None:
  """独立边界 + 架构 sector 锁（WEB-ARCHITECTURE-LOCK.yaml）。"""
  if _boundary is None:
    errors.append("missing scripts/boundary_lock_lib.py (run install_web_admin_independence_workflow.py)")
    return
  for err in _boundary.run_all_checks(APP_ROOT):
    errors.append(err)

def main() -> int:
  errors = _errors()
  if errors:
    print("web-admin DevKit harness FAIL:", file=sys.stderr)
    for err in errors:
      print(f"  - {err}", file=sys.stderr)
    return 1
  print("OK: web-admin DevKit harness (registry · contracts · file headers · boundaries)")
  return 0


if __name__ == "__main__":
  sys.exit(main())

#!/usr/bin/env python3
"""一键从 templates/frontend-devkit 复刻与 web-admin 等权的前端 App。

用法：
  uv run python scripts/devkit/scaffold_frontend_app.py --id order-console
  ./scripts/scaffold_frontend_app.sh order-console

作用：复制模板 → 替换标识 → 注册 DevKit → 同步 kernel 快照。
业务关联：templates/frontend-devkit · devkit.manifest.yaml · repo-structure.yaml
上游：sync_frontend_template.py（刷新模板）
下游：src/apps/<id>/scripts/activate.sh
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "templates" / "frontend-devkit"
MANIFEST = ROOT / "devkit.manifest.yaml"
REPO_STRUCTURE = ROOT / "contracts" / "repo-structure.yaml"
APPS_README = ROOT / "src" / "apps" / "README.md"

TEXT_SUFFIXES = {
  ".md", ".mdc", ".yaml", ".yml", ".json", ".js", ".mjs", ".ts", ".tsx",
  ".css", ".html", ".sh", ".py", ".txt", ".PIN",
}

SKIP_COPY = {
  "node_modules", "dist", "storybook-static", ".playwright-browsers",
  "test-results", "playwright-report", "__pycache__",
}

PRESERVE_IN_TEMPLATE = {"TEMPLATE.md", "template.manifest.yaml"}


def _validate_app_id(app_id: str) -> None:
  if not re.fullmatch(r"[a-z][a-z0-9]*(-[a-z0-9]+)*", app_id):
    raise SystemExit(
      f"invalid --id {app_id!r}; use kebab-case e.g. order-console"
    )


def _default_ac_scope(app_id: str) -> str:
  prefix = app_id.split("-")[0].upper()
  return f"{prefix}-PROFILE"


def _replacements(
  app_id: str,
  package_name: str,
  ac_scope: str,
  title: str,
) -> list[tuple[str, str]]:
  return [
    ("src/apps/web-admin", f"src/apps/{app_id}"),
    ("@factoryos/web-admin", package_name),
    ("web-admin-dev", f"{app_id}-dev"),
    ("WEB-PROFILE", ac_scope),
    ("web-admin-standalone", f"{app_id}-standalone"),
    ("FactoryOS · Integration Studio", title),
    ("web-admin", app_id),
  ]


def _is_text(path: Path) -> bool:
  if path.suffix.lower() in TEXT_SUFFIXES:
    return True
  return path.name in {"PIN", "BUNDLE_VERSION"}


def _apply_replacements(content: str, pairs: list[tuple[str, str]]) -> str:
  for old, new in pairs:
    content = content.replace(old, new)
  return content


def _copy_template(dest: Path, pairs: list[tuple[str, str]], *, dry_run: bool) -> int:
  count = 0
  for src in sorted(TEMPLATE.rglob("*")):
    if any(p in SKIP_COPY for p in src.parts):
      continue
    rel = src.relative_to(TEMPLATE)
    if rel.name in PRESERVE_IN_TEMPLATE:
      continue
    if src.is_dir():
      if not dry_run:
        (dest / rel).mkdir(parents=True, exist_ok=True)
      continue
    count += 1
    if dry_run:
      continue
    out = dest / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    if _is_text(src):
      text = _apply_replacements(src.read_text(encoding="utf-8"), pairs)
      out.write_text(text, encoding="utf-8")
    else:
      shutil.copy2(src, out)
  return count


def _register_manifest(app_id: str, ac_scope: str, *, dry_run: bool) -> None:
  raw = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
  profiles = list(raw.get("profiles") or [])
  rel_path = f"src/apps/{app_id}"
  if any(p.get("id") == app_id for p in profiles if isinstance(p, dict)):
    raise SystemExit(f"profile {app_id!r} already in devkit.manifest.yaml")
  profiles.append({
    "id": app_id,
    "rel_path": rel_path,
    "harness": "scripts/check_harness.py",
    "activate": "scripts/activate.sh",
    "tier": "step",
    "ac_scope": ac_scope,
  })
  raw["profiles"] = profiles
  if not dry_run:
    MANIFEST.write_text(
      yaml.safe_dump(raw, allow_unicode=True, sort_keys=False),
      encoding="utf-8",
    )


def _register_repo_structure(app_id: str, *, dry_run: bool) -> None:
  raw = yaml.safe_load(REPO_STRUCTURE.read_text(encoding="utf-8")) or {}
  layout = raw.setdefault("layout", {})
  canonical = list(layout.get("canonical_dirs") or [])
  app_path = f"src/apps/{app_id}"
  if app_path not in canonical:
    canonical.append(app_path)
    layout["canonical_dirs"] = canonical

  scan = raw.setdefault("scan", {})
  skip_files = list(scan.get("skip_files") or [])
  skip_entry = f"src/apps/{app_id}/devkit/kernel/factoryos/PATH-SNAPSHOT.md"
  if skip_entry not in skip_files:
    skip_files.append(skip_entry)
    scan["skip_files"] = skip_files

  if not dry_run:
    REPO_STRUCTURE.write_text(
      yaml.safe_dump(raw, allow_unicode=True, sort_keys=False),
      encoding="utf-8",
    )


def _update_apps_readme(app_id: str, title: str, *, dry_run: bool) -> None:
  if not APPS_README.is_file():
    return
  text = APPS_README.read_text(encoding="utf-8")
  row = f"| `{app_id}/` | {title}（frontend-devkit 脚手架） |"
  if f"`{app_id}/`" in text:
    return
  marker = "| `h5-worker/`"
  if marker in text:
    text = text.replace(marker, f"{row}\n{marker}")
  else:
    text = text.rstrip() + f"\n{row}\n"
  if not dry_run:
    APPS_README.write_text(text, encoding="utf-8")


def _copy_template_docs(dest: Path, pairs: list[tuple[str, str]], *, dry_run: bool) -> None:
  for name in ("TEMPLATE.md", "template.manifest.yaml"):
    src = TEMPLATE / name
    if not src.is_file():
      continue
    if dry_run:
      continue
    text = _apply_replacements(src.read_text(encoding="utf-8"), pairs)
    (dest / name).write_text(text, encoding="utf-8")


def _sync_kernel(app_rel: str, *, dry_run: bool) -> None:
  if dry_run:
    return
  subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "devkit" / "sync_kernel_bundle.py"), "--app", app_rel],
    cwd=ROOT,
    check=True,
  )


def _create_check_wrapper(app_id: str, *, dry_run: bool) -> None:
  script_name = app_id.replace("-", "_") + "_check.sh"
  path = ROOT / "scripts" / script_name
  if path.is_file():
    return
  body = f"""#!/usr/bin/env bash
# {app_id} 一键工程自检：DevKit activate 等价（pnpm + profile harness）
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/../src/apps/{app_id}" && pwd)"
exec "$APP_ROOT/scripts/activate.sh"
"""
  if not dry_run:
    path.write_text(body, encoding="utf-8")
    path.chmod(0o755)


def scaffold(
  app_id: str,
  *,
  package_name: str | None = None,
  ac_scope: str | None = None,
  title: str | None = None,
  dry_run: bool = False,
) -> None:
  _validate_app_id(app_id)
  if not TEMPLATE.is_dir():
    raise SystemExit(
      f"template missing: {TEMPLATE}\n"
      "Run: uv run python scripts/devkit/sync_frontend_template.py"
    )

  dest = ROOT / "src" / "apps" / app_id
  if dest.exists():
    raise SystemExit(f"destination already exists: {dest}")

  pkg = package_name or f"@factoryos/{app_id}"
  scope = ac_scope or _default_ac_scope(app_id)
  app_title = title or f"FactoryOS · {app_id.replace('-', ' ').title()}"

  pairs = _replacements(app_id, pkg, scope, app_title)
  app_rel = f"src/apps/{app_id}"

  print(f"▶ scaffold frontend-devkit → {app_rel}")
  print(f"  package={pkg}  ac_scope={scope}  title={app_title}")

  n = _copy_template(dest, pairs, dry_run=dry_run)
  print(f"  copied {n} files")
  _copy_template_docs(dest, pairs, dry_run=dry_run)

  _register_manifest(app_id, scope, dry_run=dry_run)
  _register_repo_structure(app_id, dry_run=dry_run)
  _update_apps_readme(app_id, app_title, dry_run=dry_run)
  _create_check_wrapper(app_id, dry_run=dry_run)
  _sync_kernel(app_rel, dry_run=dry_run)

  if dry_run:
    print("dry-run complete — no files written")
    return

  print(f"""
════════════════════════════════════════════════════════════
  ✅ 前端 App 已创建：{app_rel}
════════════════════════════════════════════════════════════
  开发者手册：contracts/README.md § 前端工程全流程
  1. 阅读：{app_rel}/TEMPLATE.md（结构 · 用法）
  2. 安装：cd {app_rel} && pnpm install
  3. 激活：./scripts/activate.sh   # 全绿后再写业务
  4. 快捷：./scripts/{app_id.replace('-', '_')}_check.sh（仓库根）

  结构变更后请执行：
    uv run python scripts/gen_path_snapshot.py
""")


def main() -> int:
  parser = argparse.ArgumentParser(
    description="Scaffold a web-admin-parity frontend app from templates/frontend-devkit",
  )
  parser.add_argument("--id", required=True, help="App id (kebab-case), e.g. order-console")
  parser.add_argument("--package", help="package.json name, default @factoryos/<id>")
  parser.add_argument("--ac-scope", help="AC scope in devkit.profile, default <ID>-PROFILE")
  parser.add_argument("--title", help="index.html title")
  parser.add_argument("--dry-run", action="store_true")
  args = parser.parse_args()
  scaffold(
    args.id,
    package_name=args.package,
    ac_scope=args.ac_scope,
    title=args.title,
    dry_run=args.dry_run,
  )
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

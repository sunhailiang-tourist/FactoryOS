#!/usr/bin/env python3
"""金样 web-admin ↔ templates/frontend-devkit 架构 parity 门禁。

作用：验证模板与金样在锁死路径上一致，防止 scaffold 漂移。
业务关联：contracts/frontend-devkit-lock.yaml · sync_frontend_template.py
上游：src/apps/web-admin
下游：gate pr · scaffold_frontend_app.py
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / "contracts" / "frontend-devkit-lock.yaml"

# 模板内手写文件 — 不参与字节 parity，但须存在
TEMPLATE_ONLY = {"TEMPLATE.md", "template.manifest.yaml"}


def _load_lock() -> dict:
  if not LOCK.is_file():
    raise SystemExit(f"missing lock file: {LOCK}")
  return yaml.safe_load(LOCK.read_text(encoding="utf-8")) or {}


def _sha256(path: Path) -> str:
  return hashlib.sha256(path.read_bytes()).hexdigest()


def check_parity(*, verbose: bool = False) -> list[str]:
  lock = _load_lock()
  golden_rel = str(lock.get("golden_source") or "src/apps/web-admin")
  template_rel = str(lock.get("template_path") or "templates/frontend-devkit")
  golden = ROOT / golden_rel
  template = ROOT / template_rel
  errors: list[str] = []

  if not golden.is_dir():
    errors.append(f"golden missing: {golden_rel}")
    return errors
  if not template.is_dir():
    errors.append(f"template missing: {template_rel}")
    return errors

  for sector in lock.get("sectors") or []:
    sector_dir = golden / "src" / str(sector)
    tpl_sector = template / "src" / str(sector)
    if not sector_dir.is_dir():
      errors.append(f"golden missing sector src/{sector}/")
    elif not tpl_sector.is_dir():
      errors.append(f"template missing sector src/{sector}/ (run sync_frontend_template.py)")

  for rel in lock.get("parity_required_paths") or []:
    g = golden / rel
    t = template / rel
    if not g.is_file():
      errors.append(f"golden missing required file: {golden_rel}/{rel}")
      continue
    if not t.is_file():
      errors.append(f"template missing required file: {template_rel}/{rel}")
      continue
    if _sha256(g) != _sha256(t):
      errors.append(f"parity drift: {rel} (golden ≠ template)")

  manifest = template / "template.manifest.yaml"
  if manifest.is_file():
    meta = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    if str(meta.get("template_version") or "") != str(lock.get("version") or ""):
      errors.append(
        f"template.manifest.yaml version {meta.get('template_version')!r} "
        f"≠ lock version {lock.get('version')!r}"
      )

  if verbose and not errors:
    print(f"OK: parity {golden_rel} ↔ {template_rel} · lock {lock.get('version')}")
  return errors


def main() -> int:
  parser = argparse.ArgumentParser(description="Check web-admin golden ↔ frontend-devkit template parity")
  parser.add_argument("-v", "--verbose", action="store_true")
  args = parser.parse_args()
  errors = check_parity(verbose=args.verbose)
  if errors:
    print("frontend-devkit parity FAIL:", file=sys.stderr)
    for err in errors:
      print(f"  - {err}", file=sys.stderr)
    return 1
  if not args.verbose:
    print("OK: frontend-devkit template parity")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

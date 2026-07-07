#!/usr/bin/env python3
# web-admin 资源链路三角对账 — module-id · route.name · api.id · MSW path
from __future__ import annotations

import re
import sys
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
SRC = APP / "src"

API_ENTRY = re.compile(
  r'id:\s*"([^"]+)".*?module:\s*"([^"]+)".*?routeName:\s*"([^"]+)".*?path:\s*"([^"]+)"',
  re.DOTALL,
)
ROUTE_ENTRY = re.compile(
  r'name:\s*"([^"]+)".*?moduleId:\s*"([^"]+)"',
  re.DOTALL,
)
CONTRACT_API = re.compile(r"api id\s*\|\s*`([^`]+)`")
CONTRACT_ROUTE = re.compile(r"route name\s*\|\s*`([^`]+)`")
MSW_PATH = re.compile(r'http\.(?:get|post|put|patch|delete|all)\(\s*"([^"]+)"')


def _read_api_entries() -> list[tuple[str, str, str, str]]:
  entries: list[tuple[str, str, str, str]] = []
  for reg in (SRC / "api/functions").glob("*/registry.ts"):
    text = reg.read_text(encoding="utf-8")
    for m in API_ENTRY.finditer(text):
      entries.append((m.group(1), m.group(2), m.group(3), m.group(4)))
  return entries

def _read_route_entries() -> dict[str, str]:
  mapping: dict[str, str] = {}
  for reg in (SRC / "router/modules").glob("*/registry.ts"):
    text = reg.read_text(encoding="utf-8")
    for m in ROUTE_ENTRY.finditer(text):
      mapping[m.group(2)] = m.group(1)
  return mapping

def _read_msw_paths() -> set[str]:
  paths: set[str] = set()
  for f in (SRC / "mocks/handlers").glob("*.ts"):
    if f.name == "index.ts":
      continue
    text = f.read_text(encoding="utf-8")
    paths.update(MSW_PATH.findall(text))
  return paths

def main() -> int:
  errors: list[str] = []
  routes = _read_route_entries()
  msw = _read_msw_paths()

  for api_id, module_id, route_name, path in _read_api_entries():
    if routes.get(module_id) != route_name:
      errors.append(
        f"api registry {api_id}: routeName {route_name!r} != router {routes.get(module_id)!r} for {module_id}"
      )
    contract = SRC / "pages" / module_id / "contracts/README.md"
    if contract.is_file():
      text = contract.read_text(encoding="utf-8")
      cm = CONTRACT_API.search(text)
      cr = CONTRACT_ROUTE.search(text)
      if cm and cm.group(1) != api_id:
        errors.append(f"{module_id} contracts api id {cm.group(1)!r} != registry {api_id!r}")
      if cr and cr.group(1) != route_name:
        errors.append(f"{module_id} contracts route {cr.group(1)!r} != registry {route_name!r}")
    if path not in msw and not any(p.startswith(path.rsplit("/", 1)[0]) for p in msw):
      errors.append(f"MSW missing handler path for api {api_id}: {path}")

  if errors:
    print("resource_chain FAIL:", file=sys.stderr)
    for e in errors:
      print(f"  - {e}", file=sys.stderr)
    return 1
  print("OK: resource chain aligned (api registry · router · contracts · MSW)")
  return 0


if __name__ == "__main__":
  sys.exit(main())

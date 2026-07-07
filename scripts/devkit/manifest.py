"""devkit.manifest.yaml 加载与路径解析。"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

MANIFEST_NAME = "devkit.manifest.yaml"
PROFILE_NAME = "devkit.profile.yaml"


@dataclass(frozen=True)
class ProfileEntry:
  id: str
  root: Path
  harness: Path
  activate: Path | None
  tier: str
  ac_scope: str


@dataclass(frozen=True)
class DevkitManifest:
  version: str
  mode: str
  root: Path
  profiles: tuple[ProfileEntry, ...]
  kernel: dict[str, str]


def find_manifest_root(start: Path) -> Path | None:
  """向上查找含 devkit.manifest.yaml 的目录。"""
  current = start.resolve()
  while True:
    if (current / MANIFEST_NAME).is_file():
      return current
    if current.parent == current:
      return None
    current = current.parent


def load_manifest(root: Path) -> DevkitManifest:
  """加载 manifest；profiles 路径相对各 profile rel_path 或 standalone 根。"""
  path = root / MANIFEST_NAME
  raw: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
  mode = str(raw.get("mode") or "umbrella")
  version = str(raw.get("devkit_version") or "0.0.0")
  kernel = dict(raw.get("kernel") or {})
  profiles: list[ProfileEntry] = []

  if mode == "standalone":
    profile_id = str(raw.get("project_id") or raw.get("profile") or "app")
    app_root = root
    harness_rel = str(raw.get("harness") or "scripts/check_harness.py")
    activate_rel = raw.get("activate")
    profiles.append(
      ProfileEntry(
        id=profile_id,
        root=app_root,
        harness=app_root / harness_rel,
        activate=app_root / str(activate_rel) if activate_rel else None,
        tier=str(raw.get("tier") or "step"),
        ac_scope=str(raw.get("ac_scope") or ""),
      )
    )
  else:
    for item in raw.get("profiles") or []:
      if not isinstance(item, dict):
        continue
      rel = str(item.get("rel_path") or "")
      app_root = (root / rel).resolve()
      harness_rel = str(item.get("harness") or "scripts/check_harness.py")
      activate_rel = item.get("activate")
      profiles.append(
        ProfileEntry(
          id=str(item.get("id") or rel),
          root=app_root,
          harness=app_root / harness_rel,
          activate=app_root / str(activate_rel) if activate_rel else None,
          tier=str(item.get("tier") or "step"),
          ac_scope=str(item.get("ac_scope") or ""),
        )
      )

  return DevkitManifest(
    version=version,
    mode=mode,
    root=root.resolve(),
    profiles=tuple(profiles),
    kernel=kernel,
  )


def load_profile_meta(app_root: Path) -> dict[str, Any]:
  """读取 app 内 devkit.profile.yaml（可选）。"""
  path = app_root / PROFILE_NAME
  if not path.is_file():
    return {}
  return yaml.safe_load(path.read_text(encoding="utf-8")) or {}

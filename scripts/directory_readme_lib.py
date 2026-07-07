"""contracts/directory-readmes.yaml — 目录 README 对账库（umbrella + DevKit 共用）。"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "contracts" / "directory-readmes.yaml"


@dataclass(frozen=True)
class DirectoryReadmeManifest:
  version: int
  required_sections: tuple[str, ...]
  strict_paths: frozenset[str]
  exempt_dir_names: frozenset[str]
  required_paths: tuple[str, ...]
  scan_roots: tuple[tuple[str, int], ...]


def load_manifest(path: Path | None = None) -> DirectoryReadmeManifest:
  raw = yaml.safe_load((path or MANIFEST).read_text(encoding="utf-8"))
  scan: list[tuple[str, int]] = []
  for item in raw.get("scan_roots") or []:
    scan.append((str(item["root"]), int(item.get("depth", 1))))
  return DirectoryReadmeManifest(
    version=int(raw.get("version", 1)),
    required_sections=tuple(raw.get("required_sections") or ()),
    strict_paths=frozenset(raw.get("strict_paths") or ()),
    exempt_dir_names=frozenset(raw.get("exempt_dir_names") or ()),
    required_paths=tuple(raw.get("required_paths") or ()),
    scan_roots=tuple(scan),
  )


def expand_kernel_module_paths(manifest: DirectoryReadmeManifest) -> set[str]:
  """kernel.modules → src/server/os_core/<module>/ README 要求。"""
  from repo_structure import load_snapshot

  snap = load_snapshot()
  paths = set(manifest.required_paths)
  for mod in snap.kernel_modules:
    paths.add(f"src/server/os_core/{mod}")
  return paths


def _readme_issues(readme: Path, sections: tuple[str, ...]) -> list[str]:
  if not readme.is_file():
    return ["missing README.md"]
  text = readme.read_text(encoding="utf-8")
  issues: list[str] = []
  if not text.lstrip().startswith("#"):
    issues.append("README.md must start with # heading")
  aliases: dict[str, tuple[str, ...]] = {
    "## 是什么": ("## 是什么",),
    "## 子路径": ("## 子路径", "| 路径 |", "| 层 |", "| 板块 |", "| # |"),
    "## 门禁": ("## 门禁", "## 门禁/命令"),
    "## 变更纪律": ("## 变更纪律", "## 变更规则"),
    "## 相关文档": ("## 相关文档", "## 文档链接"),
  }
  for section in sections:
    opts = aliases.get(section, (section,))
    if section == "## 是什么" and text.lstrip().startswith("#"):
      continue
    if not any(opt in text for opt in opts):
      issues.append(f"missing section {section}")
  return issues


def validate_required_readmes(
  manifest: DirectoryReadmeManifest | None = None,
  *,
  root: Path | None = None,
  path_prefix: str | None = None,
) -> list[str]:
  """登记路径须有 README + 必填节。path_prefix 限定子树（如 src/apps/web-admin）。"""
  manifest = manifest or load_manifest()
  base = root or ROOT
  required = expand_kernel_module_paths(manifest)
  if path_prefix:
    required = {p for p in required if p == path_prefix or p.startswith(path_prefix.rstrip("/") + "/")}
  errors: list[str] = []
  for rel in sorted(required):
    dir_path = base / rel
    if not dir_path.is_dir():
      continue
    readme = dir_path / "README.md"
    if not readme.is_file():
      errors.append(f"{rel}: missing README.md")
      continue
    text = readme.read_text(encoding="utf-8")
    if not text.lstrip().startswith("#"):
      errors.append(f"{rel}: README.md must start with # heading")
      continue
    if rel not in manifest.strict_paths:
      continue
    for issue in _readme_issues(readme, manifest.required_sections):
      if issue in ("missing README.md", "README.md must start with # heading"):
        continue
      errors.append(f"{rel}: {issue}")
  return errors


def validate_unregistered_dirs(
  manifest: DirectoryReadmeManifest | None = None,
  *,
  root: Path | None = None,
  path_prefix: str | None = None,
) -> list[str]:
  """扫描根下未登记 depth-1 目录 → 须用户确认后写入 manifest。"""
  manifest = manifest or load_manifest()
  base = root or ROOT
  required = expand_kernel_module_paths(manifest)
  errors: list[str] = []

  for scan_root, depth in manifest.scan_roots:
    if path_prefix and not (scan_root == path_prefix or scan_root.startswith(path_prefix.rstrip("/") + "/")):
      continue
    anchor = base / scan_root
    if not anchor.is_dir() or depth != 1:
      continue
    for child in sorted(anchor.iterdir()):
      if not child.is_dir():
        continue
      name = child.name
      if name in manifest.exempt_dir_names:
        continue
      rel = f"{scan_root}/{name}".replace("/./", "/")
      if rel not in required:
        errors.append(
          f"unregistered directory `{rel}/` — 须用户确认后写入 contracts/directory-readmes.yaml"
        )
  return errors


def format_report(errors: list[str]) -> str:
  if not errors:
    return "OK: directory README manifest aligned"
  lines = ["directory-readmes FAIL:"]
  lines.extend(f"  - {e}" for e in errors)
  lines.append(
    "\n变更 SOP：用户确认 → 更新 contracts/directory-readmes.yaml "
    "+ repo-structure.yaml + gen_path_snapshot + gate pr"
  )
  return "\n".join(lines)

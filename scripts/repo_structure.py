#!/usr/bin/env python3
"""Load contracts/repo-structure.yaml — 结构快照共享库。

Usage (library):
  from repo_structure import load_snapshot, repo_root, SNAPSHOT_PATH

关联：check_legacy_paths · audit_path_consistency · check_repo_structure · gen_path_snapshot
"""
from __future__ import annotations

import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
  import yaml
except ImportError:
  yaml = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_PATH = ROOT / "contracts" / "repo-structure.yaml"
PATH_SNAPSHOT_MD = ROOT / ".cursor" / "factoryos" / "PATH-SNAPSHOT.md"
KERNEL_REGISTRY = ROOT / "src" / "server" / "os_core" / "registry.py"


@dataclass(frozen=True, slots=True)
class RepoSnapshot:
  """仓库结构快照（contracts/repo-structure.yaml 解析结果）。"""

  version: int
  updated: str
  decision_ref: str
  imports_api: str
  imports_kernel: str
  canonical_dirs: tuple[str, ...]
  canonical_files: tuple[str, ...]
  forbidden_dirs: tuple[str, ...]
  forbidden_files: tuple[str, ...]
  forbidden_text_refs: tuple[str, ...]
  forbidden_text_regex: tuple[str, ...]
  allow_line_regex: tuple[str, ...]
  kernel_module_count: int
  kernel_modules: tuple[str, ...]
  scan_roots: tuple[str, ...]
  scan_skip_path_parts: tuple[str, ...]
  scan_skip_files: tuple[str, ...]
  scan_extra_root_files: tuple[str, ...]
  scan_binary_extensions: tuple[str, ...]
  historical_files: tuple[str, ...]
  semantic_scan_prefixes: tuple[str, ...]
  semantic_forbidden: tuple[str, ...]
  commit_watch_prefixes: tuple[str, ...]
  commit_require_staged: tuple[str, ...]


def repo_root() -> Path:
  return ROOT


def load_snapshot(path: Path | None = None) -> RepoSnapshot:
  """读取结构快照 YAML。"""
  if yaml is None:
    print("FAIL: PyYAML required — run: uv run python scripts/...", file=sys.stderr)
    raise SystemExit(2)
  p = path or SNAPSHOT_PATH
  if not p.is_file():
    print(f"FAIL: missing snapshot {p.relative_to(ROOT)}", file=sys.stderr)
    raise SystemExit(1)
  raw = yaml.safe_load(p.read_text(encoding="utf-8"))
  if not isinstance(raw, dict):
    raise ValueError("repo-structure.yaml root must be a mapping")

  layout = raw.get("layout") or {}
  imports = raw.get("imports") or {}
  kernel = raw.get("kernel") or {}
  scan = raw.get("scan") or {}

  def _str_list(key: str, section: dict) -> tuple[str, ...]:
    val = section.get(key) or []
    if not isinstance(val, list):
      raise ValueError(f"{key} must be a list")
    return tuple(str(x) for x in val)

  sem = raw.get("semantic_forbidden") or []
  sem_patterns: list[str] = []
  for item in sem:
    if isinstance(item, dict) and "pattern" in item:
      sem_patterns.append(str(item["pattern"]))

  commit = raw.get("commit_watch") or {}
  commit_prefixes = commit.get("path_prefixes") or [
    "src/server/os_core/",
    "src/server/api/modules/",
    "src/server/",
    "src/apps/",
    "src/integration/",
  ]
  commit_required = commit.get("require_staged_when_touched") or [
    "contracts/repo-structure.yaml",
    ".cursor/factoryos/PATH-SNAPSHOT.md",
  ]

  return RepoSnapshot(
    version=int(raw.get("version", 0)),
    updated=str(raw.get("updated", "")),
    decision_ref=str(raw.get("decision_ref", "")),
    imports_api=str(imports.get("api", "")),
    imports_kernel=str(imports.get("kernel", "")),
    canonical_dirs=_str_list("canonical_dirs", layout),
    canonical_files=_str_list("canonical_files", layout),
    forbidden_dirs=_str_list("forbidden_dirs", layout),
    forbidden_files=_str_list("forbidden_files", layout),
    forbidden_text_refs=tuple(str(x) for x in (raw.get("forbidden_text_refs") or [])),
    forbidden_text_regex=tuple(str(x) for x in (raw.get("forbidden_text_regex") or [])),
    allow_line_regex=tuple(str(x) for x in (raw.get("allow_line_regex") or [])),
    kernel_module_count=int(kernel.get("module_count", 0)),
    kernel_modules=_str_list("modules", kernel),
    scan_roots=_str_list("roots", scan),
    scan_skip_path_parts=_str_list("skip_path_parts", scan),
    scan_skip_files=_str_list("skip_files", scan),
    scan_extra_root_files=_str_list("extra_root_files", scan),
    scan_binary_extensions=_str_list("binary_extensions", scan),
    historical_files=tuple(str(x) for x in (raw.get("historical_files") or [])),
    semantic_scan_prefixes=tuple(str(x) for x in (raw.get("semantic_scan_prefixes") or [])),
    semantic_forbidden=tuple(sem_patterns),
    commit_watch_prefixes=tuple(str(x) for x in commit_prefixes),
    commit_require_staged=tuple(str(x) for x in commit_required),
  )


@dataclass(frozen=True, slots=True)
class StructureDrift:
  """结构漂移项（供提交拦截与人工修复）。"""

  kind: str
  detail: str


@dataclass
class StructureReport:
  """快照对账结果。"""

  drifts: list[StructureDrift] = field(default_factory=list)

  @property
  def ok(self) -> bool:
    return not self.drifts


def disk_kernel_module_dirs(root: Path | None = None) -> set[str]:
  """磁盘上 os_core 模块目录（含 registry.py 自身目录的兄弟）。"""
  base = (root or ROOT) / "src" / "server" / "os_core"
  if not base.is_dir():
    return set()
  out: set[str] = set()
  for child in base.iterdir():
    if not child.is_dir() or child.name.startswith("__"):
      continue
    if child.name == "__pycache__":
      continue
    if (child / "README.md").is_file() or any(child.glob("*.py")):
      out.add(child.name)
  return out


def analyze_structure_drift(snapshot: RepoSnapshot | None = None) -> StructureReport:
  """快照 ↔ 磁盘 ↔ registry ↔ PATH-SNAPSHOT 全量对账。"""
  snap = snapshot or load_snapshot()
  report = StructureReport()

  for rel in snap.canonical_dirs:
    if not (ROOT / rel).is_dir():
      report.drifts.append(StructureDrift("missing_canonical_dir", rel))
  for rel in snap.canonical_files:
    if not (ROOT / rel).is_file():
      report.drifts.append(StructureDrift("missing_canonical_file", rel))

  for rel in snap.forbidden_dirs:
    if (ROOT / rel).exists():
      report.drifts.append(StructureDrift("forbidden_dir_exists", rel))
  for rel in snap.forbidden_files:
    if (ROOT / rel).exists():
      report.drifts.append(StructureDrift("forbidden_file_exists", rel))

  if len(snap.kernel_modules) != snap.kernel_module_count:
    report.drifts.append(
      StructureDrift(
        "kernel_count_mismatch",
        f"module_count={snap.kernel_module_count} list={len(snap.kernel_modules)}",
      )
    )

  on_disk = disk_kernel_module_dirs()
  snap_set = set(snap.kernel_modules)
  for mod in sorted(on_disk - snap_set):
    report.drifts.append(StructureDrift("kernel_on_disk_not_in_snapshot", mod))
  for mod in sorted(snap_set - on_disk):
    report.drifts.append(StructureDrift("kernel_in_snapshot_missing_on_disk", mod))

  try:
    registered = load_kernel_registry_names()
    if registered != snap_set:
      only_reg = sorted(registered - snap_set)
      only_snap = sorted(snap_set - registered)
      if only_reg:
        report.drifts.append(StructureDrift("registry_not_in_snapshot", ", ".join(only_reg)))
      if only_snap:
        report.drifts.append(StructureDrift("snapshot_not_in_registry", ", ".join(only_snap)))
  except (OSError, ValueError, SyntaxError) as exc:
    report.drifts.append(StructureDrift("registry_parse_error", str(exc)))

  expected_md = render_path_snapshot_md(snap)
  if not expected_md.endswith("\n"):
    expected_md += "\n"
  if not PATH_SNAPSHOT_MD.is_file():
    report.drifts.append(StructureDrift("path_snapshot_missing", str(PATH_SNAPSHOT_MD.relative_to(ROOT))))
  elif PATH_SNAPSHOT_MD.read_text(encoding="utf-8") != expected_md:
    report.drifts.append(StructureDrift("path_snapshot_stale", str(PATH_SNAPSHOT_MD.relative_to(ROOT))))

  return report


def _plain_reason(d: StructureDrift) -> str:
  """把漂移项翻成一句人话。"""
  if d.kind == "commit_touched_structure":
    return d.detail.replace("暂存区含新内核路径", "本次 commit 新增了内核目录").replace(
      "（未在 snapshot.kernel.modules）", "，但结构配置文件里还没登记"
    )
  if d.kind == "commit_missing_snapshot":
    return "你改了目录/模块结构，但本次 commit 没有带上 contracts/repo-structure.yaml"
  if d.kind == "commit_missing_path_snapshot":
    return "你改了 contracts/repo-structure.yaml，但没有重新生成 PATH-SNAPSHOT.md 或未加入本次 commit"
  if d.kind == "path_snapshot_stale":
    return "PATH-SNAPSHOT.md 与 repo-structure.yaml 内容不一致（需要重新生成）"
  if d.kind == "path_snapshot_missing":
    return "缺少 .cursor/factoryos/PATH-SNAPSHOT.md（需要运行生成脚本）"
  if d.kind == "kernel_on_disk_not_in_snapshot":
    return f"磁盘上有内核模块 `{d.detail}`，但 repo-structure.yaml 的 kernel.modules 里没有"
  if d.kind == "forbidden_dir_exists":
    return f"废止目录仍存在：`{d.detail}`（应删除或移走）"
  if d.kind == "forbidden_file_exists":
    return f"废止文件仍存在：`{d.detail}`（应删除或移走）"
  fallback = {
    "missing_canonical_dir": "缺少应存在的目录",
    "missing_canonical_file": "缺少应存在的文件",
    "kernel_count_mismatch": "kernel.module_count 与 modules 列表数量不一致",
    "kernel_in_snapshot_missing_on_disk": "配置文件写了内核模块但磁盘上没有对应目录",
    "registry_not_in_snapshot": "registry.py 登记的模块未写入 repo-structure.yaml",
    "snapshot_not_in_registry": "repo-structure.yaml 的模块未写入 registry.py",
    "registry_parse_error": "registry.py 解析失败",
  }
  label = fallback.get(d.kind, d.kind)
  return f"{label}：{d.detail}"


def format_remediation(report: StructureReport, *, staged: list[str] | None = None) -> str:
  """按实际漂移类型输出「原因 + 可复制命令」，避免千篇一律的 5 步手册。"""
  kinds = {d.kind for d in report.drifts}
  new_modules: list[str] = []
  for d in report.drifts:
    if d.kind in ("commit_touched_structure", "kernel_on_disk_not_in_snapshot"):
      # detail 形如 src/server/os_core/foo/ 或 foo
      mod = d.detail.split("src/server/os_core/")[-1].split("/")[0].split("（")[0].strip()
      if mod and mod not in new_modules:
        new_modules.append(mod)

  lines = [
    "",
    "════════════════════════════════════════════════════════════════",
    "  Git 提交已拦截 · 项目目录结构与配置文件不同步",
    "  （保护机制：防止「目录改了一半就 commit」，不是代码编译错误）",
    "════════════════════════════════════════════════════════════════",
    "",
    "【原因】",
  ]
  for d in report.drifts:
    lines.append(f"  • {_plain_reason(d)}")

  lines.extend(["", "【怎么修 — 在仓库根目录复制执行】", ""])

  need_yaml_edit = bool(
    kinds
    & {
      "commit_touched_structure",
      "kernel_on_disk_not_in_snapshot",
      "kernel_in_snapshot_missing_on_disk",
      "kernel_count_mismatch",
      "missing_canonical_dir",
      "forbidden_dir_exists",
      "forbidden_file_exists",
    }
  )
  need_regen = bool(
    kinds
    & {
      "commit_missing_path_snapshot",
      "path_snapshot_stale",
      "path_snapshot_missing",
      "commit_missing_snapshot",
    }
  ) or "commit_missing_snapshot" in kinds or need_yaml_edit

  step = 1
  if need_yaml_edit:
    mod_hint = "、".join(f"`{m}`" for m in new_modules) if new_modules else "（你的新目录名）"
    lines.extend([
      f"  {step}. 编辑结构配置文件（手工，约 1 分钟）",
      "     打开：contracts/repo-structure.yaml",
      "     · 若新增了顶层目录 → 写入 layout.canonical_dirs",
      "     · 若废止了旧目录 → 写入 layout.forbidden_dirs",
      f"     · 若新增了内核模块 {mod_hint} → 写入 kernel.modules，并把 module_count +1",
      "     · 把 updated 改成今天日期；有正式决策则改 decision_ref",
      "",
    ])
    step += 1

  if need_regen:
    lines.extend([
      f"  {step}. 重新生成路径快照（自动生成，勿手改 PATH-SNAPSHOT.md）",
      "     uv run python scripts/gen_path_snapshot.py",
      "",
    ])
    step += 1

  lines.extend([
    f"  {step}. 把配置文件和快照一起加入本次 commit",
    "     git add contracts/repo-structure.yaml .cursor/factoryos/PATH-SNAPSHOT.md",
    "     # 若还改了 18-一致性矩阵 / MODULE-MAP，也一并 git add",
    "",
  ])
  step += 1

  lines.extend([
    f"  {step}. 确认门禁通过后再 commit",
    "     uv run python scripts/check_structure_change.py",
    "     git commit",
    "",
    "【常见情况 · 不用改 yaml】",
    "  只在已有目录里增删 .py 文件（例如改 graph_service/store.py）→ 不应触发本拦截。",
    "  若仍被拦，请把上面【原因】整段发给维护者（可能是误报）。",
    "",
    "详细规则：.cursor/rules/项目结构变更门禁.mdc",
  ])
  return "\n".join(lines)


def format_drift_report(report: StructureReport) -> str:
  """人类可读的漂移清单。"""
  labels = {
    "missing_canonical_dir": "缺少现行目录",
    "missing_canonical_file": "缺少现行文件",
    "forbidden_dir_exists": "废止目录仍存在",
    "forbidden_file_exists": "废止文件仍存在",
    "kernel_count_mismatch": "kernel.module_count 不一致",
    "kernel_on_disk_not_in_snapshot": "磁盘新内核模块（未入快照）",
    "kernel_in_snapshot_missing_on_disk": "快照内核模块（磁盘缺失）",
    "registry_not_in_snapshot": "registry.py 有模块未入快照",
    "snapshot_not_in_registry": "快照模块未登记 registry.py",
    "registry_parse_error": "registry.py 解析失败",
    "path_snapshot_missing": "PATH-SNAPSHOT.md 缺失",
    "path_snapshot_stale": "PATH-SNAPSHOT.md 过期",
    "commit_missing_snapshot": "结构变更 commit 未含 repo-structure.yaml",
    "commit_missing_path_snapshot": "已改快照但未 staged PATH-SNAPSHOT.md",
    "commit_touched_structure": "触及结构路径但未同步快照",
  }
  lines = ["检测到："]
  for d in report.drifts:
    label = labels.get(d.kind, d.kind)
    lines.append(f"  · [{label}] {d.detail}")
  return "\n".join(lines)


def compile_forbidden_patterns(snapshot: RepoSnapshot) -> list[re.Pattern[str]]:
  """将 forbidden_text_refs 编译为正则（整词/路径边界）。"""
  patterns: list[re.Pattern[str]] = []
  for ref in snapshot.forbidden_text_refs:
    escaped = re.escape(ref)
    patterns.append(re.compile(rf"\b{escaped}\b" if "/" not in ref else rf"\b{escaped}\b"))
  for pat in snapshot.forbidden_text_regex:
    patterns.append(re.compile(pat))
  return patterns


def compile_allow_line(snapshot: RepoSnapshot) -> re.Pattern[str] | None:
  if not snapshot.allow_line_regex:
    return None
  return re.compile("|".join(f"(?:{p})" for p in snapshot.allow_line_regex), re.I)


def load_kernel_registry_names() -> set[str]:
  """从 os_core/registry.py AST 解析 KERNEL_MODULES 名称。"""
  if not KERNEL_REGISTRY.is_file():
    raise FileNotFoundError(f"missing {KERNEL_REGISTRY.relative_to(ROOT)}")
  tree = ast.parse(KERNEL_REGISTRY.read_text(encoding="utf-8"), filename=str(KERNEL_REGISTRY))
  tuple_node: ast.Tuple | None = None
  for node in tree.body:
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Name) and target.id == "KERNEL_MODULES":
          if isinstance(node.value, ast.Tuple):
            tuple_node = node.value
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
      if node.target.id == "KERNEL_MODULES" and isinstance(node.value, ast.Tuple):
        tuple_node = node.value
  if tuple_node is None:
    raise ValueError("KERNEL_MODULES not found in os_core/registry.py")
  names: set[str] = set()
  for elt in tuple_node.elts:
    if not isinstance(elt, ast.Call):
      continue
    if elt.args and isinstance(elt.args[0], ast.Constant) and isinstance(elt.args[0].value, str):
      names.add(elt.args[0].value)
      continue
    for kw in elt.keywords:
      if kw.arg == "name" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
        names.add(kw.value.value)
        break
  return names


def render_path_snapshot_md(snapshot: RepoSnapshot) -> str:
  """生成 Agent 可读的 PATH-SNAPSHOT.md 正文。"""
  lines = [
    "# PATH-SNAPSHOT · 项目结构快照",
    "",
    "> **AUTO-GENERATED — 勿手改**",
    f"> 真源：`contracts/repo-structure.yaml` · 生成：`uv run python scripts/gen_path_snapshot.py`",
    f"> version: {snapshot.version} · updated: {snapshot.updated} · decision_ref: {snapshot.decision_ref}",
    "",
    "## import 前缀",
    "",
    f"| 层 | import | 物理根 |",
    f"|----|--------|--------|",
    f"| HTTP API | `{snapshot.imports_api}` | `src/server/api/` |",
    f"| 内核 | `{snapshot.imports_kernel}.*` | `src/server/os_core/` |",
    "",
    "## 现行路径（canonical）",
    "",
  ]
  for d in snapshot.canonical_dirs:
    lines.append(f"- `{d}/`")
  for f in snapshot.canonical_files:
    lines.append(f"- `{f}`")
  lines.extend([
    "",
    "## 废止路径（禁止作为操作路径）",
    "",
    "### 目录不得存在",
    "",
  ])
  for d in snapshot.forbidden_dirs:
    lines.append(f"- `{d}/`")
  lines.extend(["", "### 文件不得存在", ""])
  for f in snapshot.forbidden_files:
    lines.append(f"- `{f}`")
  lines.extend(["", "### 文本不得误导引用", ""])
  for ref in snapshot.forbidden_text_refs:
    lines.append(f"- `{ref}`")
  for pat in snapshot.forbidden_text_regex:
    lines.append(f"- regex: `{pat}`")
  lines.extend([
    "",
    f"## 内核模块（{snapshot.kernel_module_count}）",
    "",
  ])
  for i, name in enumerate(snapshot.kernel_modules, 1):
    lines.append(f"{i}. `{name}` → `src/server/os_core/{name}/`")
  lines.extend([
    "",
    "## 结构变更纪律",
    "",
    "1. 先改 `contracts/repo-structure.yaml`",
    "2. 跑 `uv run python scripts/gen_path_snapshot.py`",
    "3. 更新 `18-一致性矩阵` D 行 · `命名约定.md`",
    "4. `./scripts/gate pr` 全绿",
    "5. **git commit** 时 pre-commit 自动跑 `check_structure_change.py`（漂移则拦截并打印步骤）",
    "",
  ])
  return "\n".join(lines)

#!/usr/bin/env python3
"""docs/ 认知基线 — refresh · diff · workflow-check · contracts-crosscheck · gate.

基线根目录（与 factoryos 工作流隔离）:
  .cursor/docs-baseline/
    policy/WORKFLOW_MAP.json
    manifest/MANIFEST.json
    mirror/docs/...
    reports/

Usage:
  python scripts/docs_baseline.py refresh
  python scripts/docs_baseline.py diff [--write-report]
  python scripts/docs_baseline.py workflow-check
  python scripts/docs_baseline.py contracts-crosscheck
  python scripts/docs_baseline.py gate          # PR 分级门禁
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASELINE = ROOT / ".cursor" / "docs-baseline"
POLICY_MAP = BASELINE / "policy" / "WORKFLOW_MAP.json"
MANIFEST_PATH = BASELINE / "manifest" / "MANIFEST.json"
MIRROR_ROOT = BASELINE / "mirror"
REPORTS_DIR = BASELINE / "reports"

TEXT_EXTENSIONS = {
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".csv",
    ".txt",
    ".py",
    ".gitkeep",
}
BINARY_EXTENSIONS = {".png", ".svg", ".xlsx", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}

TIER_A_GLOBS = [
    "docs/文档/架构/架构决策记录-*.md",
    "docs/文档/架构/编码绝对门禁.md",
    "docs/文档/架构/治理规范.md",
    "docs/文档/架构/os_core-public-api.md",
    "docs/文档/架构/能力-模块包-模块追溯矩阵.md",
    "docs/文档/架构/命名约定.md",
    "docs/文档/架构/架构闭合清单.md",
    "docs/文档/架构/膨胀期架构守则.md",
    "docs/文档/验收/*.md",
    "docs/文档/规格说明/DSL执行动词.md",
    "docs/文档/规格说明/Shadow-Mode与对账规格.md",
    "docs/文档/规格说明/规则引擎.md",
    "docs/文档/规格说明/执行与回滚.md",
    "docs/文档/规格说明/多租户与隔离.md",
]

TIER_C_PREFIXES = (
    "docs/文档/数据结构/",
    "docs/文档/接口/",
    "docs/scripts/",
)

TIER_C_CONTRACT_PAIRS: list[tuple[str, str]] = [
    ("docs/文档/数据结构/CMV注册表.yaml", "contracts/cmv/CMV注册表.yaml"),
    ("docs/文档/数据结构/CMV同步规则.md", "contracts/cmv/CMV同步规则.md"),
    ("docs/文档/接口/工厂操作系统-v1.1.yaml", "contracts/openapi/工厂操作系统-v1.1.yaml"),
]


@dataclass(frozen=True)
class FileEntry:
    path: str
    sha256: str
    tier: str
    mirrored: bool
    superseded_by: str | None = None
    size: int = 0


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_head() -> str | None:
    try:
        r = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if r.returncode == 0:
            return r.stdout.strip()
    except OSError:
        pass
    return None


def classify_tier(rel_path: str) -> str:
    for prefix in TIER_C_PREFIXES:
        if rel_path.startswith(prefix):
            return "C"
    ext = Path(rel_path).suffix.lower()
    if ext in BINARY_EXTENSIONS:
        return "D"
    for pattern in TIER_A_GLOBS:
        if fnmatch.fnmatch(rel_path, pattern):
            return "A"
    if rel_path.startswith("docs/"):
        return "B"
    return "B"


def superseded_target(rel_path: str) -> str | None:
    if rel_path.startswith("docs/文档/数据结构/"):
        name = Path(rel_path).name
        if name in ("CMV注册表.yaml", "CMV同步规则.md"):
            return f"contracts/cmv/{name}"
        return f"contracts/schemas/{name}"
    if rel_path.startswith("docs/文档/接口/"):
        return f"contracts/openapi/{Path(rel_path).name}"
    if rel_path.startswith("docs/scripts/"):
        return f"scripts/{Path(rel_path).name}"
    return None


def should_mirror(path: Path, tier: str) -> bool:
    if tier == "D":
        return False
    if path.suffix.lower() in TEXT_EXTENSIONS or path.suffix == "":
        return True
    return path.suffix.lower() in {".yaml", ".yml", ".json", ".csv", ".md", ".py"}


def iter_docs_files() -> list[Path]:
    if not DOCS.is_dir():
        return []
    files: list[Path] = []
    for p in sorted(DOCS.rglob("*")):
        if not p.is_file():
            continue
        rel_parts = p.relative_to(DOCS).parts
        if any(part.startswith(".") for part in rel_parts):
            continue
        if "__pycache__" in rel_parts:
            continue
        files.append(p)
    return files


def scan_docs() -> dict[str, FileEntry]:
    entries: dict[str, FileEntry] = {}
    for path in iter_docs_files():
        rel = rel_posix(path)
        tier = classify_tier(rel)
        digest = sha256_file(path)
        mirror = should_mirror(path, tier)
        entries[rel] = FileEntry(
            path=rel,
            sha256=digest,
            tier=tier,
            mirrored=mirror,
            superseded_by=superseded_target(rel) if tier == "C" else None,
            size=path.stat().st_size,
        )
    return entries


def load_manifest() -> dict | None:
    if not MANIFEST_PATH.is_file():
        return None
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def manifest_entries(manifest: dict) -> dict[str, FileEntry]:
    out: dict[str, FileEntry] = {}
    for item in manifest.get("files", []):
        out[item["path"]] = FileEntry(
            path=item["path"],
            sha256=item["sha256"],
            tier=item["tier"],
            mirrored=item.get("mirrored", False),
            superseded_by=item.get("superseded_by"),
            size=item.get("size", 0),
        )
    return out


def write_manifest(entries: dict[str, FileEntry]) -> None:
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_commit": git_head(),
        "docs_root": "docs/",
        "baseline_root": ".cursor/docs-baseline/",
        "file_count": len(entries),
        "tier_counts": {
            t: sum(1 for e in entries.values() if e.tier == t) for t in ("A", "B", "C", "D")
        },
        "files": [
            {
                "path": e.path,
                "sha256": e.sha256,
                "tier": e.tier,
                "mirrored": e.mirrored,
                **({"superseded_by": e.superseded_by} if e.superseded_by else {}),
                "size": e.size,
            }
            for e in sorted(entries.values(), key=lambda x: x.path)
        ],
    }
    MANIFEST_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sync_mirror(entries: dict[str, FileEntry]) -> None:
    desired: set[str] = set()
    for rel, entry in entries.items():
        if not entry.mirrored:
            continue
        src = ROOT / rel
        dest = MIRROR_ROOT / rel
        desired.add(rel)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(src.read_bytes())

    mirror_docs = MIRROR_ROOT / "docs"
    if mirror_docs.is_dir():
        for existing in mirror_docs.rglob("*"):
            if not existing.is_file():
                continue
            rel = existing.relative_to(MIRROR_ROOT).as_posix()
            if rel not in desired:
                existing.unlink()


def compare(
    current: dict[str, FileEntry], baseline: dict[str, FileEntry]
) -> tuple[list[str], list[str], list[str]]:
    cur_paths = set(current)
    base_paths = set(baseline)
    added = sorted(cur_paths - base_paths)
    removed = sorted(base_paths - cur_paths)
    modified: list[str] = []
    for path in sorted(cur_paths & base_paths):
        if current[path].sha256 != baseline[path].sha256:
            modified.append(path)
    return added, removed, modified


def load_workflow_map() -> list[dict]:
    if not POLICY_MAP.is_file():
        return []
    data = json.loads(POLICY_MAP.read_text(encoding="utf-8"))
    return data.get("rules", [])


def match_workflow_rules(paths: list[str]) -> list[dict]:
    rules = load_workflow_map()
    hits: list[dict] = []
    for path in paths:
        for rule in rules:
            pattern = rule.get("match", "")
            if fnmatch.fnmatch(path, pattern):
                hits.append({"path": path, **rule})
    return hits


def cmd_refresh() -> int:
    if not DOCS.is_dir():
        print("docs/ not found", file=sys.stderr)
        return 1
    entries = scan_docs()
    sync_mirror(entries)
    write_manifest(entries)
    tc = {t: sum(1 for e in entries.values() if e.tier == t) for t in "ABCD"}
    print(f"Baseline refreshed: {len(entries)} files")
    print(f"  Tier A={tc['A']} B={tc['B']} C={tc['C']} D={tc['D']}")
    print(f"  Manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"  Mirror:   {MIRROR_ROOT.relative_to(ROOT)}/docs/")
    return 0


def format_diff_report(
    added: list[str],
    removed: list[str],
    modified: list[str],
    current: dict[str, FileEntry],
    baseline: dict[str, FileEntry],
) -> str:
    lines = [
        "# docs baseline diff",
        "",
        f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        f"- Added: {len(added)}",
        f"- Removed: {len(removed)}",
        f"- Modified: {len(modified)}",
        "",
    ]
    for label, paths in ("Added", added), ("Removed", removed), ("Modified", modified):
        if not paths:
            continue
        lines.append(f"## {label}")
        lines.append("")
        for p in paths:
            tier = current.get(p) or baseline.get(p)
            t = tier.tier if tier else "?"
            lines.append(f"- `[{t}]` `{p}`")
        lines.append("")

    changed = added + removed + modified
    hits = match_workflow_rules(changed)
    if hits:
        lines.append("## Workflow map hits")
        lines.append("")
        seen: set[str] = set()
        for h in hits:
            key = h.get("id", h["path"])
            if key in seen:
                continue
            seen.add(key)
            affects = ", ".join(f"`{a}`" for a in h.get("affects", []))
            lines.append(f"- **{h.get('id', '?')}** (`{h['path']}`) → {affects}")
        lines.append("")
    return "\n".join(lines)


def cmd_diff(*, write_report: bool) -> int:
    manifest = load_manifest()
    if manifest is None:
        print("No baseline — run: ./scripts/docs_baseline refresh", file=sys.stderr)
        return 1
    current = scan_docs()
    baseline = manifest_entries(manifest)
    added, removed, modified = compare(current, baseline)
    report = format_diff_report(added, removed, modified, current, baseline)
    print(report)
    if write_report:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        out = REPORTS_DIR / "latest-diff.md"
        out.write_text(report, encoding="utf-8")
        print(f"\nWrote {out.relative_to(ROOT)}")
    if not added and not removed and not modified:
        print("\nDocs baseline in sync.")
        return 0
    print(f"\nDrift: +{len(added)} -{len(removed)} ~{len(modified)}")
    return 0


def cmd_workflow_check() -> int:
    manifest = load_manifest()
    if manifest is None:
        print("No baseline — run refresh first", file=sys.stderr)
        return 1
    current = scan_docs()
    baseline = manifest_entries(manifest)
    added, removed, modified = compare(current, baseline)
    changed = added + removed + modified
    tier_a = [p for p in changed if (current.get(p) or baseline.get(p)) and (current.get(p) or baseline.get(p)).tier == "A"]
    hits = match_workflow_rules(changed)
    if not changed:
        print("Workflow check OK — no docs drift")
        return 0
    print(f"Docs drift: {len(changed)} file(s); Tier-A: {len(tier_a)}")
    for p in tier_a:
        print(f"  [A] {p}")
    if hits:
        print("\nSuggested .cursor / contracts updates:")
        for h in hits:
            affects = ", ".join(h.get("affects", []))
            print(f"  {h.get('id', '?')}: {h['path']} → {affects}")
    return 1 if tier_a else 0


def schema_contract_path(docs_rel: str) -> str | None:
    name = Path(docs_rel).name
    if name in ("CMV注册表.yaml", "CMV同步规则.md"):
        return f"contracts/cmv/{name}"
    if docs_rel.startswith("docs/文档/数据结构/") and name.endswith(".schema.json"):
        return f"contracts/schemas/{name}"
    return None


def cmd_contracts_crosscheck(changed_only: list[str] | None = None) -> int:
    """若 changed_only 给定，仅检查本轮变更的 Tier-C 路径（gate 用）。"""
    errors: list[str] = []
    warnings: list[str] = []

    def check_pair(docs_rel: str, contract_rel: str) -> None:
        docs_path = ROOT / docs_rel
        contract_path = ROOT / contract_rel
        if not docs_path.is_file():
            return
        if changed_only is not None and docs_rel not in changed_only:
            return
        if not contract_path.is_file():
            errors.append(f"Missing contract for {docs_rel}: {contract_rel}")
            return
        if sha256_file(docs_path) != sha256_file(contract_path):
            msg = f"Content drift: {docs_rel} ≠ {contract_rel}"
            if changed_only is not None:
                errors.append(msg)
            else:
                warnings.append(msg)

    for docs_rel, contract_rel in TIER_C_CONTRACT_PAIRS:
        check_pair(docs_rel, contract_rel)

    schemas_docs = ROOT / "docs" / "文档" / "数据结构"
    if schemas_docs.is_dir():
        for docs_path in sorted(schemas_docs.glob("*.schema.json")):
            docs_rel = rel_posix(docs_path)
            contract_rel = schema_contract_path(docs_rel)
            if not contract_rel:
                continue
            if changed_only is not None and docs_rel not in changed_only:
                continue
            contract_path = ROOT / contract_rel
            if not contract_path.is_file():
                errors.append(f"Missing contracts mirror: {contract_rel} (from {docs_rel})")
                continue
            if sha256_file(docs_path) != sha256_file(contract_path):
                msg = f"Schema drift: {docs_rel} ≠ {contract_rel}"
                if changed_only is not None:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    if errors:
        print("contracts-crosscheck FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    if warnings:
        print("contracts-crosscheck WARN (legacy frozen drift — ok until Tier-C edits):")
        for w in warnings:
            print(f"  - {w}")
        return 0
    print("contracts-crosscheck OK (Tier-C docs ↔ contracts)")
    return 0


def cmd_gate() -> int:
    manifest = load_manifest()
    if manifest is None:
        print("FAIL: no docs baseline — run ./scripts/docs_baseline refresh", file=sys.stderr)
        return 1

    current = scan_docs()
    baseline = manifest_entries(manifest)
    added, removed, modified = compare(current, baseline)
    changed = added + removed + modified

    exit_code = 0
    tier_a = [p for p in changed if (current.get(p) or baseline.get(p)) and (current.get(p) or baseline.get(p)).tier == "A"]
    tier_b = [p for p in changed if (current.get(p) or baseline.get(p)) and (current.get(p) or baseline.get(p)).tier == "B"]
    tier_c = [p for p in changed if (current.get(p) or baseline.get(p)) and (current.get(p) or baseline.get(p)).tier == "C"]

    if tier_a:
        exit_code = 1
        print(f"FAIL Tier-A: {len(tier_a)} workflow-critical doc(s) changed without baseline refresh:")
        for p in tier_a:
            print(f"  - {p}")
        print("  → ./scripts/docs_baseline refresh && update .cursor/factoryos per workflow-check")

    if tier_b:
        print(f"WARN Tier-B: {len(tier_b)} reference doc(s) drift (refresh recommended):")
        for p in tier_b[:10]:
            print(f"  - {p}")
        if len(tier_b) > 10:
            print(f"  ... and {len(tier_b) - 10} more")

    if tier_c:
        print(f"INFO Tier-C: {len(tier_c)} superseded path(s) changed — contracts-crosscheck on deltas")

    cc = cmd_contracts_crosscheck(changed_only=tier_c if tier_c else [])
    if cc != 0:
        exit_code = 1

    if not changed:
        print("Gate docs-sync OK — baseline in sync")
    elif exit_code == 0:
        print("Gate docs-sync OK — only Tier-B drift (warn)")

    return exit_code


def main() -> int:
    p = argparse.ArgumentParser(description="FactoryOS docs cognitive baseline")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("refresh", help="Freeze docs/ into .cursor/docs-baseline/")
    sd = sub.add_parser("diff", help="Compare docs/ vs baseline manifest")
    sd.add_argument("--write-report", action="store_true", help="Write reports/latest-diff.md")
    sub.add_parser("workflow-check", help="Tier-A drift + WORKFLOW_MAP hits")
    sub.add_parser("contracts-crosscheck", help="Tier-C docs vs contracts/")
    sub.add_parser("gate", help="PR graded gate (A/C fail, B warn)")

    args = p.parse_args()
    if args.cmd == "refresh":
        return cmd_refresh()
    if args.cmd == "diff":
        return cmd_diff(write_report=args.write_report)
    if args.cmd == "workflow-check":
        return cmd_workflow_check()
    if args.cmd == "contracts-crosscheck":
        return cmd_contracts_crosscheck()
    if args.cmd == "gate":
        return cmd_gate()
    return 1


if __name__ == "__main__":
    sys.exit(main())

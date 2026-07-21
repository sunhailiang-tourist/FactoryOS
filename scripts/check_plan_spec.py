#!/usr/bin/env python3
"""Validate Dev plan markdown against contracts/ + 工作流 plan 结构门禁（stdlib only）。

Usage:
  python scripts/check_plan_spec.py
  python scripts/check_plan_spec.py --plan _factoryos_pipeline/2026-07-21/plan/plan-….md
  python scripts/check_plan_spec.py --plan … --legacy   # 仅 AC/HTTP，跳过 v2 结构

Exit 0 = OK；1 = gaps。

机械门禁（默认 · 与 STEP0/plan-template 对齐）：
  · §4 Step 总览 + ≥1 个 ### Step N
  · 每 Step 含函数/文件落位/入参/返回（标题或关键字）
  · 类型=新功能 → 同目录 materials-*.md 或材料准入路径有效
  · UI 命中=是 → §8.2 存在且无「待实现/未知/未确认」
  · AC ID ∈ contracts/acceptance；HTTP 路径 ∈ OpenAPI（有则查）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"
ACCEPTANCE_DIR = ROOT / "contracts" / "acceptance"
OPENAPI = ROOT / "contracts" / "openapi" / "工厂操作系统-v1.1.yaml"

AC_RE = re.compile(r"\b([A-Z][A-Z0-9]*-\d{2})\b")
HTTP_RE = re.compile(
    r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/v1/[A-Za-z0-9_./{}-]+)",
    re.IGNORECASE,
)
TYPE_RE = re.compile(r"\*\*类型\*\*[：:]\s*(.+)")
MATERIALS_RE = re.compile(r"\*\*材料准入\*\*[：:]\s*(.+)")
STEP_HEAD_RE = re.compile(r"^###\s+Step\s+(\d+)\b", re.MULTILINE | re.IGNORECASE)
UI_HIT_RE = re.compile(
    r"命中(?:判定)?\*\*[：:]\s*\*?\*?\s*(是|否)|"
    r"\*\*命中(?:判定)?\*\*[：:]\s*(是|否)|"
    r"命中(?:判定)?[：:]\s*(是|否)",
)
FORBIDDEN_UI_STATUS = re.compile(r"待实现|未知|未确认")
LEGACY_MARK = re.compile(r"plan_format\s*[：:]\s*legacy", re.IGNORECASE)


def latest_plan() -> Path | None:
    candidates = sorted(
        (
            p
            for p in PIPELINE.glob("*/plan/plan-*.md")
            if "draft" not in p.name.lower()
        ),
        key=lambda p: p.stat().st_mtime,
    )
    return candidates[-1] if candidates else None


def load_acceptance_text() -> str:
    parts: list[str] = []
    if ACCEPTANCE_DIR.is_dir():
        for p in sorted(ACCEPTANCE_DIR.glob("*.md")):
            parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def load_openapi_text() -> str:
    if not OPENAPI.is_file():
        return ""
    return OPENAPI.read_text(encoding="utf-8")


def _section_after(text: str, heading_pat: str) -> str:
    """取匹配标题之后到下一同级 ## 之前的文本。"""
    m = re.search(heading_pat, text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"\n##\s+", rest)
    return rest[: nxt.start()] if nxt else rest


def check_contracts(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    ac_ids = sorted(set(AC_RE.findall(text)))
    http_ops = sorted(set(HTTP_RE.findall(text)))

    if not ac_ids:
        errors.append(f"{path}: no AC IDs found (expect G-01, STU-01, CMNT-01, …)")
        return errors

    acceptance = load_acceptance_text()
    openapi = load_openapi_text()

    for ac_id in ac_ids:
        if ac_id not in acceptance:
            errors.append(f"{path}: AC {ac_id} not found in contracts/acceptance/")

    for method, api_path in http_ops:
        norm_path = api_path.split("{")[0].rstrip("/")
        if openapi and norm_path and norm_path not in openapi:
            errors.append(
                f"{path}: {method.upper()} {api_path} not found in contracts/openapi"
            )

    return errors


def check_structure_v2(path: Path, text: str) -> list[str]:
    errors: list[str] = []

    if not re.search(r"##\s*4[\.．]?\s*.*Step\s*总览", text, re.IGNORECASE):
        errors.append(
            f"{path}: 缺少「## 4. Step 总览」— plan-template v2 硬要求（见 DEV-GATES Gate 3）"
        )

    steps = list(STEP_HEAD_RE.finditer(text))
    if not steps:
        errors.append(
            f"{path}: 缺少「### Step N」展开节 — 禁止只有总览不展开（plan-template §6）"
        )
        return errors

    for i, m in enumerate(steps):
        start = m.start()
        end = steps[i + 1].start() if i + 1 < len(steps) else len(text)
        # 截断到下一个 ## （非 ###）以免吞掉 §7+
        chunk = text[start:end]
        cut = re.search(r"\n##\s+[^#]", chunk[1:])
        if cut:
            chunk = chunk[: cut.start() + 1]
        n = m.group(1)
        for label, pat in (
            ("函数", r"函数|6\.3"),
            ("文件落位", r"文件落位|6\.4"),
            ("入参", r"入参|6\.6"),
            ("返回", r"返回|6\.7"),
        ):
            if not re.search(pat, chunk, re.IGNORECASE):
                errors.append(
                    f"{path}: Step {n} 缺少「{label}」表/节（须含关键字或 6.x 标题）"
                )

    return errors


def _resolve_materials_ref(plan_path: Path, raw: str) -> Path | None:
    raw = raw.strip().strip("`").strip()
    if not raw or raw.upper().startswith("N/A"):
        return None
    # 取第一个路径样 token
    token = re.split(r"[\s（(]", raw, maxsplit=1)[0].strip("`")
    p = Path(token)
    if not p.is_absolute():
        cand = ROOT / token
        if cand.is_file():
            return cand
        sibling = plan_path.parent / Path(token).name
        if sibling.is_file():
            return sibling
    return p if p.is_file() else None


def check_materials(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    type_m = TYPE_RE.search(text)
    mat_m = MATERIALS_RE.search(text)
    type_val = type_m.group(1).strip() if type_m else ""
    mat_val = mat_m.group(1).strip() if mat_m else ""
    is_new = "新功能" in type_val
    hits = sorted(path.parent.glob("materials-*.md"))

    def mat_is_na(val: str) -> bool:
        return bool(re.search(r"\bN/A\b", val, re.IGNORECASE))

    if not is_new:
        if mat_m and not mat_is_na(mat_val):
            resolved = _resolve_materials_ref(path, mat_val)
            if resolved is None and not hits:
                errors.append(
                    f"{path}: 材料准入未解析到文件，且同目录无 materials-*.md "
                    f"（声明={mat_val!r}）"
                )
        return errors

    # 新功能：禁止 N/A；须有 materials 文件
    if mat_m and mat_is_na(mat_val):
        errors.append(f"{path}: 类型=新功能 禁止「材料准入：N/A」")
        return errors

    if mat_m and not mat_is_na(mat_val):
        resolved = _resolve_materials_ref(path, mat_val)
        if resolved is not None:
            return errors
        if hits:
            return errors
        errors.append(
            f"{path}: 材料准入未解析到文件，且同目录无 materials-*.md "
            f"（声明={mat_val!r}）"
        )
        return errors

    if not hits:
        errors.append(
            f"{path}: 类型=新功能 须落盘 materials-*.md 或声明「材料准入」有效路径"
        )
    return errors


def check_ui_reconcile(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    m = UI_HIT_RE.search(text)
    if not m:
        # 未声明命中 → 若有 §8 标题但无判定，提示；不硬失败（允许缺 §8=未命中）
        return errors

    hit = next(g for g in m.groups() if g)
    if hit != "是":
        return errors

    sec8 = _section_after(text, r"^##\s*8[\.．]?.*UI")
    if not sec8:
        errors.append(
            f"{path}: UI 对账命中=是，但缺少「## 8 … UI」节（plan-template §8）"
        )
        return errors
    if not re.search(r"8\.2|接口字段对账", sec8):
        errors.append(f"{path}: UI 命中=是，缺少 §8.2 接口字段对账表")
    if FORBIDDEN_UI_STATUS.search(sec8):
        errors.append(
            f"{path}: UI §8 仍含「待实现/未知/未确认」— 禁止 gate plan / 可以开始"
        )
    return errors


def check_plan(path: Path, *, legacy: bool = False) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = check_contracts(path, text)

    if legacy or LEGACY_MARK.search(text):
        return errors

    errors.extend(check_structure_v2(path, text))
    errors.extend(check_materials(path, text))
    errors.extend(check_ui_reconcile(path, text))
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Plan ↔ contracts + v2 结构门禁")
    p.add_argument("--plan", type=Path, help="plan markdown path (default: latest)")
    p.add_argument(
        "--legacy",
        action="store_true",
        help="仅 AC/HTTP 对账，跳过 Step 总览/材料/UI 结构门禁",
    )
    args = p.parse_args()

    plan = args.plan or latest_plan()
    if plan is None or not plan.is_file():
        print("No plan file found under _factoryos_pipeline/*/plan/", file=sys.stderr)
        return 1

    errors = check_plan(plan.resolve(), legacy=args.legacy)
    if errors:
        print("Plan/spec mismatches:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    mode = "legacy" if args.legacy or LEGACY_MARK.search(plan.read_text(encoding="utf-8")) else "v2"
    print(f"Plan/spec OK ({mode}): {plan.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

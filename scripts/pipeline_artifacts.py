#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流落盘工件（dev/test/verify）工具（stdlib only）。

作用：
- 把“当天工作产物（计划/结论/验收结论/回归结论）”统一落到 `_factoryos_pipeline/<YYYY-MM-DD>/`。
- 目录结构固定为：`dev/`、`test/`、`verify/` 三类；文件按 `HH-MM`（UTC）前缀，天然可排序复盘。

业务关联：
- SH-步步流：强调“落盘可追溯”，但不强制把 gate 输出写入文件；本工具补齐“强制输出”。

上游：
- `scripts/gate_cli.py` 在 `gate plan/test/step/pr/verify` 执行后调用。

下游：
- 人工复盘/交接只关注当天目录；Verify 回合可直接引用这些结论文件。
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"


@dataclass(frozen=True)
class ArtifactRef:
    """落盘工件引用。

    字段含义：
    - bucket: 三类之一：dev/test/verify
    - path: 绝对路径
    - relpath: 相对仓库根路径（用于日志/提示）
    """

    bucket: str
    path: Path
    relpath: str


def utc_date_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def utc_time_hm() -> str:
    return datetime.now(timezone.utc).strftime("%H-%M")


def ensure_bucket_dir(bucket: str) -> Path:
    if bucket not in {"dev", "test", "verify"}:
        raise ValueError(f"invalid bucket={bucket!r}")
    d = PIPELINE / utc_date_str() / bucket
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_artifact(
    *,
    bucket: str,
    stem: str,
    content: str,
    suffix: str = ".md",
) -> ArtifactRef:
    """写入一份落盘工件。

    参数/返回业务说明：
    - bucket: dev/test/verify 三类之一
    - stem: 文件名主体（不含时间前缀和后缀），例如 `gate-step_step1`
    - content: 工件正文（建议 Markdown）
    - suffix: 默认 `.md`
    """

    d = ensure_bucket_dir(bucket)
    ts = utc_time_hm()
    safe_stem = stem.strip().replace(" ", "_")
    path = d / f"{ts}_{safe_stem}{suffix}"
    path.write_text(content, encoding="utf-8")
    return ArtifactRef(bucket=bucket, path=path, relpath=str(path.relative_to(ROOT)))


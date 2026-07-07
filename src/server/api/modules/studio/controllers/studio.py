"""Studio 域 HTTP 路由（GET /v1/studio/flows）。

作用：暴露 Integration Studio 六步向导导航；RBAC 由 AuthMiddleware 守门。
业务关联：STU-09 · web-admin `/studio/*` 拉取步骤定义。
上游：modules/studio/routers · AuthMiddleware（X-Actor-Role）
下游：data/studio_wizard_steps.json
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Request

_DATA_DIR = Path(__file__).resolve().parents[3] / "data"
_WIZARD_FILE = _DATA_DIR / "studio_wizard_steps.json"

router = APIRouter(tags=["Studio"])


@lru_cache(maxsize=1)
def _load_wizard_steps() -> dict[str, Any]:
  """加载六步向导 JSON（进程内缓存，export 镜像非运行时真源）。"""
  raw = _WIZARD_FILE.read_text(encoding="utf-8")
  return json.loads(raw)


@router.get("/v1/studio/flows")
def get_studio_flows_http(request: Request) -> dict[str, Any]:
  """GET /v1/studio/flows — Studio 六步导航（STU-09 integrator 200）。

  功能：返回六步向导 JSON 并附带当前 actor_role。
  业务含义：web-admin /studio/* 拉取步骤定义与 RBAC 上下文。
  上游：AuthMiddleware 注入 request.state.actor_role。
  下游：data/studio_wizard_steps.json。
  """
  payload = _load_wizard_steps()
  role = getattr(request.state, "actor_role", None)
  return {
    **payload,
    "actor_role": role,
  }

"""Probes 域 HTTP 路由（/health · /ready）。

作用：进程存活与就绪探针；无业务逻辑。
业务关联：K8s 探针（非 OpenAPI 正式域）。
上游：modules/probes/routers。
下游：无（进程内返回 status ok）。
"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Probes"])


@router.get("/health")
def health() -> dict[str, str]:
  """GET /health 进程存活探针。

  功能：返回进程存活状态。
  业务含义：K8s liveness 检查（非 OpenAPI 正式域）。
  上游：kubelet HTTP GET。
  返回：{"status": "ok"}。
  """
  return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str]:
  """GET /ready 就绪探针。

  功能：返回进程就绪状态。
  业务含义：K8s readiness 检查（S0 与 health 等价）。
  上游：kubelet HTTP GET。
  返回：{"status": "ok"}。
  """
  return {"status": "ok"}

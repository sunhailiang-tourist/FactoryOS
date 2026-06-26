"""进程探针 /health · /ready。"""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["Probes"])


@router.get("/health")
def health() -> dict[str, str]:
  """进程存活探针（非 OpenAPI 正式域）。"""
  return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str]:
  """就绪探针（S0 与 health 等价）。"""
  return {"status": "ok"}

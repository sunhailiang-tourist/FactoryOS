"""integration GIP 外置注册表 — Pack · Tenant · Catalog 清单。

作用：统一管理 integration/ 子树；每条须 summary/problem/usage。
业务关联：ADR-004 GIP · ADR-008 export 镜像 · check_integration_registry。
关联文档：docs/文档/架构/配置枢纽与关系模型.md
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class IntegrationMount:
  """integration 子树挂载点（打开本文件即可见职责与用法）。"""

  name: str
  path: str
  summary: str
  problem: str
  usage: str


ROOT = Path(__file__).resolve().parent

INTEGRATION_MOUNTS: tuple[IntegrationMount, ...] = (
  IntegrationMount(
    name="catalog",
    path="catalog",
    summary="连接器类型目录（只读镜像）",
    problem="Pack Blueprint 须与 platform_registry seed 对齐，避免散落 YAML",
    usage="integration/catalog/*.yaml；bootstrap 导入 · Studio 选 Pack 类型",
  ),
  IntegrationMount(
    name="packs",
    path="packs",
    summary="Graph · Conn · Rule Pack 文件",
    problem="交付物须文件化 export，便于 Git/Studio 导入导出",
    usage="packs/<tenant>/ 下 graph/rule/conn 包；Package import/export API",
  ),
  IntegrationMount(
    name="tenants",
    path="tenants",
    summary="租户模板与 export 镜像",
    problem="租户 shadow_mode · licensed_packs 须可配置、可审计",
    usage="tenants/<id>/settings.json；PUT /v1/tenants/{id}/settings（W7+）",
  ),
  IntegrationMount(
    name="tools",
    path="tools",
    summary="guide · connector-agent 工具",
    problem="实施/运维脚本须与 GIP 同仓、版本对齐",
    usage="tools/guide/flows.json · connector-agent CLI；非 runtime 热路径",
  ),
)


def integration_mount_names() -> tuple[str, ...]:
  """已登记 integration 挂载名。"""
  return tuple(m.name for m in INTEGRATION_MOUNTS)


def validate_integration_mounts() -> list[str]:
  """磁盘目录 ⊆ 注册表；返回错误列表。"""
  errors: list[str] = []
  for mount in INTEGRATION_MOUNTS:
    if not (ROOT / mount.path).is_dir():
      errors.append(f"missing integration/{mount.path}")
  on_disk = {p.name for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")}
  registered = set(integration_mount_names())
  extra = sorted(on_disk - registered - {"__pycache__"})
  if extra:
    errors.append(f"unregistered integration dirs: {extra}")
  return errors

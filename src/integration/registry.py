"""integration GIP 外置注册表 — Pack · Tenant · Catalog 清单。

作用：统一管理 integration/ 子树；与 platform_registry seed 对齐。
业务关联：ADR-004 GIP · ADR-008 export 镜像。
关联文档：docs/文档/架构/配置枢纽与关系模型.md
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class IntegrationMount:
  """integration 子树挂载点。"""

  name: str
  path: str
  summary: str


ROOT = Path(__file__).resolve().parent

INTEGRATION_MOUNTS: tuple[IntegrationMount, ...] = (
  IntegrationMount("catalog", "catalog", "连接器类型目录（只读镜像）"),
  IntegrationMount("packs", "packs", "Graph · Conn · Rule Pack 文件"),
  IntegrationMount("tenants", "tenants", "租户模板与 export 镜像"),
  IntegrationMount("tools", "tools", "guide · connector-agent 工具"),
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

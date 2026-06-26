"""Legacy mock 写计数（W2 E-06/E-07 验收）。

作用：dry_run 时禁止调用；非 dry_run 时递增计数供测试断言。
业务关联：唯一写 Legacy 经 connector_sdk；W2 无真实 HTTP。
上游：execution_service
下游：integration test E-06 · E-07
关联文档：contracts/acceptance E-06 · E-07
"""
from __future__ import annotations

_write_count: int = 0


def reset_write_count() -> None:
  """重置 mock Legacy 写次数（测试前置）。"""
  global _write_count
  _write_count = 0


def get_write_count() -> int:
  """返回 mock Legacy 累计写次数。"""
  return _write_count


def mock_legacy_write(*, pack_id: str, verb: str) -> None:
  """模拟 Connector 写 Legacy（非 dry_run 路径）。

  功能：递增全局写计数。
  参数 pack_id：Pack 标识
  参数 verb：CMV 动词
  """
  global _write_count
  _ = pack_id, verb
  _write_count += 1

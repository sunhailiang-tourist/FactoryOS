"""AC-BASE-001 注册表：52 P0 用例以 pending 红测占位，驱动 W1+ TDD 红→绿。

每个用例在实现前 pytest 收集为 xfail(strict)；实现完成后去掉 pending 标记即可变绿。
"""
from __future__ import annotations

import pytest

from tests.ac_registry import load_ac_ids

AC_IDS = load_ac_ids()
# W1/W2 plan 已拆出独立 failing tests，不再走 pending 占位
ACTIVE_AC_IDS = frozenset({
  "S-01", "S-02", "S-03", "S-04", "C-01",
  "E-03", "E-06", "E-07", "E-09",
})
PENDING_AC_IDS = [ac_id for ac_id in AC_IDS if ac_id not in ACTIVE_AC_IDS]


@pytest.mark.pending
@pytest.mark.parametrize("ac_id", PENDING_AC_IDS)
def test_ac_pending_until_implemented(ac_id: str) -> None:
  pytest.fail(
    f"AC {ac_id} not implemented — W1+ Step 按 plan 实现后移除此 pending 或改为真实断言"
  )

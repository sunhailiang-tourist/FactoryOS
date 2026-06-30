"""W6 Step1：license_service 内核 stub · assert_pack_licensed（workflow 门禁）。

业务：静态 licensed_packs 校验；未实现时红测。
上游：plan Step1 · os_core.license_service
下游：gate step --step 1 -k 'workflow'
"""
from __future__ import annotations

import importlib

import pytest


def _get_assert_pack_licensed():
  """导入 W6 Step1 内核 assert_pack_licensed（未实现时红测）。"""
  module = importlib.import_module("os_core.license_service")
  fn = getattr(module, "assert_pack_licensed", None)
  assert fn is not None, "缺少 os_core.license_service.assert_pack_licensed"
  return fn


@pytest.mark.integration
@pytest.mark.parametrize("case", ["licensed"], ids=["workflow"])
def test_w6_step1_assert_pack_licensed_allows_known_pack(case: str) -> None:
  """Step1：default tenant 的 conn-mock 在 licensed 列表内。"""
  assert_pack_licensed = _get_assert_pack_licensed()
  assert_pack_licensed(tenant_id="default", pack_id="conn-mock")

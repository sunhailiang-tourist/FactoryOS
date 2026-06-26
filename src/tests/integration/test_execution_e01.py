"""W3 E-01：L0 QUERY_ENTITY on frozen graph。"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from os_core.connector_sdk import mock_legacy


@pytest.mark.integration
@pytest.mark.parametrize("case", ["query"], ids=["E-01"])
def test_E01_l0_query_on_frozen_graph(
  case: str,
  api_client: TestClient,
  frozen_graph_env: dict,
) -> None:
  mock_legacy.reset_write_count()
  resp = api_client.post(
    "/v1/execute",
    json={
      "tenant_id": "default",
      "graph_id": frozen_graph_env["graph_id"],
      "graph_version": frozen_graph_env["version"],
      "verb": "QUERY_ENTITY",
      "params": {"entity_type": "work_order", "entity_id": "wo-1"},
      "ruleset_id": frozen_graph_env["ruleset_id"],
      "actor": {"user_id": "u1", "role": "operator", "channel": "api"},
    },
  )
  assert resp.status_code == 200, resp.text
  assert mock_legacy.get_write_count() == 0

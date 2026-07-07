"""阶段1 Step1：STU-09 integrator RBAC · web-admin Studio 壳。

业务：operator 访问 Studio API 403 · integrator 200。
上游：plan Step1 · Integration-Studio 规格 §4
下游：gate step --step 1 -k 'STU-09'
"""
from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from tests.integration.stu_helpers import get_studio_flows

ROOT = Path(__file__).resolve().parents[3]
WEB_ADMIN = ROOT / "src" / "apps" / "web-admin"


@pytest.mark.integration
@pytest.mark.parametrize("case", ["operator_forbidden"], ids=["STU-09"])
def test_STU09_operator_cannot_access_studio_flows(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-09：role:operator 访问 Studio → 403。"""
  resp = get_studio_flows(api_client, role="operator")
  assert resp.status_code == 403, resp.text


@pytest.mark.integration
@pytest.mark.parametrize("case", ["integrator_allowed"], ids=["STU-09-integrator"])
def test_STU09_integrator_can_access_studio_flows(
  case: str,
  api_client: TestClient,
) -> None:
  """STU-09：role:integrator 可读取 Studio 六步 flows。"""
  resp = get_studio_flows(api_client, role="integrator")
  assert resp.status_code == 200, resp.text
  body = resp.json()
  steps = body.get("steps") or body.get("flows") or []
  assert len(steps) >= 6, "Studio 须暴露至少六步向导（connect→export）"


@pytest.mark.workflow
@pytest.mark.parametrize("case", ["scaffold"], ids=["STU-09-scaffold"])
def test_STU09_web_admin_studio_scaffold_exists(case: str) -> None:
  """Step1：web-admin Vite 脚手架与 /studio 入口文件存在。"""
  assert (WEB_ADMIN / "package.json").is_file(), "缺少 web-admin/package.json"
  assert (WEB_ADMIN / "vite.config.ts").is_file() or (
    WEB_ADMIN / "vite.config.js"
  ).is_file(), "缺少 vite.config"
  src = WEB_ADMIN / "src"
  assert src.is_dir(), "缺少 web-admin/src"
  studio_markers = list(src.rglob("*studio*"))
  assert studio_markers, "缺少 /studio 相关源码（layout 或 pages/studio）"

"""WEB-PROFILE W-11 Standalone S 红测（Test Agent · 非验收盘）。

业务：迁出仓零父仓 activate 前置条件
上游：plan-web-admin-w11-standalone.md · test-1710
下游：Dev Step1～2 实现后变绿
"""
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
WEB_ADMIN = ROOT / "src" / "apps" / "web-admin"
VENDOR_CONTRACTS = WEB_ADMIN / "vendor" / "factoryos-contracts"
STANDALONE_MANIFEST = WEB_ADMIN / "devkit.manifest.standalone.yaml"
CODEGEN_CHECK = WEB_ADMIN / "scripts" / "check_codegen_fresh.py"
SIMULATE_ACTIVATE = WEB_ADMIN / "scripts" / "simulate_standalone_activate.sh"
STANDALONE_READY = WEB_ADMIN / "scripts" / "check_standalone_ready.py"
PROFILE = WEB_ADMIN / "devkit.profile.yaml"


@pytest.mark.parametrize(
  "case",
  [
    "W-11a-vendor-contracts",
    "W-11b-codegen-dual-path",
    "W-11c-simulate-activate",
    "W-11d-harness-profile",
    "W-11e-standalone-ready-script",
  ],
)
def test_W11_standalone_prerequisites(case: str) -> None:
  """W-11：standalone 迁出前置 — Dev 实现前须 FAIL。"""
  if case == "W-11a-vendor-contracts":
    openapi = VENDOR_CONTRACTS / "openapi"
    assert openapi.is_dir(), (
      "missing vendor/factoryos-contracts/openapi — "
      "standalone 须 pin 契约镜像（见 devkit.manifest.standalone.yaml）"
    )
    yaml_files = list(openapi.glob("*.yaml")) + list(openapi.glob("*.yml"))
    assert yaml_files, "vendor openapi dir empty"

  elif case == "W-11b-codegen-dual-path":
    text = CODEGEN_CHECK.read_text(encoding="utf-8")
    assert "vendor" in text and "factoryos-contracts" in text, (
      "check_codegen_fresh.py must resolve OpenAPI from vendor in standalone mode"
    )

  elif case == "W-11c-simulate-activate":
    assert SIMULATE_ACTIVATE.is_file(), (
      "missing scripts/simulate_standalone_activate.sh — "
      "CI/红测须可复现零父仓 activate"
    )

  elif case == "W-11d-harness-profile":
    raw = PROFILE.read_text(encoding="utf-8")
    assert "standalone_ready" in raw, (
      "devkit.profile.yaml must register standalone_ready harness check"
    )

  elif case == "W-11e-standalone-ready-script":
    assert STANDALONE_READY.is_file(), (
      "missing scripts/check_standalone_ready.py — W-11 harness 子脚本"
    )

  assert STANDALONE_MANIFEST.is_file(), "devkit.manifest.standalone.yaml missing"

"""Registry harness 闭环（kernel · router · integration）。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"


@pytest.mark.workflow
def test_kernel_registry_harness_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "check_kernel_registry.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr or r.stdout


@pytest.mark.workflow
def test_router_registry_harness_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "check_router_registry.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr or r.stdout


@pytest.mark.workflow
def test_main_has_no_include_router() -> None:
  main = (ROOT / "src/server/api/main.py").read_text(encoding="utf-8")
  assert "include_router" not in main


@pytest.mark.workflow
def test_os_core_registry_lists_kernel_modules() -> None:
  sys.path.insert(0, str(ROOT / "src" / "server"))
  from os_core.registry import kernel_module_names

  names = kernel_module_names()
  assert "platform_registry" in names
  assert "execution_service" in names
  assert "license_service" in names
  assert "reconciliation_service" in names
  assert len(names) == 11


@pytest.mark.workflow
def test_integration_registry_harness_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "check_integration_registry.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr or r.stdout


@pytest.mark.workflow
def test_legacy_paths_harness_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "check_legacy_paths.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr or r.stdout


@pytest.mark.workflow
def test_repo_structure_harness_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "check_repo_structure.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr or r.stdout


@pytest.mark.workflow
def test_path_consistency_harness_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "audit_path_consistency.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr or r.stdout


@pytest.mark.workflow
def test_structure_change_gate_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "check_structure_change.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr or r.stdout

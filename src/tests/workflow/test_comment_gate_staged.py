"""CMNT-C staged 注释门禁单测（精准识别 · 双速双严）。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import comment_fix_lib as cfl  # noqa: E402
import comment_gate_git as cgg  # noqa: E402
from check_comments import run_check  # noqa: E402


def _bad_py() -> str:
  return "def handler() -> None:\n  pass\n"


def _good_py() -> str:
  return (
    '"""\n'
    "模块：src/server/api/modules/good.py\n"
    "作用：单测夹具合格模块，用于验证 staged 仅审缓存区文件。\n"
    "业务关联：CMNT-C 注释闭环验收。\n"
    "上游：pytest 夹具。\n"
    "下游：check_comments --staged。\n"
    '"""\n'
    "def ok() -> None:\n"
    '  """功能：x\n  业务含义：y\n  上游：a\n  下游：b\n  参数：无\n  返回：无\n  异常：无\n  """\n'
    "  pass\n"
  )


def _bad_ts() -> str:
  return "export function useDemo() {\n  return 1;\n}\n"


@pytest.fixture()
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
  monkeypatch.setattr(cgg, "ROOT", tmp_path)
  return tmp_path


def test_filter_gate_paths_python_and_ts(repo: Path) -> None:
  py_file = repo / "src/server/api/modules/a.py"
  py_file.parent.mkdir(parents=True)
  py_file.write_text("x", encoding="utf-8")
  ts_file = repo / "src/apps/web-admin/src/a.ts"
  ts_file.parent.mkdir(parents=True)
  ts_file.write_text("x", encoding="utf-8")

  py, ts = cgg.filter_gate_paths(
    [
      "src/server/api/modules/a.py",
      "src/apps/web-admin/src/a.ts",
      "src/apps/web-admin/src/api/generated/x.ts",
      "src/tests/foo.py",
      "README.md",
    ]
  )
  assert len(py) == 1
  assert py[0].name == "a.py"
  assert len(ts) == 1
  assert ts[0].name == "a.ts"


def test_staged_violation_blocks_only_staged(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
  good = repo / "src/server/api/modules/good.py"
  good.parent.mkdir(parents=True)
  good.write_text(_good_py(), encoding="utf-8")
  bad = repo / "src/server/api/modules/bad.py"
  bad.write_text(_bad_py(), encoding="utf-8")

  monkeypatch.setattr(cgg, "git_staged_relpaths", lambda: ["src/server/api/modules/good.py"])
  errors, py_n, _ = run_check("staged")
  assert py_n == 1
  assert errors == []

  monkeypatch.setattr(
    cgg,
    "git_staged_relpaths",
    lambda: ["src/server/api/modules/good.py", "src/server/api/modules/bad.py"],
  )
  errors2, py_n2, _ = run_check("staged")
  assert py_n2 == 2
  assert any("bad.py" in e for e in errors2)


def test_unstaged_bad_does_not_block_staged_check(
  repo: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
  good = repo / "src/server/api/modules/only_good.py"
  good.parent.mkdir(parents=True)
  good.write_text(_good_py(), encoding="utf-8")
  bad = repo / "src/server/api/modules/unstaged_bad.py"
  bad.write_text(_bad_py(), encoding="utf-8")

  monkeypatch.setattr(cgg, "git_staged_relpaths", lambda: ["src/server/api/modules/only_good.py"])
  errors, _, _ = run_check("staged")
  assert errors == []


def test_comment_fix_staged_then_green(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
  path = repo / "src/server/api/modules/fixme.py"
  path.parent.mkdir(parents=True)
  path.write_text(_bad_py(), encoding="utf-8")
  monkeypatch.setattr(cgg, "git_staged_relpaths", lambda: ["src/server/api/modules/fixme.py"])

  errors_before, _, _ = run_check("staged")
  assert errors_before

  assert cfl.fix_python_file(path)
  errors_after, _, _ = run_check("staged")
  assert errors_after == [], "\n".join(errors_after)


def test_ts_staged_header_and_export(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
  path = repo / "src/apps/web-admin/src/demo/useX.ts"
  path.parent.mkdir(parents=True)
  path.write_text(_bad_ts(), encoding="utf-8")
  rel = "src/apps/web-admin/src/demo/useX.ts"
  monkeypatch.setattr(cgg, "git_staged_relpaths", lambda: [rel])

  errors, _, ts_n = run_check("staged")
  assert ts_n == 1
  assert errors

  assert cfl.fix_ts_file(path)
  errors2, _, _ = run_check("staged")
  assert errors2 == [], "\n".join(errors2)


def test_staged_empty_paths_ok(monkeypatch: pytest.MonkeyPatch) -> None:
  monkeypatch.setattr(cgg, "git_staged_relpaths", lambda: [])
  errors, py_n, ts_n = run_check("staged")
  assert errors == []
  assert py_n == 0
  assert ts_n == 0


def test_commit_hook_non_interactive_blocks(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
  path = repo / "src/server/api/modules/hook_bad.py"
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(_bad_py(), encoding="utf-8")
  monkeypatch.setattr(cgg, "git_staged_relpaths", lambda: ["src/server/api/modules/hook_bad.py"])

  from check_comments_commit_hook import run_commit_hook  # noqa: E402

  assert run_commit_hook(interactive=False) == 1


def test_classify_errors_has_p0() -> None:
  from check_comments_commit_hook import _classify_errors  # noqa: E402

  buckets = _classify_errors(["a.py:1: f — missing docstring"])
  assert "P0" in buckets


def test_check_comments_cli_full_green() -> None:
  r = subprocess.run(
    [sys.executable, str(SCRIPTS / "check_comments.py"), "--full"],
    cwd=ROOT,
    capture_output=True,
    text=True,
  )
  assert r.returncode == 0, r.stderr
  assert "OK" in r.stdout

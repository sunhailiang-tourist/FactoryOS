"""comment_gate_lib 单元测试（P1～P3 规则可靠性）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import comment_gate_lib as cg  # noqa: E402

_HEADER = (
  '"""测试模块。\n\n'
  "作用：单测夹具。\n"
  "业务关联：comment_gate_lib 规则验证。\n"
  "上游：pytest。\n"
  "下游：check_python_comments.py。\n"
  '"""\n'
)


def _write(tmp_path: Path, name: str, body: str) -> Path:
  p = tmp_path / name
  p.write_text(_HEADER + body, encoding="utf-8")
  return p


def test_p1_field_requires_description(tmp_path: Path) -> None:
  p = _write(
    tmp_path,
    "m.py",
    "from pydantic import BaseModel, Field\n\n"
    "class M(BaseModel):\n"
    '  ok: str = Field(description="好")\n'
    "  bad: str\n",
  )
  errs = cg.check_file_rules(p)
  assert any("bad" in e and "Field(description" in e for e in errs)


def test_p3_platform_error_doc(tmp_path: Path) -> None:
  p = _write(
    tmp_path,
    "s.py",
    "from os_core.shared_contracts.exceptions import PlatformError\n\n"
    "def go() -> None:\n"
    '  """功能：测。\n\n'
    "  业务含义：抛错。\n"
    "  上游：无。\n"
    "  下游：无。\n"
    '  """\n'
    '  raise PlatformError("X", "msg")\n',
  )
  errs = cg.check_file_rules(p)
  assert any("PlatformError" in e and "异常" in e for e in errs)


def test_p2_block_comment(tmp_path: Path) -> None:
  p = _write(
    tmp_path,
    "c.py",
    "def long_fn() -> int:\n"
    '  """功能：测。\n\n'
    "  业务含义：累加。\n"
    "  上游：无。\n"
    "  下游：无。\n"
    "  返回：int。\n"
    '  """\n'
    "  a = 1\n"
    "  b = 2\n"
    "  c = 3\n"
    "  d = 4\n"
    "  e = 5\n"
    "  f = 6\n"
    "  g = 7\n"
    "  h = 8\n"
    "  i = 9\n"
    "  return a + b + c + d + e + f + g + h + i\n",
  )
  errs = cg.check_file_rules(p)
  assert any("block comment" in e for e in errs)

  text = p.read_text()
  p.write_text(
    text.replace('  """功能：测。', '  # 业务：十项累加求和\n  """功能：测。'),
    encoding="utf-8",
  )
  errs2 = cg.check_file_rules(p)
  assert not any("block comment" in e for e in errs2)


def test_full_server_gate_green() -> None:
  files = []
  for base in (ROOT / "src" / "server" / "os_core", ROOT / "src" / "server" / "api"):
    files.extend(base.rglob("*.py"))
  files = [f for f in files if "__pycache__" not in f.parts]
  errs = cg.check_files(files)
  assert errs == [], "\n".join(errs[:20])

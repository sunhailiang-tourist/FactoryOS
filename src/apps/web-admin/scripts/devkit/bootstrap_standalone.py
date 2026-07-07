#!/usr/bin/env python3
"""Standalone 模式：从 umbrella 内核 bootstrap .cursor · pipeline · gate 接缝。"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

def _kernel_sources(app_root: Path, umbrella_root: Path) -> tuple[Path | None, Path | None]:
  """解析 factoryos / rules 源：umbrella 优先，其次 devkit/kernel 快照。"""
  for root in (umbrella_root, app_root):
    factoryos = root / ".cursor" / "factoryos"
    rules = root / ".cursor" / "rules"
    if factoryos.is_dir():
      return factoryos, rules if rules.is_dir() else None
  bundle = app_root / "devkit" / "kernel"
  bf = bundle / "factoryos"
  br = bundle / "rules"
  if bf.is_dir():
    return bf, br if br.is_dir() else None
  return None, None


def bootstrap_standalone(app_root: Path, umbrella_root: Path | None = None) -> list[str]:
  """复制 AI 研发内核到 standalone app；返回已创建路径列表。"""
  app_root = app_root.resolve()
  umbrella = (umbrella_root or app_root).resolve()
  src_factoryos, src_rules = _kernel_sources(app_root, umbrella)
  created: list[str] = []

  if not src_factoryos:
    return created

  dst_factoryos = app_root / ".cursor" / "factoryos"
  if not dst_factoryos.is_dir():
    dst_factoryos.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src_factoryos, dst_factoryos, dirs_exist_ok=True)
    created.append(str(dst_factoryos.relative_to(app_root)))

  dst_rules = app_root / ".cursor" / "rules"
  if src_rules and src_rules.is_dir() and not dst_rules.is_dir():
    dst_rules.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src_rules, dst_rules, dirs_exist_ok=True)
    created.append(str(dst_rules.relative_to(app_root)))

  pipeline = app_root / "_factoryos_pipeline"
  if not pipeline.is_dir():
    pipeline.mkdir(parents=True, exist_ok=True)
    readme_src = umbrella / "_factoryos_pipeline" / "README.md"
    bundle_readme = app_root / "devkit" / "kernel" / "pipeline" / "README.md"
    if readme_src.is_file():
      shutil.copy2(readme_src, pipeline / "README.md")
    elif bundle_readme.is_file():
      shutil.copy2(bundle_readme, pipeline / "README.md")
    else:
      (pipeline / "README.md").write_text(
        "# _factoryos_pipeline\n\nStandalone DevKit 落盘目录。\n",
        encoding="utf-8",
      )
    (pipeline / "workflow_state.md").write_text(
        """# workflow_state

> Standalone DevKit · 真源见 .cursor/factoryos/ACTIVATION.md

```yaml
phase: STEP0
agent: dev
step: 0
plan:
test_plan:
updated:
goal:
```
""",
        encoding="utf-8",
      )
    created.append("_factoryos_pipeline/")

  gate_wrapper = app_root / "scripts" / "gate"
  if not gate_wrapper.is_file():
    gate_wrapper.parent.mkdir(parents=True, exist_ok=True)
    if umbrella != app_root and (umbrella / "scripts" / "gate").is_file():
      gate_wrapper.write_text(
        f"""#!/usr/bin/env bash
# Standalone → 委托 umbrella gate（迁出过渡期仍接 FactoryOS 根）
set -euo pipefail
UMBRELLA="{umbrella}"
exec "$UMBRELLA/scripts/gate" "$@"
""",
        encoding="utf-8",
      )
    else:
      gate_wrapper.write_text(
        """#!/usr/bin/env bash
# Standalone DevKit gate — profile harness + 关键词落盘接缝
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
case "${1:-}" in
  plan|test|step)
    python "$APP_ROOT/scripts/check_harness.py"
    ;;
  *)
    echo "Standalone DevKit: ./scripts/gate plan|test|step → check_harness" >&2
    echo "全量 gate pr 需 FactoryOS umbrella 或升级 devkit.kernel 快照。" >&2
    exit 1
    ;;
esac
""",
        encoding="utf-8",
      )
    gate_wrapper.chmod(0o755)
    created.append("scripts/gate")

  devkit_local = app_root / "scripts" / "devkit"
  if not (devkit_local / "frontend_contract_lib.py").is_file():
    src_devkit = umbrella / "scripts" / "devkit"
    if src_devkit.is_dir():
      shutil.copytree(src_devkit, devkit_local, dirs_exist_ok=True)
      created.append("scripts/devkit/")

  return created


def main() -> int:
  if len(sys.argv) < 2:
    print("Usage: bootstrap_standalone.py <app_root> [umbrella_root]", file=sys.stderr)
    return 1
  app = Path(sys.argv[1])
  umbrella = Path(sys.argv[2]) if len(sys.argv) > 2 else app
  created = bootstrap_standalone(app, umbrella)
  if created:
    print("Bootstrapped:", ", ".join(created))
  else:
    print("Nothing to bootstrap (kernel already present or umbrella missing)")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())

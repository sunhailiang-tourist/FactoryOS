#!/usr/bin/env python3
"""运行 DevKit App Profile harness（umbrella 调度入口）。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
  sys.path.insert(0, str(SCRIPTS))

from devkit.manifest import DevkitManifest, find_manifest_root, load_manifest


def _tier_rank(tier: str) -> int:
  order = {"contracts": 0, "boundaries": 1, "step": 2, "full": 3}
  return order.get(tier, 2)


def profiles_for_tier(manifest: DevkitManifest, harness_tier: str) -> tuple:
  """仅运行 profile.tier <= harness_tier 的项。"""
  min_rank = _tier_rank(harness_tier)
  return tuple(p for p in manifest.profiles if _tier_rank(p.tier) <= min_rank)


def run_profile(profile, repo_root: Path, python: str) -> int:
  if not profile.root.is_dir():
    print(f"SKIP profile {profile.id}: missing {profile.root}", file=sys.stderr)
    return 0
  if not profile.harness.is_file():
    print(f"FAIL profile {profile.id}: missing harness {profile.harness}", file=sys.stderr)
    return 1
  env = {
    **dict(__import__("os").environ),
    "FACTORYOS_ROOT": str(repo_root),
    "DEVKIT_PROFILE": profile.id,
    "DEVKIT_APP_ROOT": str(profile.root),
  }
  print(f"\n── DevKit profile: {profile.id} ({profile.harness.relative_to(profile.root)})")
  result = subprocess.run(
    [python, str(profile.harness)],
    cwd=profile.root,
    env=env,
  )
  return result.returncode


def run_all(
  repo_root: Path | None = None,
  *,
  harness_tier: str = "full",
  profile_ids: list[str] | None = None,
  python: str | None = None,
) -> int:
  root = repo_root or ROOT
  manifest_path = root / "devkit.manifest.yaml"
  if not manifest_path.is_file():
    print("DevKit: no devkit.manifest.yaml — skip app profiles")
    return 0
  manifest = load_manifest(root)
  py = python or sys.executable
  selected = profiles_for_tier(manifest, harness_tier)
  if profile_ids:
    wanted = set(profile_ids)
    selected = tuple(p for p in selected if p.id in wanted)
  if not selected:
    return 0
  print(f"DevKit · mode={manifest.mode} · v{manifest.version} · {len(selected)} profile(s)")
  for profile in selected:
    if run_profile(profile, root, py) != 0:
      print(f"\nDevKit FAILED at profile {profile.id}", file=sys.stderr)
      return 1
  print("\nDevKit profiles OK")
  return 0


def main(argv: list[str] | None = None) -> int:
  import argparse
  import os

  parser = argparse.ArgumentParser(description="Run DevKit app profile harness checks")
  parser.add_argument("--tier", "-t", default=os.environ.get("DEVKIT_HARNESS_TIER", "full"))
  parser.add_argument("--profile", "-p", action="append", dest="profiles")
  parser.add_argument("--root", type=Path, default=ROOT)
  args = parser.parse_args(argv)
  if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
  return run_all(args.root, harness_tier=args.tier, profile_ids=args.profiles, python=sys.executable)


if __name__ == "__main__":
  sys.exit(main())

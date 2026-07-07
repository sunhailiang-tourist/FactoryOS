#!/usr/bin/env bash
# web-admin 一键工程自检：DevKit activate 等价（pnpm + profile harness）
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/../src/apps/web-admin" && pwd)"
exec "$APP_ROOT/scripts/activate.sh"

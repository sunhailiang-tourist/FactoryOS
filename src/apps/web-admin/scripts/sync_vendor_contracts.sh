#!/usr/bin/env bash
# umbrella 内：将 contracts/ 同步到 vendor/factoryos-contracts 镜像
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UMBRELLA="$(cd "$APP_ROOT/../../.." && pwd)"
VENDOR="$APP_ROOT/vendor/factoryos-contracts"

mkdir -p "$VENDOR/openapi"
cp "$UMBRELLA/contracts/openapi/工厂操作系统-v1.1.yaml" "$VENDOR/openapi/"
cp -R "$UMBRELLA/contracts/schemas" "$VENDOR/"
cp "$UMBRELLA/contracts/error-registry.yaml" "$VENDOR/"
echo "OK: synced vendor/factoryos-contracts from $UMBRELLA/contracts"

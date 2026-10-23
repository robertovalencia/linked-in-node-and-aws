#!/usr/bin/env bash
# Uses the operator's temporary AWS profile; does not provision infrastructure.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
exec node "$root/scripts/aws-release-local.mjs" "$@"

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash scripts/setup-local.sh
case "${1:-up}" in
  up) docker compose up -d --build --wait --wait-timeout 240; echo 'Marketplace: http://localhost:8180' ;;
  deps) docker compose up -d --wait postgres kafka ;;
  down) docker compose down ;;
  logs) docker compose logs --tail=150 -f "${@:2}" ;;
  status) docker compose ps ;;
  reset)
    [ "${2:-}" = '--confirm-local-data-loss' ] || { echo 'Reset deletes only this project local data. Pass --confirm-local-data-loss.'; exit 2; }
    docker compose down --volumes
    ;;
  *) echo 'Usage: scripts/local.sh up|deps|down|logs [service]|status|reset --confirm-local-data-loss'; exit 2 ;;
esac

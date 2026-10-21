#!/usr/bin/env bash
# Runs on the SSM-managed host as root; no secrets in command arguments or logs.
set -euo pipefail
umask 077
release_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$release_dir"
exec 9>/opt/marketplace/deploy.lock
flock -n 9 || { echo 'Another deployment is running'; exit 1; }
secret_arn=$(jq -er .secret_arn manifest.json)
region=$(jq -er .region manifest.json)
registry=$(jq -er .backend manifest.json | cut -d/ -f1)
trap 'rm -f "$release_dir/secret.json"' EXIT
aws secretsmanager get-secret-value --region "$region" --secret-id "$secret_arn" --query SecretString --output text >secret.json
python3 - <<'PY'
import json,re
from pathlib import Path
s=json.loads(Path('secret.json').read_text()); m=json.loads(Path('manifest.json').read_text())
keys=['POSTGRES_PASSWORD','IDENTITY_DB_PASSWORD','CATALOG_DB_PASSWORD','INQUIRIES_DB_PASSWORD','NOTIFICATIONS_DB_PASSWORD','JWT_SECRET','INTERNAL_API_KEY']
for k in keys:
    if not re.fullmatch(r'[a-f0-9]{64,}',s.get(k,'')): raise SystemExit(f'{k} must contain at least 64 lowercase hex characters')
for k in ['backend','frontend']:
    if not re.fullmatch(r'[0-9]+\.dkr\.ecr\.[a-z0-9-]+\.amazonaws\.com/[a-z0-9/-]+@sha256:[a-f0-9]{64}',m[k]): raise SystemExit('Require ECR sha256 images')
Path('.env').write_text(''.join(f'{k}={s[k]}\n' for k in keys)+f'BACKEND_IMAGE={m["backend"]}\nFRONTEND_IMAGE={m["frontend"]}\n')
PY
aws ecr get-login-password --region "$region" | docker login --username AWS --password-stdin "$registry"
previous=$(readlink -f /opt/marketplace/current || true)
marketplace-compose -f compose.yaml pull
healthy=false
if marketplace-compose -f compose.yaml up -d --wait --wait-timeout 180; then
for attempt in $(seq 1 60); do
  if bash ./aws-smoke.sh; then healthy=true; break; fi
  sleep 3
done
fi
if [[ "$healthy" == true ]]; then
  backend_image=$(jq -er .backend manifest.json)
  if ! docker run --rm --network host -v "$release_dir:/release:ro" --entrypoint node "$backend_image" /release/acceptance.mjs http://127.0.0.1:80; then healthy=false; fi
fi
if [[ "$healthy" != true ]]; then
  echo 'Health verification failed; restoring previous application images.'
  if [[ -n "$previous" && -f "$previous/compose.yaml" ]]; then
    cd "$previous"
    marketplace-compose -f compose.yaml up -d --wait --wait-timeout 180
    bash ./aws-smoke.sh
  fi
  exit 1
fi
ln -sfn "$release_dir" /opt/marketplace/current
printf 'Release verified: %s\n' "$(jq -r .source_sha manifest.json)"

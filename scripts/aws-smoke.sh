#!/usr/bin/env bash
set -euo pipefail
base="${AWS_DEV_BASE_URL:-http://127.0.0.1:80}"
curl --fail --silent --show-error --max-time 5 "$base/health" >/dev/null
for service in identity catalog inquiries notifications; do
  marketplace-compose -f compose.yaml exec -T "$service" node -e 'fetch(`http://localhost:${process.env.PORT}/health/ready`).then(async r=>{if(!r.ok)process.exit(1);console.log(await r.text())}).catch(()=>process.exit(1))'
done

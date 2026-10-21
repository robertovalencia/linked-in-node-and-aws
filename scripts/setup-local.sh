#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [ -e .env ]; then
  echo 'Keeping existing .env and database credentials.'
  exit 0
fi
umask 077
node --input-type=module <<'JS'
import { randomBytes } from 'node:crypto';
import { writeFileSync } from 'node:fs';
const keys=['POSTGRES_PASSWORD','IDENTITY_DB_PASSWORD','CATALOG_DB_PASSWORD','INQUIRIES_DB_PASSWORD','NOTIFICATIONS_DB_PASSWORD','SONAR_DB_PASSWORD','JWT_SECRET','INTERNAL_API_KEY'];
writeFileSync('.env',keys.map(k=>`${k}=${randomBytes(32).toString('hex')}`).join('\n')+'\n',{flag:'wx',mode:0o600});
console.log('Created independent local credentials in .env (mode 0600).');
JS

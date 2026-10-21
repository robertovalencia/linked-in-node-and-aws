#!/usr/bin/env bash
set -euo pipefail
for service in identity catalog inquiries notifications; do
  key="${service^^}_DB_PASSWORD"
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres -v role="$service" -v password="${!key}" <<'SQL'
CREATE ROLE :"role" LOGIN PASSWORD :'password';
CREATE DATABASE :"role" OWNER :"role";
REVOKE CONNECT ON DATABASE :"role" FROM PUBLIC;
SQL
done

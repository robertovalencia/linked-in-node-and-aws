#!/bin/sh
# Reject configuration injection before the standard nginx envsubst entrypoint.
set -eu
for hostname in "$IDENTITY_UPSTREAM" "$CATALOG_UPSTREAM" "$INQUIRIES_UPSTREAM" "$NOTIFICATIONS_UPSTREAM"; do
  case "$hostname" in
    ''|*[!a-zA-Z0-9.-]*|.*|-*) echo 'Invalid API upstream hostname' >&2; exit 1 ;;
  esac
  [ "${#hostname}" -le 253 ] || { echo 'API upstream hostname too long' >&2; exit 1; }
done
case "$DNS_RESOLVER" in
  ''|*[!0-9.]*) echo 'DNS_RESOLVER must be an IPv4 address' >&2; exit 1 ;;
esac
printf '%s\n' "$DNS_RESOLVER" | awk -F. '
  NF != 4 { exit 1 }
  { for (i=1; i<=4; i++) if ($i == "" || $i + 0 > 255) exit 1 }
' || { echo 'Invalid IPv4 DNS resolver' >&2; exit 1; }

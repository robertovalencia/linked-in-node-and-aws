#!/bin/bash
set -euo pipefail
dnf install -y docker jq python3 awscli-2
systemctl enable --now docker amazon-ssm-agent
install -d -m 0700 /opt/marketplace/releases
# Compose is vendored in release bundles from the validated CLI container in CI.
# The host uses that pinned container against its Docker socket, avoiding curl|sh.
cat >/usr/local/bin/marketplace-compose <<'COMPOSE'
#!/bin/bash
set -euo pipefail
exec docker run --rm --network host -v /var/run/docker.sock:/var/run/docker.sock -v /root/.docker:/root/.docker:ro -v /opt/marketplace:/opt/marketplace -w "$PWD" docker:27.5.1-cli@sha256:851f91d241214e7c6db86513b270d58776379aacc5eb9c4a87e5b47115e3065c compose "$@"
COMPOSE
chmod 0755 /usr/local/bin/marketplace-compose

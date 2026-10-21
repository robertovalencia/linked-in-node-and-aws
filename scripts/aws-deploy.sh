#!/usr/bin/env bash
# Publishes a release bundle and invokes SSM. Infrastructure must already exist.
set -euo pipefail
: "${AWS_REGION:?}" "${AWS_INSTANCE_ID:?}" "${AWS_RELEASE_BUCKET:?}" "${AWS_SECRET_ARN:?}" "${BACKEND_IMAGE:?}" "${FRONTEND_IMAGE:?}" "${GITHUB_SHA:?}"
[[ "$GITHUB_SHA" =~ ^[a-f0-9]{40}$ ]] || exit 2
root="$(cd "$(dirname "$0")/.." && pwd)"
bundle=$(mktemp -d)
trap 'rm -rf "$bundle"' EXIT
cp "$root/infra/aws-dev/compose.yaml" "$bundle/"
cp "$root/infra/postgres/init-databases.sh" "$bundle/"
cp "$root/scripts/aws-remote-deploy.sh" "$root/scripts/aws-smoke.sh" "$root/scripts/acceptance.mjs" "$bundle/"
export bundle
python3 - <<'PY'
import json,os
from pathlib import Path
m={k:os.environ[v] for k,v in {'source_sha':'GITHUB_SHA','backend':'BACKEND_IMAGE','frontend':'FRONTEND_IMAGE','secret_arn':'AWS_SECRET_ARN','region':'AWS_REGION'}.items()}
Path(os.environ['bundle'],'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
PY
mkdir -p "$root/work"
cp "$bundle/manifest.json" "$root/work/release-manifest.json"
tar -czf "$bundle/release.tgz" -C "$bundle" compose.yaml init-databases.sh aws-remote-deploy.sh aws-smoke.sh acceptance.mjs manifest.json
aws s3 cp "$bundle/release.tgz" "s3://$AWS_RELEASE_BUCKET/releases/$GITHUB_SHA.tgz" --only-show-errors
# Restrict interpolated command values to prevent remote shell interpretation.
[[ "$AWS_RELEASE_BUCKET" =~ ^[a-z0-9.-]+$ && "$AWS_REGION" =~ ^[a-z0-9-]+$ ]] || exit 2
python3 - <<'PY' >"$bundle/parameters.json"
import os,json
sha=os.environ['GITHUB_SHA']; bucket=os.environ['AWS_RELEASE_BUCKET']; region=os.environ['AWS_REGION']
command=f'set -eu; mkdir -p /opt/marketplace/releases/{sha}; cd /opt/marketplace/releases/{sha}; aws s3 cp s3://{bucket}/releases/{sha}.tgz release.tgz --region {region} --only-show-errors; tar -xzf release.tgz; bash ./aws-remote-deploy.sh'
print(json.dumps({'commands':[command],'executionTimeout':['900']}))
PY
command_id=$(aws ssm send-command --region "$AWS_REGION" --instance-ids "$AWS_INSTANCE_ID" --document-name AWS-RunShellScript --parameters "file://$bundle/parameters.json" --query Command.CommandId --output text)
for attempt in $(seq 1 100); do
  status=$(aws ssm get-command-invocation --region "$AWS_REGION" --command-id "$command_id" --instance-id "$AWS_INSTANCE_ID" --query Status --output text 2>/dev/null || true)
  case "$status" in
    Success) aws ssm get-command-invocation --region "$AWS_REGION" --command-id "$command_id" --instance-id "$AWS_INSTANCE_ID" --query StandardOutputContent --output text; exit 0;;
    Failed|Cancelled|TimedOut) aws ssm get-command-invocation --region "$AWS_REGION" --command-id "$command_id" --instance-id "$AWS_INSTANCE_ID"; exit 1;;
  esac
  sleep 10
done
echo "SSM command $command_id did not finish within bounded deployment timeout" >&2
exit 1

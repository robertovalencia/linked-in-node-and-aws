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
rm -f "$root/work/aws-acceptance.json" "$root/work/aws-ssm-invocation.json" "$root/work/aws-ssm-command.json"
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
aws ssm send-command --region "$AWS_REGION" --instance-ids "$AWS_INSTANCE_ID" --document-name AWS-RunShellScript --parameters "file://$bundle/parameters.json" --output json >"$root/work/aws-ssm-command.json"
command_id=$(python3 - "$root/work/aws-ssm-command.json" <<'PYTHON'
import json,sys
print(json.load(open(sys.argv[1]))['Command']['CommandId'])
PYTHON
)
for attempt in $(seq 1 100); do
  if ! aws ssm get-command-invocation --region "$AWS_REGION" --command-id "$command_id" --instance-id "$AWS_INSTANCE_ID" --output json >"$bundle/invocation.json" 2>/dev/null; then sleep 10; continue; fi
  cp "$bundle/invocation.json" "$root/work/aws-ssm-invocation.json"
  status=$(python3 - "$bundle/invocation.json" <<'PYTHON'
import json,sys
print(json.load(open(sys.argv[1]))['Status'])
PYTHON
)
  case "$status" in
    Success|Failed|Cancelled|TimedOut|Cancelling)
      python3 - "$root/work/aws-ssm-invocation.json" "$root/work/aws-acceptance.json" "$command_id" <<'PYTHON'
import base64,gzip,json,os,sys
from pathlib import Path
invocation=json.loads(Path(sys.argv[1]).read_text())
if invocation.get('CommandId') != sys.argv[3] or invocation.get('InstanceId') != os.environ['AWS_INSTANCE_ID']: raise SystemExit('SSM evidence identity does not match deployment command and instance')
successful=invocation.get('Status')=='Success'
if successful and invocation.get('ResponseCode') != 0: raise SystemExit('SSM reported Success with nonzero response code')
markers=[line.removeprefix('MARKETPLACE_ACCEPTANCE_GZIP_BASE64=') for line in invocation.get('StandardOutputContent','').splitlines() if line.startswith('MARKETPLACE_ACCEPTANCE_GZIP_BASE64=')]
if not markers and not successful: sys.exit(0)
if len(markers)!=1: raise SystemExit('Require one complete acceptance evidence marker in exact SSM response')
report=json.loads(gzip.decompress(base64.b64decode(markers[0],validate=True)))
Path(sys.argv[2]).write_text(json.dumps({**report,'sourceSha':os.environ['GITHUB_SHA'],'ssmCommandId':invocation['CommandId'],'ssmInstanceId':invocation['InstanceId'],'ssmStatus':invocation['Status']},indent=2)+'\n')
if successful and (report.get('expected')!=48 or report.get('passed')!=48 or report.get('failed')!=0 or len(report.get('results',[]))!=48 or any(row.get('status')!='PASS' for row in report['results'])):
    raise SystemExit('AWS acceptance evidence must contain exactly 48 PASS results and zero failures')
if successful: print(f"AWS acceptance verified: 48 passed, command {invocation['CommandId']}")
PYTHON
      if [[ "$status" == Success ]]; then exit 0; fi
      cat "$root/work/aws-ssm-invocation.json"
      exit 1;;
  esac
  sleep 10
done
echo "SSM command $command_id did not finish within bounded deployment timeout" >&2
exit 1

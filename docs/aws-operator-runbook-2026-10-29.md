# Visible AWS commands and 24-hour cleanup — 29 October 2026

> Current checkpoint, October30: infrastructure complete,112 managed resources/serial8, approved deadline9:51PM EDT. No automatic cleanup exists. [Current readiness audit](aws-automatic-shutdown-readiness-2026-10-30.md) and [exact cleanup-transition packet](aws-cleanup-transition-review-2026-10-30.md). Original deadlines and initial plans below are historical.
**Historical initial failure, superseded by successful micro completion.** [Actual execution and independent critic](evidence/aws-infrastructure-apply-2026-10-29/README.md) · [current repair/cost/deadline review](aws-repair-review-2026-10-30.md).

Deadline: **today 5:51:25 PM EDT**, operator return **3:51 PM EDT**. No automatic cleanup exists. The initial `2fd776…` artifact is consumed and must never be retried. The initial create-only helper below correctly refuses an existing application state; its commands are historical preparation examples, not repair commands. Current repair plans must bind the actual 100-instance partial state. Preserve certificate/bootstrap state. Do not reset the deadline or run an old plan.

## Viewing commands in iTerm

Computer Use explicitly denied iTerm access. No AppleScript, shell-driven UI or other route is used to bypass that denial. These commands are intended for you to paste into iTerm manually. The helper prints each command and purpose before execution, writes a mode 0600 transcript and structured steps inside a mode 0700 ignored work directory, and never offers apply, destroy or login subcommands.

Start with this credential-free command:

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
python3 scripts/aws-ecs-operator.py --help
```

After the public-IP lookup is authorized, run a fresh preflight in an unused directory:

```bash
python3 scripts/aws-ecs-operator.py preflight \
  --run-directory work/aws-operator-preparation-2026-10-29/manual-preflight \
  --https-context work/aws-operator-preparation-2026-10-29/https-context.json \
  --s3-backend-context work/aws-operator-preparation-2026-10-29/s3-backend-context.json
```

This command performs the checks in the table below and calls AWS checkip to compare CLI egress privately with the approved /32. It does not silently change ingress, fetch secrets, log in or create resources. A supplied browser CIDR must be explicitly approved; CLI and browser egress can differ with VPN/proxy routing. An additional IP lookup/private recording was rejected by automatic approval review for sensitive connection metadata. It was not retried before the human explicitly authorized a new lookup. The subsequent authorized lookup and successful run are linked above.

Historical first attempt (before the new explicit IP approval):

| Step actually attempted | Purpose / actual result |
|---|---|
|Clean the child-process environment|Pinned marketplace-dev/us-east-2; removed static/role/container/config-path/Terraform overrides and optimization flags; no environment dump|
|`aws sts get-caller-identity`|Same effective credentials as Terraform; account 772641336063 passed|
|`aws freetier get-account-plan-state --region us-east-1`|Free/ACTIVE with $100 USD credits; not a cap or service-create guarantee|
|`terraform workspace show` and backend validation|Default workspace; exact encrypted/locked/account-bound S3 bucket/key passed|
|Application-state `head-object`|404: no prior application state; expected absence, not a failed deployment|
|`aws acm describe-certificate`|Exact hostname/certificate ISSUED and nonexportable|
|Named ECS/RDS/ALB and project-VPC reads|No proposed application resources in these scopes; default VPC not touched|
|AWS checkip comparison|Address suppressed; mismatch caused STOP|
|`terraform plan`|Not reached; no fresh artifact or review-success claim|

Do not use `set -x`, credential-export commands, secret-value reads or database password commands in a transcript. Keep raw plans/state, TLS keys and generated payloads out of Git. The helper does not overwrite an existing run directory: use a new name for a new attempt so failures remain evidence.

## Historical initial-plan commands — not valid for repair

The following is a prepared command, **a replay command; the actual successful run is documented above**. For any future replay, refresh the private contexts/inputs and proposed time window first:

```bash
python3 scripts/aws-ecs-operator.py plan \
  --run-directory work/aws-operator-preparation-2026-10-29/operator-run-approved-client \
  --inputs work/aws-operator-preparation-2026-10-29/inputs.tfvars.json \
  --https-context work/aws-operator-preparation-2026-10-29/https-context.json \
  --s3-backend-context work/aws-operator-preparation-2026-10-29/s3-backend-context.json \
  --rates-file work/aws-operator-preparation-2026-10-29/rates.json
```

It requires a fresh live preflight, rejects initial activation/discard flags and existing state/topology, copies private inputs, creates the S3-backed saved plan, derives its actual JSON, and runs the strict binary/source/backend/security/cost reviewer. Normal planning creates/deletes an S3 lock object. No application apply occurs. Outputs include `application.tfplan`, `plan.json`, `review.json`, `transcript.txt` and `steps.json` in the new run directory.

The older `8cf376...` artifact was superseded before provisioning. The subsequently approved `2fd776...` artifact was executed once and failed partially; it is consumed. Its historical inputs used an ExpiresAt tag of 22:00 UTC. The actual first paid create started at **29 October 21:51:25.219221 UTC**, fixing the shutdown deadline at **30 October 21:51:25.219221 UTC / 5:51:25 PM EDT**. The new repair input rounds the deadline tag down to 21:51:25 UTC. Tags are metadata, never timers. Use the [current exact repair review](aws-repair-review-2026-10-30.md); do not run this initial create-only workflow against existing partial state.

## Selected shutdown mechanism and cost comparison

| Method | What must be prepared | Added gross modeled controller cost | Remaining condition |
|---|---|---:|---|
|Operator-assisted|Named operator; human return before deadline; fresh login; reviewed cleanup-transition and destroy plans; final inventory|$0 additional controller service|Selected by the human. They must return; laptop/network/authentication must be available. Not unattended enforcement.|
|AWS-native proposal|Separate Scheduler→on-demand CodeBuild project/service roles/source bundle; bounded retries/failure handling; exact state/resource scope; independent rehearsal and separate Terraform plan|About $0.20 one 30-minute cleanup; $0.33 rehearsal+cleanup; $1.40 higher three 60-minute attempts|Not selected or implemented. Do not add these services. Any later change would require its own design/cost/plan review.|

Official Ohio CodeBuild Linux `general1.small` on-demand compute is $0.005/minute, rounded up per build. Scheduler gross pricing beyond shared allowance is $1/million invocations. Logs/S3 allowances are included in the comparison; no shared free allowance/credit is deducted. [Official CodeBuild pricing](https://aws.amazon.com/codebuild/pricing/), [Scheduler pricing](https://aws.amazon.com/eventbridge/pricing/), [selected regional SKU and exact Decimal calculations](evidence/aws-operator-preparation-2026-10-29/shutdown-cost-comparison.json). No reserved capacity, dedicated NAT or extra database is assumed for this controller. Repeated failures and extra runtime can exceed the model.

AWS login auto-refreshes for up to 12 hours, which cannot cover a 24-hour unattended teardown. [Official CLI documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html). A Codex reminder is a notification, not deletion infrastructure. Scheduler successfully invoking CodeBuild would prove dispatch only; final cleanup success requires actual absent-resource/retained-state checks. The proposed native controller needs bounded build-level retries and an explicitly approved failure destination; scheduler API retries alone do not handle a failed build. Service eligibility/IAM/SCP permissions remain unproved, and no account upgrade or restriction bypass is authorized.

The human chose 24 hours from the first billable application resource. Its conservative actual start and deadline are now recorded above and in the execution journal; neither a repair nor new tags reset them. Confirm operator availability for the remaining window before any further approved apply. Plan for human return around hour22 to renew login, stop writes and review cleanup, then begin destruction with time to verify completion before hour24. An ExpiresAt tag never deletes resources. Begin stopping traffic and preparing teardown ahead of the deadline; AWS deletion is asynchronous, so initiating it at hour 24 does not mean every charge/data copy disappears at that instant. Keep exact start/deadline, owner, retries and actual completion times in a private run record.

## Concrete cleanup sequence for the selected discard policy

The new Terraform flag `teardown_discard_demo_data` defaults false. Ordinary plans keep existing RDS protection/final-snapshot/automated-backup behavior, protected operations objects and seven-day runtime-secret recovery. Existing ECR `force_delete=true` is unchanged. Setting the flag is an explicit teardown transition; it must never be used to weaken the ordinary initial-plan gate.

1. Freeze new writes and stop application tasks; preserve sanitized operational evidence privately. Before database deletion, require actual RUNNING and PENDING task lists to be empty for the exact project cluster, including standalone migration/bootstrap tasks; desired_count=0 alone is insufficient. Record task ARNs and stop only this project's remaining tasks under the reviewed cleanup scope. Keep any generated demo-secret payload paths in the run record. Confirm expected account, backend, certificate/state boundaries and a real human/controller approval for the cleanup scope.
2. Inventory project-specific manual/recovery snapshots, retained automated backups, secrets, operation-bucket versions, ECR images and logs. Old manual snapshots are not removed by changing RDS deletion flags. Never delete account-wide snapshots or unrelated buckets.
3. Create a private cleanup input file from the actual current deployment inputs. Set `deploy_application=false`, `teardown_discard_demo_data=true` and `seed_demo=false`; retain the actual image digests where needed to scale registered services to zero. Do not put passwords in Terraform.
4. Prepare a **saved cleanup-transition plan**, inspect every action and reject unexpected creates/replacements/unrelated changes. Expected transitions: RDS protection off, skip final snapshot, delete automated backups; operations bucket force_destroy; six runtime secrets recovery 0; active service desired counts to 0 when present. RDS manages its own master secret separately. A fresh critic and exact approval precede applying this transition.
5. Apply that exact transition and verify actual state/configuration. Require actual RUNNING and PENDING task lists to be empty for the project cluster, including standalone/bootstrap tasks, before preparing destroy; an ECS desired count of zero is not proof that tasks stopped. Provider documentation explicitly says enabling operations `force_destroy` only in the same destroy operation is insufficient: the transition must have been successfully applied first. A failed transition is not permission to force deletion through another channel.
6. Prepare a separate **saved destroy plan** against the actual ECS state, review the exact resources, and apply only the approved destroy artifact. It removes application ALB/NAT/EIP/EC2/EBS/ECS/RDS/ECR/logs/secrets/operations resources. It does not target the separate bootstrap/certificate roots.
7. Verify actual resource absence, including lingering task ENIs/NAT EIPs, snapshots/backups and pending secret deletion. Verify RDS-managed master-secret outcome; forced secret deletion is asynchronous and does not promise a particular deletion time. Delete only separately reviewed project-demo snapshots/backups that existed before destroy.
8. Remove only the recorded local demo-secret payload directory after required evidence; preserve bootstrap/certificate/application Terraform state. Inventory retained S3 state versions and certificate explicitly, and check delayed billing/credits. Do not claim zero residual cost or proof of physical media erasure.

The following **future preparation-only template** creates a private cleanup-transition plan. It does not apply or destroy. It is not executed evidence and cannot produce a meaningful transition while application state is absent. Replace the current-input path only after a real deployment exists. The actual apply/destroy commands will be generated with exact approved hashes, source/backend/account checks and fresh review from real state; there is no speculative apply command here to run prematurely.

```bash
bash <<'BASH'
set -euo pipefail
umask 077
DEMO_ROOT=/Users/robertovalencia/Documents/Business/linked-in-node-and-aws
cd "$DEMO_ROOT"
[[ -d .git && -f infra/aws-ecs-dev/versions.tf ]] || exit 1
unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN AWS_SECURITY_TOKEN
unset AWS_ROLE_ARN AWS_WEB_IDENTITY_TOKEN_FILE AWS_ROLE_SESSION_NAME
unset AWS_CONTAINER_CREDENTIALS_FULL_URI AWS_CONTAINER_CREDENTIALS_RELATIVE_URI
unset AWS_CONTAINER_AUTHORIZATION_TOKEN AWS_CONTAINER_AUTHORIZATION_TOKEN_FILE
unset AWS_CONFIG_FILE AWS_SHARED_CREDENTIALS_FILE AWS_DEFAULT_PROFILE
unset TF_WORKSPACE TF_DATA_DIR TF_CLI_CONFIG_FILE TF_LOG TF_LOG_PATH PYTHONOPTIMIZE
while IFS= read -r name; do
  case "$name" in AWS_ENDPOINT_URL*|TF_VAR_*|TF_CLI_ARGS*) unset "$name";; esac
done < <(env | cut -d= -f1)
export AWS_PROFILE=marketplace-dev AWS_REGION=us-east-2 AWS_DEFAULT_REGION=us-east-2
[[ "$(aws sts get-caller-identity --query Account --output text)" == 772641336063 ]] || exit 1
[[ "$(terraform -chdir=infra/aws-ecs-dev workspace show)" == default ]] || exit 1
# Verify the initialized real backend without printing its full configuration.
python3 - <<'PYBACKEND'
import json
from pathlib import Path
p=Path('infra/aws-ecs-dev/.terraform/terraform.tfstate')
b=json.loads(p.read_text())['backend']; c=b['config']
expected={'bucket':'772641336063-linked-in-node-terraform-state',
          'key':'linked-in-node/ecs-dev/terraform.tfstate','region':'us-east-2',
          'encrypt':True,'use_lockfile':True,'allowed_account_ids':['772641336063']}
if b['type']!='s3' or any(c.get(k)!=v for k,v in expected.items()):
    raise SystemExit('STOP: wrong backend')
PYBACKEND
DEMO_CURRENT_INPUTS=/ABSOLUTE/PRIVATE/ACTUAL_CURRENT_INPUTS.tfvars.json
[[ -f "$DEMO_CURRENT_INPUTS" ]] || exit 1
# A new directory prevents overwriting any prior plan or failed evidence.
DEMO_CLEANUP_DIR=$(mktemp -d "$DEMO_ROOT/work/aws-operator-preparation-2026-10-29/cleanup.XXXXXX")
export DEMO_CURRENT_INPUTS DEMO_CLEANUP_DIR
python3 - <<'PYINPUTS'
import json,os,stat
from pathlib import Path
p=Path(os.environ['DEMO_CURRENT_INPUTS']); d=Path(os.environ['DEMO_CLEANUP_DIR'])
for f in (p,d):
    s=f.stat()
    if s.st_uid!=os.getuid() or stat.S_IMODE(s.st_mode)&0o077:
        raise SystemExit('STOP: input/artifact permissions must be owner-only')
v=json.loads(p.read_text())
v.update(deploy_application=False,teardown_discard_demo_data=True,seed_demo=False)
(d/'cleanup.tfvars.json').write_text(json.dumps(v,indent=2)+'\n')
PYINPUTS
terraform -chdir=infra/aws-ecs-dev plan -input=false -lock-timeout=60s \
  -var-file="$DEMO_CLEANUP_DIR/cleanup.tfvars.json" \
  -out="$DEMO_CLEANUP_DIR/cleanup-transition.tfplan"
terraform -chdir=infra/aws-ecs-dev show -no-color "$DEMO_CLEANUP_DIR/cleanup-transition.tfplan"
shasum -a 256 "$DEMO_CLEANUP_DIR/cleanup-transition.tfplan"
printf 'STOP for independent exact-plan review and approval. Private artifacts: %s\n' "$DEMO_CLEANUP_DIR"
BASH
```

After a separately approved transition actually succeeds, verify stopped tasks and database/deletion settings before preparing a fresh saved destroy plan. Never proceed to destroy after a failed transition. Before each eventual apply, recheck the exact approved artifact hash and embedded source/provider lock, current account/backend/default workspace and owner-only artifacts. A hash or account printout alone is not a guard. The initial create-only reviewer intentionally refuses cleanup transitions; those require a distinct destructive-scope review. Application resources now exist partially; cleanup artifacts must bind their actual current state.

Never run `terraform destroy -auto-approve`, delete raw state, apply the bootstrap plan again or use the old EC2/SSM deployment workflow as this ECS release. A saved destroy plan must be generated from real current partial state after any required cleanup transition has actually succeeded. Source/mock tests do not establish a verified cloud teardown.

## Costs and evidence boundary

The last fresh 31-rate Ohio review retains expected $6.83/24 hours for zero-task infrastructure probes and $8.32/24 hours for future five-task activation, before credits/recovery/controller costs. Corresponding 720-hour comparisons are $191.22/$235.68. Those are dated usage models, not spending caps or measured cloud consumption. Actual fresh saved-plan preparation succeeded separately as documented above. A new application plan and any chosen native controller require current quantity/cost review before apply.

With the selected discard policy, no final demo snapshot or retained automated backup is intended after successful teardown. Initial backup/recovery protection remains during the demo. Existing manual/recovery snapshots need explicit deletion, and retained/state/cleanup timing must be verified. Secrets scheduled for ordinary deletion are not charged during their recovery window; recovery 0 implements the chosen discard policy rather than a proven fee saving. The protected state allocation remains approximately $0.000972/24 h or$0.029165/720 h under the existing 1 GB/version/request assumptions; actual versions/requests can grow. The preserved nonexportable ACM certificate has no additional ACM fee. [Actual bootstrap state evidence](evidence/aws-state-bootstrap-2026-10-29/README.md).

[Preparation evidence and independent critic](evidence/aws-operator-preparation-2026-10-29/README.md) distinguish 12 mocked Terraform tests, 28 fake-CLI tests and the actual fail-closed preflight. No AWS application health/security/recovery/rollback/48-check success, unattended shutdown or provisioning approval is inferred. The actual fresh saved plan has separate execution evidence linked above.

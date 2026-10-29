# 10 · The project's AWS Terraform command workflow

[Previous: runnable local commands](09-terraform-local-commands.md) · [Walkthrough index](README.md) · [Terraform concepts](04-terraform-setup-and-plans.md)

This is an **operator command reference**, not a run-every-block deployment script. The local chapter is runnable now; these AWS commands require the deployment owner's actual working directories, private inputs, state/backend and approved saved artifact. “Create Node.js AWS LinkedIn project” owns current costs, plans and cloud execution. Adding commands to study material does not authorize their execution.

**29 October execution update:** the state bootstrap has now been approved/applied (5 creates, 0 updates/deletes), its controls verified, and the real S3-backed application plan reviewed. The [execution journal](11-aws-execution-journal.md) is the current step-by-step record. The bootstrap commands below remain operator references, not instructions to recreate the already-managed bucket. Application apply and shutdown mechanism remain pending.

The historical recorded status on 28 October 2026 is: one certificate issued; state-bootstrap and application plans unapplied; no live HTTPS marketplace. Read the [dated plan review](https://github.com/robertovalencia/linked-in-node-and-aws/blob/01c30fc0ca3958a99f6808f2211153f2d602c7c4/docs/aws-https-plan-review-2026-10-28.md) before using a historical example. New source, inputs, state or topology need a new plan/review. The selected client range remains private.

## Step 1. Check tools and the source revision

Run from the repository root. These commands inspect local tools/source, not AWS resources:

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
terraform version
aws --version
git status --short
git rev-parse HEAD
terraform fmt -check -recursive infra/bootstrap infra/aws-ecs-certificate infra/aws-ecs-dev
```

Expected: supported installed tools, known source revision, no unexpected worktree changes and no formatting differences in the selected roots. Terraform constraints are `>=1.10,<2.0`; AWS provider selection also depends on the root's committed lock file. Do not run `init -upgrade` casually during a reviewed deployment: provider changes are a separate review.

## Step 2. Verify the operator identity

Stay in the same terminal so the selected AWS environment and owner-provided paths remain available. These are **read-only AWS calls**, after an authorized temporary login already exists:

```bash
export AWS_PROFILE=marketplace-dev
export AWS_REGION=us-east-2
export AWS_DEFAULT_REGION=us-east-2
aws sts get-caller-identity
```

Expected account: `772641336063`. Inspect the actual ARN as well; a profile name is not proof of the identity inside it. Use the same effective credential environment for CLI and Terraform. A study viewer's `ViewOnlyAccess`/ACM read permissions are not a deployment operator role. If login expired or permissions are insufficient, return to the owner’s authentication/permission workflow; do not create a permanent key or grant unrestricted access just to unblock a command.

The browser uses Google-backed AWS Builder ID. Browser login and a currently usable CLI session are separate observations. MFA registration does not prove an existing CLI credential has refreshed.

## Step 3. Choose the root and preserve its state

| Root in source | Purpose | State/operation boundary |
|---|---|---|
| `infra/bootstrap` | Protected state bucket; optional OIDC definitions | Bucket-only plan actually applied with 5 creates and no OIDC on 29 October; preserve its existing local state |
| `infra/aws-ecs-certificate` | Certificate request | Already applied in a preserved private local working directory; do not initialize a fresh empty copy and request a duplicate |
| `infra/aws-ecs-dev` | Prepared ECS/RDS/network/broker resources | Actual S3 backend now initialized at the distinct ECS key; application apply pending; old local preview must not be applied |
| `infra/aws-dev` | Preserved legacy EC2/SSM environment | Different architecture/state key; not an ECS shortcut |

The root source is not automatically the operator's initialized working copy. The deployment owner must identify the correct root, existing state and run directory. Cloud commands below deliberately require those variables instead of guessing a new state location.

## Step 4. Prepare a fresh bootstrap plan—not an apply

**Owner-operated template.** Set these to the actual reviewed paths provided by the deployment owner before running. The bootstrap input file must explicitly select Ohio (`region="us-east-2"`), the approved private state-bucket name and `create_github_oidc=false`; the source default Region is different.

```bash
(
  set -eu
  : "${AWS_PROFILE:?Select the owner-approved AWS profile first}"
  : "${OWNER_BOOTSTRAP_ROOT:?Set the reviewed bootstrap working directory}"
  : "${OWNER_BOOTSTRAP_INPUTS:?Set the absolute private bootstrap tfvars path}"
  : "${OWNER_RUN_DIR:?Set the existing private run directory for this review}"
  umask 077
  test -d "$OWNER_BOOTSTRAP_ROOT"
  test -f "$OWNER_BOOTSTRAP_INPUTS"
  test -d "$OWNER_RUN_DIR"
  chmod 700 "$OWNER_RUN_DIR"
  test ! -e "$OWNER_RUN_DIR/bootstrap.tfplan"
  terraform -chdir="$OWNER_BOOTSTRAP_ROOT" init -input=false
  terraform -chdir="$OWNER_BOOTSTRAP_ROOT" validate
  terraform -chdir="$OWNER_BOOTSTRAP_ROOT" plan -input=false \
    -var-file="$OWNER_BOOTSTRAP_INPUTS" -out="$OWNER_RUN_DIR/bootstrap.tfplan"
  terraform -chdir="$OWNER_BOOTSTRAP_ROOT" show -no-color "$OWNER_RUN_DIR/bootstrap.tfplan"
  shasum -a 256 "$OWNER_RUN_DIR/bootstrap.tfplan"
)
```

`OWNER_*` variables are operator-provided absolute paths, not literal strings to paste. The directory is owner-only/private and must be suitable for the real existing state, not a new discarded teaching folder. Each guarded block runs in a subshell with `set -eu`: the first failed command stops that block, while its umask does not change your terminal afterward. `test ! -e` therefore stops accidental replacement of an earlier review artifact. Do not remove that fail-fast wrapper. Do not paste a secret-bearing plan into a public issue. The prior observed 5-create result is historical, not a result promised for a fresh plan.

**Stop here for review:** source/inputs, account/Region, plan hash, actions, current costs, bucket retention and separate approval. A plan can contact AWS to refresh/read information; it does not itself execute the proposed resource creates. This chapter did not execute this cloud template.

## Step 5. Apply only the separately approved saved artifact

**Paid/resource-changing operator reference. The bootstrap approval/apply is now complete; application approval remains separate.** The owner supplies the exact approved plan path/hash and same initialized root. Set the recorded approved hash as well as the paths; the block compares it and rechecks the account before the final line. A matching hash is an integrity check, not evidence of human approval. Do not substitute a newly generated or stale plan.

```bash
(
  set -eu
  : "${AWS_PROFILE:?Select the owner-approved AWS profile first}"
  : "${OWNER_APPROVED_ROOT:?Set the exact approved initialized root}"
  : "${OWNER_APPROVED_PLAN:?Set the absolute approved saved-plan path}"
  : "${OWNER_APPROVED_SHA256:?Set the exact plan SHA256 from the approved review receipt}"
  test -d "$OWNER_APPROVED_ROOT"
  test -f "$OWNER_APPROVED_PLAN"
  test "$(aws sts get-caller-identity --query Account --output text)" = "772641336063"
  REVIEWED_PLAN_DIGEST="$(shasum -a 256 "$OWNER_APPROVED_PLAN" | awk '{print $1}')"
  test "$REVIEWED_PLAN_DIGEST" = "$OWNER_APPROVED_SHA256"
  terraform -chdir="$OWNER_APPROVED_ROOT" apply -input=false "$OWNER_APPROVED_PLAN"
)
```

Applying a saved plan runs **without a further yes/no prompt**. It can create, replace or delete resources according to that artifact. The command is shown so you understand the operation; prior concrete approval is the gate, not an expectation that Terraform will ask again. If the hash, source/input context or state differs, stop and ask the deployment owner for a fresh reviewed plan. Do not use `-auto-approve` or `-lock=false` as a workaround.

For the current bootstrap stage, read its non-secret bucket-name output after a successful approved apply:

```bash
(
  set -eu
  : "${OWNER_BOOTSTRAP_ROOT:?Set the actual initialized owner root}"
  terraform -chdir="$OWNER_BOOTSTRAP_ROOT" output -raw state_bucket
)
```

A completed bootstrap supplies state storage; it does not deploy the marketplace. Preserve bootstrap state and the existing certificate's separate state. Do not move/delete either implicitly.

## Step 6. Initialize the final ECS S3 backend after bootstrap

**Owner-operated template, only after the state bucket exists.** The owner prepares an ignored private backend file from the [source example](https://github.com/robertovalencia/linked-in-node-and-aws/blob/01c30fc0ca3958a99f6808f2211153f2d602c7c4/infra/aws-ecs-dev/backend.hcl.example): actual bucket, ECS state key `linked-in-node/ecs-dev/terraform.tfstate`, Ohio, `encrypt=true` and `use_lockfile=true`.

```bash
(
  set -eu
  : "${AWS_PROFILE:?Select the owner-approved AWS profile first}"
  : "${OWNER_ECS_ROOT:?Set the reviewed ECS working directory}"
  : "${OWNER_BACKEND_FILE:?Set the absolute prepared ECS backend-file path}"
  test -d "$OWNER_ECS_ROOT"
  test -f "$OWNER_BACKEND_FILE"
  terraform -chdir="$OWNER_ECS_ROOT" init -input=false \
    -backend-config="$OWNER_BACKEND_FILE"
  terraform -chdir="$OWNER_ECS_ROOT" validate
)
```

`init` configures backend/provider access; it can fail if the bucket or permissions are absent. A backend migration/reconfiguration prompt is not routine boilerplate. Stop for an owner-reviewed state decision rather than guessing `-migrate-state` or `-reconfigure`. The old scratch/local HTTPS preview is not the final S3-backed apply artifact. Never switch to the legacy key `linked-in-node/dev/terraform.tfstate`.

## Step 7. Save and review a new S3-backed infrastructure plan

The actual private input file contains the approved hostname/certificate/client range, current owner/expiry proposal, supported PostgreSQL version and verified broker image. Example `.invalid` names, documentation CIDRs, dummy digests and old expiry dates are **not** ready deployment inputs.

```bash
(
  set -eu
  : "${AWS_PROFILE:?Select the owner-approved AWS profile first}"
  : "${OWNER_ECS_ROOT:?Set the reviewed initialized ECS working directory}"
  : "${OWNER_ECS_INPUTS:?Set the absolute current private ECS tfvars path}"
  : "${OWNER_RUN_DIR:?Set the private review-artifact directory}"
  test -d "$OWNER_ECS_ROOT"
  test -f "$OWNER_ECS_INPUTS"
  test -d "$OWNER_RUN_DIR"
  chmod 700 "$OWNER_RUN_DIR"
  test ! -e "$OWNER_RUN_DIR/ecs-final.tfplan"
  test ! -e "$OWNER_RUN_DIR/ecs-final-plan.json"
  umask 077
  terraform -chdir="$OWNER_ECS_ROOT" plan -input=false \
    -var-file="$OWNER_ECS_INPUTS" -out="$OWNER_RUN_DIR/ecs-final.tfplan"
  terraform -chdir="$OWNER_ECS_ROOT" show -no-color "$OWNER_RUN_DIR/ecs-final.tfplan"
  terraform -chdir="$OWNER_ECS_ROOT" show -json "$OWNER_RUN_DIR/ecs-final.tfplan" \
    > "$OWNER_RUN_DIR/ecs-final-plan.json"
  chmod 600 "$OWNER_RUN_DIR/ecs-final.tfplan" "$OWNER_RUN_DIR/ecs-final-plan.json"
  shasum -a 256 "$OWNER_RUN_DIR/ecs-final.tfplan"
)
```

Shell redirection writes relative to the shell's directory, not Terraform's `-chdir`; absolute artifact paths prevent that confusion. `umask 077` applies **before** file creation because chmod afterward cannot undo an earlier exposure window. JSON plans and binary plans stay private/ignored and may contain sensitive values even when normal console output redacts them.

The [offline plan-review tool](https://github.com/robertovalencia/linked-in-node-and-aws/blob/01c30fc0ca3958a99f6808f2211153f2d602c7c4/scripts/aws-ecs-review-plan.py) additionally binds source/binary/security relationships and the private HTTPS context. Use the deployment owner's exact review invocation; passing this generic Terraform sequence is not a substitute for that project gate. The tool's default is the hostname-free shape; approved HTTPS review needs its explicit private context and dated rates. Current costs and this new saved plan need approval before the Step 5 apply pattern is used for infrastructure.

## Step 8. Read outputs, then deploy and test the application separately

After successful approved infrastructure apply, these existing outputs are useful diagnostics:

```bash
(
  set -eu
  : "${OWNER_ECS_ROOT:?Set the actual initialized owner root}"
  terraform -chdir="$OWNER_ECS_ROOT" output -raw deployment_account_id
  terraform -chdir="$OWNER_ECS_ROOT" output -raw deployment_region
  terraform -chdir="$OWNER_ECS_ROOT" output -raw alb_dns_name
  terraform -chdir="$OWNER_ECS_ROOT" output -raw application_url
)
```

An output can be null/unavailable for a deliberately unconfigured stage. `application_url` describes configured intent, not a successful HTTP request. The owner still needs exact-source image publication/scanning, secret population, owned-database bootstrap, separately reviewed task/service activation, application DNS routing, browser/API/security/recovery checks and teardown. Earlier TLS with an empty target group can produce 503; do not call it a working UI.

The [deployment walkthrough](06-deployment-security-and-operations.md) explains those stages. The [ECS runbook](https://github.com/robertovalencia/linked-in-node-and-aws/blob/01c30fc0ca3958a99f6808f2211153f2d602c7c4/docs/aws-ecs-dev.md) supplies the owner-operated publication/bootstrap procedure. AWS teardown needs its own reviewed plan, retained snapshots/state decisions and current costs; the local lab's cleanup command is not a cloud teardown recipe.

## If “trigger” means GitHub Actions

From an authenticated GitHub CLI session in this repository, the existing **verification-only** workflow can be dispatched as follows:

```bash
# Optional hosted verification dispatch; this can consume GitHub Actions minutes.
(
  set -eu
  gh workflow run deploy-dev.yml --ref main -f deploy=false
  gh run list --workflow deploy-dev.yml --limit 5
)
```

Select the actual verification run from that list, then set `OWNER_VERIFICATION_RUN_ID` to its numeric ID in the same terminal before using this observation block:

```bash
(
  set -eu
  : "${OWNER_VERIFICATION_RUN_ID:?Set the actual selected verification run ID}"
  gh run view "$OWNER_VERIFICATION_RUN_ID"
  gh run watch "$OWNER_VERIFICATION_RUN_ID" --exit-status
)
```

These commands are a reproduction reference; this documentation change did not dispatch a hosted run. Verify the selected run’s source SHA before using it as release evidence. The workflow's verification job checks source/integration and mocked Terraform configurations. There is **no Terraform infrastructure apply job**. Its optional `deploy=true` branch is the preserved EC2/SSM release path, not ECS deployment. Do not turn that input on expecting it to apply the current ECS plan. See the [actual workflow](https://github.com/robertovalencia/linked-in-node-and-aws/blob/01c30fc0ca3958a99f6808f2211153f2d602c7c4/.github/workflows/deploy-dev.yml).

## Troubleshooting in command order

| Failure | First check |
|---|---|
| No/expired credentials | Authorized temporary CLI login and fresh STS identity, not browser login alone |
| AccessDenied | Exact identity/action, policies/boundary/account constraints; viewer policies are insufficient for deployment |
| Backend bucket missing | Approved bootstrap has not completed, or the bucket/account/Region is wrong |
| State migration/reconfiguration prompt | Existing root/state ownership must be resolved before proceeding |
| Stale saved plan | Have the owner regenerate/review it; do not bypass state locking or apply a different artifact |
| URL output but DNS fails / HTTP 503 | DNS, listener, targets and application activation have separate gates |
| Expected infrastructure but console empty | Confirm account/Region/state and actual apply result; a reviewed plan is only a proposal |

**Recall:** Which step creates state storage? Why is a fresh S3-backed plan required afterward? Why is `gh workflow run ... deploy=false` not a cloud deployment? Why does a plan hash matter when saved-plan apply does not ask again?

Primary references: [init](https://developer.hashicorp.com/terraform/cli/commands/init), [saved plans and exit codes](https://developer.hashicorp.com/terraform/cli/commands/plan), [apply](https://developer.hashicorp.com/terraform/cli/commands/apply), [S3 backend/locking](https://developer.hashicorp.com/terraform/language/backend/s3).

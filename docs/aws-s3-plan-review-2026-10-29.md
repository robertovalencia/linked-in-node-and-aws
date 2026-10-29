# Actual S3-backed AWS plan review — 29 October 2026

**Superseded application artifact:** subsequent user-directed demo-data cleanup source changes mean the recorded `8cf376...` plan now correctly refuses source binding. Do not apply it. The [current operator runbook and actual stopped preflight](aws-operator-runbook-2026-10-29.md) record the new work. A fresh saved plan is blocked on intended-client and shutdown decisions; the estimates below are historical dated models, not a new plan pass.

**State bootstrap complete; application infrastructure pending approval.** The human approved only the exact five-create S3 bootstrap plan. It actually added 5 resources, changed/destroyed 0; authenticated controls and independent post-apply review pass. [Actual bootstrap execution evidence](evidence/aws-state-bootstrap-2026-10-29/README.md). Existing certificate state remains separate and preserved. No application apply, image publication, ALB endpoint or marketplace runtime verification has occurred.

## New saved application plan

| Review field | Actual result |
|---|---|
| Account/region |772641336063 / us-east-2 (Ohio)|
| Source checkout at preparation |37fc766; reviewer/documentation changes uncommitted when planned; actual embedded Terraform/provider-lock bytes equal source|
| Changes |111 creates,0 updates,0 deletes|
| Saved binary SHA256 |`8cf376c7e79bd48c459c9892eecc111e02a352d8cfd10dd8723a35eaae2c9625`|
| Actual backend |S3 `772641336063-linked-in-node-terraform-state`, key `linked-in-node/ecs-dev/terraform.tfstate`, default workspace|
| Backend safeguards |encrypt=true, use_lockfile=true, allowed_account_ids=[772641336063], explicit isolated workspace prefix|
| Application task definitions/services |0 / 0; exact-source images, secret values and bootstrap remain later stages|
| Proposed expiry metadata |2026-10-30T17:30:00Z; proposal only, not an applied deadline or automated shutdown|

The saved artifact is ignored/private at `work/aws-s3-plan-review-2026-10-29/application.tfplan`. It supersedes neither certificate nor bootstrap state. The old 111-create local-backend HTTPS preview must never be applied. [Actual binary/backend/source review, quantities and itemized ledgers](evidence/aws-s3-plan-2026-10-29/plan-review.json).

The real source root was initialized against the approved S3 bucket, not a scratch local override. Authenticated object history was empty beforehand; default workspace application key returned404. Terraform state-list exits1 for a missing state file; that expected condition was separately confirmed instead of treating it as nonempty state or migrating/importing anything. Planning created/deleted the normal S3 lock object. This is a preparation operation, not an application apply. Backend/account/key/locking/workspace proof comes from the actual saved binary, not just mutable initialization metadata. [Backend receipt](evidence/aws-s3-plan-2026-10-29/backend-initialization.json). [HashiCorp S3 backend documentation](https://developer.hashicorp.com/terraform/language/backend/s3).

## Current costs before provisioning

31 selected official rates/units/tier bounds were refreshed29 October. Selected amounts are unchanged; EC2/RDS catalog publication timestamps advanced and fresh responses are preserved. Actual saved-plan quantities match the review ledger. Gross USD before credits, taxes, recovery exercises or non-AWS tools:

| Scope | Duration | Idle | Expected | Higher use |
|---|---:|---:|---:|---:|
|Current 111-create HTTPS probe infrastructure, zero app tasks|24 h|$5.94|$6.83|$21.14|
|Current 111-create HTTPS probe infrastructure, zero app tasks|720 h /30 days|$164.29|$191.22|$622.19|
|Future five-task activation estimate, not an activation plan|24 h|$7.43|$8.32|$22.62|
|Future five-task activation estimate, not an activation plan|720 h /30 days|$208.76|$235.68|$666.66|

The account is Free/ACTIVE with100 USD remaining credits as of 29 October authenticated checks. Credits are not subtracted from gross estimates or promised to cover all charges. Usage assumptions are not caps; budgets are alerts. [Fresh tariffs/receipt](evidence/aws-s3-plan-2026-10-29/price-refresh.json) and [12 full itemized ledgers](evidence/aws-s3-plan-2026-10-29/plan-review.json) cover compute/EBS, RDS storage/backups/CPU-credit sensitivity, ALB/LCUs/IPv4, zonal NAT/data/S3 gateway, logs/queries/retention/metrics/alarms, ECR/S3, seven secrets/KMS, private DNS and transfer. [Complete phased alternatives and tradeoffs](aws-cost-review-2026-10-27/README.md).

State allocation already included in the combined S3 meter remains about$0.000972/24 h,$0.001944/48 h,$0.029165/720 h for1 GB retained versions plus1 PUT/LIST and10 GET per hour. Do not add it again. Private CloudMap zone charges are not prorated; the30-day scenario crosses October/November and includes2 calendar charges. No public Route53zone, purchased domain, MSK, WAF, customer KMS key, paid security-service enablement or interface endpoints are proposed. Single-AZ compute/database/Kafka are cost compromises with recovery work, not high availability.

## Network and operational scope

The unchanged [architecture/traffic matrix](aws-ecs-dev.md) remains authoritative. One approved IPv4 /32 can reach ALB443 over TLS1.2/1.3 using the issued nonexportable certificate for `app.linked-in-node-rv.dynv6.net`. Other hosts get403. ALB SG can reach only frontend 8180; frontend reaches the four private API ports; Inquiries reaches Catalog 8182; API/bootstrap SGs reach RDS 5432; only Inquiries/Notifications reach Kafka 9093. There is no public SSH, database, broker or direct API ingress. Internal API HTTP hops remain documented; DB/broker clients verify TLS.

Current plan creates an empty frontend target group and no application tasks. A permitted-host503 after infrastructure apply is expected until activation and proves no user journey. Unknown-host403 is only listener-policy evidence. Seven alarms have no configured notification destination; metric/alarm configuration does not prove emission, delivery or operational response. Account create permissions/capacity are not established by a successful plan; the Free plan's existing restrictions still apply. The generated broad IAM operator draft is neither attached nor an execution prerequisite.

## Strict reviewer and independent gates

`--s3-backend-context` explicitly selects actual S3 mode. The reviewer decodes only the pinned Terraform 1.17.0 saved-plan backend schema and fails closed on another producer/format. It rejects local/alternate backends, changed bucket/key/workspace/region, unlocked/unencrypted state, static credentials/profile/role/endpoint/skip-check overrides, extra Terraform source and unreviewed account settings. Existing source/JSON/template/privacy and HTTPS/SG graph gates remain enforced. Meaningful negative controls mutate actual saved backend bytes; original network controls stub only `terraform show` while retaining real source checks. Both valid actual and legacy fixtures must be accepted first. [Results](evidence/aws-s3-plan-2026-10-29/s3-negative-controls.json):54 actual S3 controls,23 legacy HTTPS controls,11 hostname-free controls pass. These are offline controls, not AWS runtime security tests.

Reproduce from repository root (no AWS calls/apply):

```bash
python3 scripts/aws-ecs-review-plan.py \
  --plan-json work/aws-s3-plan-review-2026-10-29/plan.json \
  --plan-binary work/aws-s3-plan-review-2026-10-29/application.tfplan \
  --https-context work/aws-s3-plan-review-2026-10-29/https-context.json \
  --s3-backend-context work/aws-s3-plan-review-2026-10-29/s3-backend-context.json \
  --rates-file docs/evidence/aws-s3-plan-2026-10-29/rates.json \
  --report work/aws-s3-plan-review-2026-10-29/recheck.json
```

[Independent critic](evidence/aws-s3-plan-2026-10-29/critic.md) assesses preparation readiness only. The biggest remaining gap is the unprovisioned/unactivated application and therefore untested cloud runtime, security, observability, recovery and rollback behavior.

## Next approval and 24-hour shutdown boundary

This application plan is not authorized to apply. Before any paid infrastructure start, agree the exact24-hour UTC deadline, teardown ownership/scheduler, database snapshot/backup/secret/log/state retention decisions and current allowed client address. Refresh the proposed expiry/input/saved plan and its review if timing, topology, source or account conditions change; old approval cannot apply to a changed artifact. An ExpiresAt tag does not shut anything down. The demo clock starts with the first billable application-infrastructure provisioning, not with later successful activation. State bootstrap alone did not start it.

After explicit exact-plan/current-cost approval: recheck same-effective-environment identity/artifact/source/backend; apply only the approved artifact. Then verify actual private topology/TLS and publish only exact-source CI-verified scanned immutable images, populate secrets outside Terraform, run owned-DB bootstrap/migrations, and prepare/review the separate task activation plan. Set actual dynv6 application CNAME only once the ALB exists. Require target health,48 API acceptance checks, browser journeys, authorization/identity denials, log/metric delivery, broker replay, isolated DB restore RPO/RTO and bad-release rollback before claiming a working deployment. The preserved EC2/SSM deploy=true workflow is not the ECS release path.

At the agreed24-hour limit, destroy ALB/NAT/EIP/compute/RDS rather than only stopping. RDS deletion protection requires a reviewed transition; final snapshots/retained backups, secret recovery windows, logs, ECR, operation-bucket versions and state versions can outlive the app and continue costing. Preserve required data/state offline, explicitly inventory retained resources, and separately review protected state-bucket removal after dependencies are gone. First deployment has no prior good ECS release; image rollback cannot undo destructive migrations, rotated keys or lost writes. [Detailed recovery/rollback/teardown runbook](aws-ecs-dev.md).

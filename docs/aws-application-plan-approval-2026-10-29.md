# Application infrastructure approval package — 29 October 2026

**A new matching S3-backed plan is prepared; no application resources have been applied.** The human explicitly approved the current-IP lookup and private single-/32 rule preparation. The real CLI and in-app browser used the same observed route. The rule remains one approved client, not Internet-wide ingress. Exact address/contexts/raw plans remain owner-only and out of Git. [Actual command journal and evidence](evidence/aws-application-plan-2026-10-29/README.md).

## Exact artifact and expected behavior

| Field | Actual result |
|---|---|
|Account/region|772641336063 / us-east-2 (Ohio)|
|Source at planning|`0a068845de05701eca83809c803db1625196235d`, clean; embedded Terraform/provider lock match current source|
|Saved binary SHA256|`2fd776a529ab587759500bf71e43c5f461a528034db2942d5af2f664fe222b56`|
|Private saved artifact|`work/aws-operator-preparation-2026-10-29/final-plan-run/application.tfplan`|
|Resource actions|111 creates,0 updates,0 deletes|
|Actual backend|Encrypted/locked S3, exact ECS key, default workspace, allowed-account guard|
|Applications|0 task definitions / 0 services; deploy_application=false, seed_demo=false, teardown_discard_demo_data=false|
|Planning expiry tag|2026-10-30T22:00:00Z; proposal only, not a timer or actual deadline|

This is the infrastructure stage: private VPC/subnets/trust, one ALB with HTTPS/host routing, one zonal NAT/EIP, private Kafka EC2/EBS, private Single-AZ RDS PostgreSQL, ECR repositories, secret metadata, discovery, operations storage and logs/alarms. It creates paid resources but cannot yet serve marketplace journeys. Secret values, exact-source scanned images, database/broker bootstrap and separately reviewed activation remain later stages.

The initial protections are retained: RDS deletion protection and snapshot/backup safeguards, operations force_destroy=false, runtime-secret recovery 7 days, encrypted/private data resources and zero app tasks. The selected eventual demo-data discard policy is implemented through a separate explicit cleanup transition after tasks stop, then a separately reviewed destroy plan. It does not weaken ordinary initial deployment protections.

The old 8cf application artifact correctly refuses changed source. The first current-client artifact dc389 was superseded by refreshed timing metadata. Never apply either. State bootstrap/certificate have separate preserved state; no bootstrap reapply or state migration is needed.

## Current gross cost estimate

The current plan reviewer binds actual quantities to the dated 31-rate official Ohio packet refreshed 29 October and recalculates all 12 itemized ledgers. Shared credits/free allowances are not deducted; these are usage assumptions, not caps.

| Scenario |24hours|720hours /30days|
|---|---:|---:|
|Infrastructure idle|$5.94|$164.29|
|Infrastructure expected probes|**$6.83**|**$191.22**|
|Infrastructure higher usage|$21.14|$622.19|
|Future five-task activation expected, not in this plan|**$8.32**|**$235.68**|

[Full ledgers and quantities](evidence/aws-application-plan-2026-10-29/plan-review.json) include compute/storage, ALB/LCUs/IPv4, NAT/data, RDS/backups/credit sensitivity, logs/metrics/alarms/queries, ECR/S3, seven secrets/KMS, private DNS and transfer. The fresh preflight reports Free/ACTIVE with $100 USD credits; this is not a promise of complete coverage or create permission. Recovery exercises, taxes and non-AWS tooling are separate. No automatic-cleanup controller/service is selected or added.

After successful complete discard cleanup, retained demo snapshots/backups/logs/images/operation objects are not intended. Existing manual/recovery snapshots and service-managed secret outcomes need actual scoped verification. The preserved encrypted/versioned Terraform state allocation remains about $0.000972/24h or$0.029165/720h under 1 GB/version/request assumptions, not a cap. The separate nonexportable ACM certificate has no additional certificate fee. Delayed/asynchronous deletion and billing can leave residual charges until verified.

## Time, cleanup and approval boundaries

The human selected **operator-assisted cleanup 24 hours from the first billable application resource**, with human return/login renewal and exact teardown-plan approval. No controller, reminder or unattended cutoff exists. Actual T0 and T0+24h UTC deadline will be recorded at provisioning, rather than pretending the planning tag is an actual clock. The current tag proposes 22:00 UTC on 30 October; reconcile the actual start/deadline in the private run record/progress journal and refresh the plan if reviewed input/source/timing conditions materially change before apply.

Plan for human return around hour 22: renew temporary login, freeze writes, preserve sanitized evidence, review/apply cleanup transition and verify actual RUNNING/PENDING service/standalone tasks are zero. Then review/apply a real saved destroy plan and verify hourly resources are absent before the 24-hour target. AWS deletion is asynchronous; operator unavailability/API failures can extend charges. [Detailed guarded commands and selected discard transitions](aws-operator-runbook-2026-10-29.md).

Neither a meaningful current cleanup-transition plan nor a meaningful destroy plan can be generated while application state is absent. Their actual future resources/actions/hashes must be reviewed from real state. Preserve bootstrap, certificate and application Terraform state; do not delete account-wide snapshots or unrelated resources. Image rollback cannot reverse discarded data.

## Exact next action after explicit approval

The human's IP/preparation/retention choices do not authorize this apply. After approval of this exact artifact/current costs, the operator will show each command, verify the same effective AWS account/environment, source/provider-lock/backend/workspace/hash and owner-only artifacts, then run the exact saved-plan apply:

```bash
terraform -chdir=infra/aws-ecs-dev apply -input=false \
  /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-operator-preparation-2026-10-29/final-plan-run/application.tfplan
```

This is a proposed consequential action, **not an executed command**. A saved-plan apply does not ask Terraform's usual interactive approval question; the explicit human approval and preceding checks are mandatory. Failed/mismatching checks stop execution; no alternate channel or stale artifact is permitted. Actual T0/deadline, each command/output and resource-control verification will be recorded after an approved apply.

A failed apply is not an automatic rollback. Preserve partial state and logs, record the earliest billable resource and its24-hour deadline even on failure, inspect actual remaining resources and stop activation. Review any repair/cleanup plan; do not upgrade the account or bypass managed restrictions to force completion.

After infrastructure: verify actual TLS/SG/private topology, run exact-source Sonar/acceptance/image gates, populate secrets outside Terraform, bootstrap databases/broker, and prepare/review separate image-registration/activation plans. Only then configure the actual application DNS CNAME and require target health, 48 API checks, browser journeys, authorization/identity denials, CloudWatch emission, replay/restore/rollback evidence. An empty target group can return 503; that is not a working marketplace.

[Independent final critic](evidence/aws-application-plan-2026-10-29/critic.md) judges preparation only. Source Verify [40949770714](https://github.com/robertovalencia/linked-in-node-and-aws/actions/runs/40949770714) passed source/integration/Terraform at 0a068845, including the new helper tests; it is not AWS deployment evidence. Raw plans/contexts/transcripts stay private, while the journal publishes sanitized actual command/exit evidence.

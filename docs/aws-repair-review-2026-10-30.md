# Infrastructure repair review — 30 October 2026

**Preparation review PASS for the exact saved repair plan. No repair apply approved or performed.** The earlier human-approved initial plan failed partially. [Actual execution, failures and independent critic](evidence/aws-infrastructure-apply-2026-10-29/README.md).

The shutdown deadline remains **today, 30 October, 5:51:25 PM EDT / 21:51:25 UTC**. Return by **3:51 PM EDT** for operator-assisted cleanup preparation, renewal and exact approval. There is no automatic teardown. Preserve the separate Terraform state bucket and ACM certificate; discard synthetic demo data only through separately reviewed cleanup artifacts.

Current authenticated read-only checks at 14:40 UTC: Free/ACTIVE, $98.59 reported credits, 100 managed state instances, only ALB tainted; no RDS, listener or application tasks. Partial allocations remain billable. The original plan has been consumed and must not be retried.

The proposed repairs preserve private networking and the approved client rule: explicit one-day automated backup retention with seven-day source default; broker registration through Cloud Map; documented regional/account ALB log delivery and explicit tainted-ALB replacement. Fresh planning exposed latest-AMI drift and ineffective empty custom-health configuration, so the broker AMI will be pinned and the five empty discovery services corrected and explicitly reviewed.

Official Ohio prices refreshed at 14:39 UTC: all 31 rate/unit/tier selections unchanged. Full steady-state comparison: infrastructure idle/expected/higher **$5.95/$6.84/$21.14 per 24 hours**, **$164.39/$191.32/$622.29 per 720 hours**. Future five-task application, not in this repair scope: **$7.43/$8.32/$22.62**, **$208.86/$235.78/$666.76**. These windows do not extend the deadline.

At 14:41 UTC, hypothetical immediate repaired expected recurring cost through the same deadline was **$1.89**, excluding the existing October zone charge, replacement reserve and billing tails. Current unrepaired fixed envelope is approximately **$0.186/hour**, excluding the zone and all unmeasured usage. A separate illustrative replacement reserve is **$0.0325** under its bounded one-hour assumption. None of these are invoices or caps; credits can lag consumption. One-day retention reduces the recovery window, and Free-plan acceptance remains unproven. Backup GB assumptions remain conservative and unchanged.

The saved binary and exact changes are available below. The source-bound mixed-action reviewer, 56 negative controls and eight additional independent controls pass; a fresh critic accepts preparation only. No application activation, secret population, image publication, DNS change, account upgrade or new 24-hour run is authorized by repair preparation.


## Exact saved repair artifact

Binary SHA256: `cd87e0ed4e5fd86fcfcbb4a0d4ffbcb443140a87fd754de7a61ff3408bddacd1`.

Private binary: `work/aws-infrastructure-repair-2026-10-29/plan/repair.tfplan`. Its decoded JSON, actual baseline, context, broker template and inputs are owner-only siblings. [Sanitized action summary](evidence/aws-repair-plan-2026-10-30/summary.json) · [current full cost ledger](evidence/aws-repair-plan-2026-10-30/costs.md).

Terraform proposes **18 adds, 82 updates, 6 destroys**. This means 12 previously missing new resources plus six explicit replacements, yielding 112 managed instances after a successful repair:

| Action | Exact scope and purpose |
|---|---|
|Replace 1 ALB, delete before create|The persisted ALB is tainted after failed log-attribute configuration. Preserve HTTPS-only client trust, logging, header controls and existing certificate; install the listener/rule only after corrected bucket policy|
|Replace 5 empty app discovery definitions|Catalog, frontend, identity, inquiries and notifications. Actual ListInstances read-back proves zero registered instances. Set explicit custom-health threshold 1 so provider 6.70 sends the intended configuration; empty blocks were omitted. ECS supplies future health status; Cloud Map is not an active health monitor|
|Create 12 missing resources|1 private RDS, HTTPS listener + host rule, 7 alarms, broker Cloud Map service + instance registration|
|Update 82 existing resources|Deadline tags only, including the broker root-volume tags, except the operations-bucket policy update that grants the official ALB log-delivery scope. Tags use 21:51:25Z, rounding the operative deadline down by a fraction of a second|
|Preserve the broker and its disk|Explicit AMI pin equals the deployed AMI; same EC2 instance ID and root EBS volume ID. No lifecycle-ignore workaround, import, targeting, untaint or state rewrite|

The final plan has no resource deletions outside those six replacements. No ECS task definitions/services/tasks, secret versions, database bootstrap, images or public DNS record are included. One approved client /32 remains private in the inputs and plan; there is no SSH, database or Kafka internet ingress. Logging is not disabled to bypass the earlier failure.

## Commands and actual results

Working directory: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/infra/aws-ecs-dev`. The agent uses a cleaned environment pinned to profile `marketplace-dev` and Ohio; these commands contain no secret values.

```bash
terraform fmt -check -recursive
terraform validate -json
terraform plan -input=false -lock-timeout=60s -detailed-exitcode -json \
  -var-file=/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-infrastructure-repair-2026-10-29/plan/inputs.tfvars.json \
  -out=/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-infrastructure-repair-2026-10-29/plan/repair.tfplan
terraform show -json /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-infrastructure-repair-2026-10-29/plan/repair.tfplan
```

The command block records the actual subprocess arguments. The agent captured raw `terraform show -json` output directly into the owner-only ignored `plan.json`; it was not printed in a public transcript or copied into Git. Do not paste raw plan/state JSON into a chat, issue or CI log.

Actual results: fmt 0, validate 0, plan 2 (changes), show 0. The provider warns that custom-health failure_threshold is deprecated and always 1; explicit 1 is intentional for its nonempty request behavior. Eighteen isolated backend-disabled Terraform test runs passed. Raw plan output and transcripts remain private. The first plan with unintended broker replacement remains rejected and preserved; it is not this artifact.

## Repair, rollback and recovery boundaries

One-day retention keeps automated backups enabled but shortens the possible recovery history from seven days. It does not establish a one-day RPO; actual RPO/RTO need a separate recovery exercise. The prior error proves seven days was rejected, not that one day will succeed. Keep the account Free; stop on any service rejection rather than upgrade or silently disable protections.

ALB replacement removes the incomplete physical ALB before creating its replacement. There is currently no working listener or application to preserve, but a replacement can still fail and leave paid partial allocations. Keep actual state and diagnostics; generate another reviewed repair or cleanup plan from the resulting state. Never retry the consumed initial artifact or the rejected AMI preview. Preserve separate state-bootstrap/certificate roots.

After separately approved execution, verify RDS encryption/private access/deletion protection/retention, actual ALB log-delivery test object and real logs, TLS with the issued certificate, correct-host empty-target response and wrong-host denial, Cloud Map DNS registration, seven alarms and the absence of app tasks. A prepared configuration or successful apply alone does not prove these runtime gates. Application activation and recovery exercises remain separate reviewed scopes. The cleanup transition and final destroy artifacts must be prepared from the resulting actual state before their own approval; no automatic cleanup is installed.

Official references: [ALB log policy and verification](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/enable-access-logging.html), [Cloud Map registration](https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html), [custom-health semantics](https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html), [provider 6.70 implementation](https://github.com/hashicorp/terraform-provider-aws/blob/v6.70.0/internal/service/servicediscovery/service.go), [RDS retention](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.BackupRetention.html).

## Provider read-back details and remaining live checks

The configured root-volume `tags.ExpiresAt` is exactly 21:51:25 UTC. Provider 6.70 retains the prior 22:00 value in its computed `root_block_device.tags_all` mirror in this saved plan. This is disclosed, not treated as actual correction. Its update implementation applies the explicit changed `tags` to the existing volume ID and uses the `tags_all` branch only when `tags` did not change. The reviewer may accept only this exact unchanged computed mirror, with all other ownership tags and volume protections preserved. Actual `DescribeVolumes` after an approved repair must confirm the live deadline tag. [Provider implementation](https://github.com/hashicorp/terraform-provider-aws/blob/v6.70.0/internal/service/ec2/ec2_instance.go#L1816).

Existing security groups also contain computed ingress/egress read-back arrays for the standalone rules. No inline ingress/egress expressions are configured. Their 35 exact trust paths were independently flattened and compared with the standalone rules; this is not permission to ignore extra mirrored rules. The strict repair review must reject a changed peer, port, CIDR, configured inline rule or unexpected mirror. Frozen-state broker/AMI/EBS identities and protections must remain bound despite normal provider refresh normalization.

Rejected artifacts are preserved privately: first unintended latest-AMI replacement; then missing explicit volume expiry; and the initial overly strict local assertion that both configured `tags` and computed `tags_all` were immediately canonical. That last assertion failed, triggering the provider-source check and the narrowly documented live-verification boundary above. No failed evidence is relabeled as a pass.

## Independent final verdict and approval boundary

The [fresh harsh critic](evidence/aws-repair-plan-2026-10-30/critic.md) accepts this exact preparation. It independently reran the real mixed-action reviewer, all **56 negative controls**, **8 additional controls**, and **28 fake-CLI operator tests**; inspected the **18 passed Terraform mock runs**; and recomputed **372 item products / 12 ledgers**. It verified the recorded empty-instance API receipts and the frozen/refreshed/planned broker and disk controls. No new AWS mutation was made during review.

The repository [working agreement](../AGENTS.md) requires separate approval for the concrete changed saved plan and current costs. The initial apply approval does not cover these replacements or reduced backup retention. Approval of this exact artifact would authorize infrastructure repair only, with the original deadline, no account upgrade, no app activation, and mandatory actual read-back. Any source/input/binary or material state change requires another plan/review; do not substitute an older artifact.

At **15:02 UTC on 30 October**, the remaining interval is **6.82 hours**. If repaired immediately, expected recurring gross cost through the same deadline is approximately **$1.80**, plus the separately stated $0.0325 bounded replacement reserve, previously incurred charges, usage variation and billing/deletion tails. The existing October zone charge is not added again. [Deterministic current calculation](evidence/aws-repair-plan-2026-10-30/remaining-window.json). This is not a cap or a new 24-hour run.

---
title: "Disaster recovery, backup and resilience testing"
topic: "Disaster recovery, backup and resilience testing"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 68 · Disaster recovery, backup and resilience testing

**Prerequisites:** Data services, storage/encryption, SLOs and release rollback.

[Previous lesson](67-otel-tracing-slos-and-incidents.md) · [Next lesson](69-cloud-cost-allocation-and-optimization.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. Name the loss you need to recover from

Recovery-time objective describes a target restoration interval; recovery-point objective describes acceptable data loss. Define the event being considered: accidental deletion, failed schema migration, instance loss, availability-zone failure or regional outage. Different failures require different controls. A restarted container is not a disaster-recovery demonstration.

The existing project stores PostgreSQL and Kafka volumes on an encrypted root disk that is deleted on instance termination. Logical service ownership does not remove that shared failure domain. Inspect the actual [root-disk configuration](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) and [Docker volume mapping](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/compose.yaml) to verify where durable data lives. A source repository and image registry can rebuild software, but they do not contain the current business data.

## 2. Separate backup existence from recoverability

A backup policy needs scope, schedule, consistency, retention, encryption, access and restore ownership. An object or snapshot being present does not prove it is readable with available keys or that a restored application can use it. Cross-account or cross-region copies also require a deliberate identity/key and dependency design. Do not promise recovery merely because a service advertises automated backup support.

For a relational database, decide how application consistency and point-in-time requirements are met. For an event stream, consider retention, consumer offsets, replay and downstream idempotency. Restoring the database and replaying events from a different point can cause duplicates or missing projections unless reconciliation is designed.

## 3. Compare recovery strategies as tradeoffs

Backup/restore, pilot light, warm standby and active/active maintain different amounts of ready capacity and state. More pre-existing capacity can reduce some recovery steps while increasing cost and complexity. Multi-region operation introduces replication, consistency, routing, keys and operational decisions; it is not simply another Terraform region alias.

A Multi-AZ design addresses selected local failure domains but is not automatically regional disaster recovery. Replication can also copy an accidental write or corruption. Recovery planning must include logical mistakes, not just hardware outages.

## 4. Test a complete restore path

A useful drill restores into an isolated destination, validates the intended recovery point, checks service credentials/schema, runs business journeys and records measured restoration time. Avoid overwriting the only good environment as a first test. Define cleanup and evidence retention before the drill so temporary resources and restored sensitive data do not linger.

## 5. Practice resilience without uncontrolled disruption

A fault experiment should state a hypothesis, scope, steady-state check, abort condition, recovery procedure and evidence. The local broker-outage drill is a bounded example; it does not authorize disabling arbitrary account services. Learning can start with local database export/restore on disposable data or a paper exercise when the current environment is not isolated enough.

## 6. Connect release rollback and data recovery

Restoring an old image cannot reverse a destructive migration or recreate a deleted disk. Prefer compatible expand/contract changes and define when to roll forward versus restore. A backup kept without a usable key or current restore procedure is an incomplete recovery asset.

## Example and current-project boundary

**New recovery design worksheet:**

| Failure | Proposed recovery asset | Verification |
|---|---|---|
| Lost host disk | Independently stored database backup and rebuild procedure | Restore into isolated target and run inquiries/ownership checks |
| Replayed events | Stable event IDs and durable consumer deduplication | Repeat selected events; verify one effect |
| Bad schema change | Compatible migration or tested restore/roll-forward path | Verify both application versions against intended schema |

This table proposes tests. It does not claim the portfolio has already deployed backups, RDS failover or multi-region capacity.

## Practice with observable evidence

1. Choose two explicit failure scenarios and state assumed RTO/RPO values without claiming they are achieved.
2. Inventory software artifacts, business data, secrets, encryption keys, Terraform state and external DNS dependencies.
3. Write an isolated restore drill with success/abort criteria and the business checks required afterward.
4. Identify the decision/evidence that must go to the deployment-cost owner before any AWS drill is scheduled.

**Expected evidence:** a recovery asset/dependency map and a reproducible drill plan that measures restoration rather than assuming it.

## Recall and interview defense

### Is replication a complete backup strategy?

No. Replication can propagate unwanted changes. Recovery must address deletion, corruption, consistency and usable restoration points.

### Does a successful local restart prove the RTO/RPO for AWS?

No. State which failure was exercised and measure the actual recovery path in the relevant environment.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [AWS disaster recovery strategies](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
- [RDS backup concepts](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html)
- [AWS Backup concepts](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html)

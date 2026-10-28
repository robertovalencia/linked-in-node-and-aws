---
title: "RDS PostgreSQL: backups, failover, and connection recovery"
topic: "RDS PostgreSQL: backups, failover, and connection recovery"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 57 · RDS PostgreSQL: backups, failover, and connection recovery

**Prerequisites:** 48, 54, and 56; transactions and the project’s service-owned databases.

[Previous: 56](56-ec2-autoscaling-and-eks-comparison.md) · [Next: 58](58-data-caching-and-dynamodb-design.md) · [Study path](../README.md)

**Implementation boundary:** The current application uses PostgreSQL containers on its EC2 host. It does not declare Amazon RDS. This lesson is an educational managed-database proposal and does not migrate or access any database.

RDS for PostgreSQL manages infrastructure around the PostgreSQL engine, including supported backup, maintenance, and availability mechanisms. A DB subnet group identifies subnets for database placement. A Multi-AZ DB instance deployment provides a standby for availability and failover; that standby is not a read-scaling endpoint. Read replicas serve a different purpose and commonly use asynchronous replication. Backup/restore protects against recovery scenarios that replication alone cannot solve, such as an accidental delete replicated to a standby.

## 1. Preserve logical data ownership during migration

The project’s four capabilities own separate databases and credentials even when sharing one PostgreSQL server. A move to RDS should preserve those boundaries and explicit grants. Managed infrastructure does not authorize cross-service joins or shared application logins. Define TLS, parameter settings, extension compatibility, connection limits, and migration method. Decide who can administer the instance versus who can read business data. Database engine privileges are distinct from IAM permission to manage the RDS resource.

## 2. Design private connectivity and credential handling

A proposed DB subnet group should fit the intended multi-zone arrangement, with database ingress from the application SG on PostgreSQL’s port. A private endpoint must resolve and route correctly from the workload. Require the application’s chosen PostgreSQL TLS verification behavior, not merely a claim that “RDS is encrypted.” Retrieve credentials through an approved secret mechanism and size connection pools across all replicas. Multiplying application tasks can exhaust database connections even when CPU remains moderate.

## 3. Distinguish availability from read scaling

A classic Multi-AZ DB instance synchronously maintains a standby for failover support; applications connect using the appropriate primary endpoint and must reconnect after failover. A read replica can offload eligible reads but may lag, so read-after-write expectations matter. Other RDS Multi-AZ cluster models have different readable-instance behavior; name the exact model rather than generalizing every Multi-AZ option. Multiple zones improve availability against certain failures; they do not automatically provide cross-Region disaster recovery.

## 4. Specify recovery objectives and restore evidence

Recovery point objective (RPO) describes acceptable data loss measured in time; recovery time objective (RTO) describes acceptable restoration time. Automated backups, transaction-log retention, manual snapshots, and copies serve distinct recovery needs. Restoring typically creates a separate database resource, so applications need a controlled validation and cutover plan. A successful backup job is weaker evidence than a verified restore with expected records and permissions. Define how secrets, network access, schema, and application state are validated after restoration.

## 5. Prepare clients for failures and maintenance

Failover can interrupt sessions and leave a client uncertain whether a write committed. Reconnect with bounded retries and use operation-level idempotency where the business operation may be repeated. Do not retry every transaction blindly, especially after a lost response. DNS caching, pool recycling, transaction timeouts, and driver behavior affect recovery. Maintenance and engine upgrades also need compatibility testing. A database endpoint remaining the same does not guarantee existing TCP connections continue to work.

## Source or illustrative example

**New illustrative recovery scenario:** an operator deletes inquiry rows, and replication faithfully copies the deletion. Failing over to the standby does not recover the pre-delete records. A separate point-in-time restoration followed by business validation may be appropriate. **Actual source anchor:** [architecture and database ownership](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/docs/architecture.md) describe today’s logical boundaries; they are not evidence of RDS backups or a completed restore.

## Safe exercise

Run a local recovery-objective comparison:

```sh
python3 - <<'PY'
acceptable_loss_minutes = 5
observed_restore_minutes = 23
required_restore_minutes = 15
print('RPO requirement:', acceptable_loss_minutes)
print('RTO met:', observed_restore_minutes <= required_restore_minutes)
PY
```

Expected outcome: RPO requirement 5 and `RTO met: False`. The observed duration is a fictional exercise input, not a measured project result. Write a restore runbook with source backup, target isolation, integrity checks, role/grant checks, reconciliation, cutover, and rollback criteria. No database calls are needed.

## Failure diagnosis

A connection timeout calls for DNS, routing, SG, and endpoint checks; password failure calls for credential/version and database-role checks. Read-after-write inconsistency may be replica lag or incorrect endpoint selection. Following failover, stale pooled sessions may need replacement even when DNS is correct. A restore that starts but misses records may reflect the chosen recovery point or application expectations; compare timestamps and transaction evidence before declaring success.

## Recall and answers

### Does a standby protect against an application deleting valid rows?

Not by itself. Replication can copy the deletion; recovery requires an appropriate independent restore path.

### Does Multi-AZ always mean read scaling?

No. The classic single-standby DB instance model uses its standby for availability, not ordinary read queries.

## Mastery check

Explain the difference among failover, read replica, backup, point-in-time restore, and cross-Region recovery. Produce a proposed restore checklist and a connection-recovery policy for uncertain writes. State explicitly that the existing project has no measured RDS recovery result.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [RDS backup and restore](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)
- [Multi-AZ single-standby DB instances](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html)
- [RDS read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)

---
title: "Amazon MSK: Kafka security and operations"
topic: "Amazon MSK: Kafka security and operations"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 59 · Amazon MSK: Kafka security and operations

**Prerequisites:** 46–49 and the project outbox/inbox lesson; 57 recovery concepts.

[Previous: 58](58-data-caching-and-dynamodb-design.md) · [Next: 60](60-sqs-sns-eventbridge-and-workflows.md) · [Study path](../README.md)

**Implementation boundary:** The project runs a Kafka container and at-least-once outbox delivery. Amazon MSK is not declared. A managed Kafka proposal preserves application delivery semantics rather than creating a new exactly-once guarantee.

Kafka is a retained partitioned event log. A topic contains partitions; ordering is defined within a partition, and a consumer group tracks progress using offsets. Amazon Managed Streaming for Apache Kafka (MSK) operates supported Kafka infrastructure with service-specific security and operational features. A broker being managed does not choose partition keys, define event contracts, eliminate duplicate publication, or prove that a consumer’s database effect happened exactly once.

## 1. Preserve the producer and consumer contract

The inquiries service commits its record and outbox together, then publishes and records delivery. A crash after broker acknowledgment but before updating the outbox can publish again. Notifications must continue deduplicating by durable event identity. Moving the broker to MSK does not merge the PostgreSQL transaction with Kafka acknowledgment. Define event version, key, schema compatibility, retention, and consumer ownership before discussing the managed service. Separate producer retry safety from consumer side-effect safety.

## 2. Map network reachability and authentication

Clients need bootstrap discovery and connectivity to the brokers returned in metadata, not just a successful first TCP connection. Select supported private connectivity, TLS settings, and security groups for the chosen MSK mode. Authentication establishes client identity; authorization controls topic/group operations. IAM access control is a supported option for compatible clients and uses IAM policies for IAM identities; Kafka ACLs do not govern those IAM identities. Verify library support rather than assuming any existing SASL configuration works unchanged.

## 3. Handle secrets correctly for SCRAM designs

If choosing SASL/SCRAM, follow MSK’s Secrets Manager requirements: the secret name begins `AmazonMSK_`, it uses a customer-managed KMS key, and it is associated with the cluster through the documented mechanism. A secret encrypted under the default Secrets Manager key cannot be substituted. Never commit a real JAAS password or broker credential to examples. Define rotation, client refresh, and who may read the secret. An ARN reference is only the start of the access and lifecycle design.

## 4. Understand partitions, replicas, and acknowledgment tradeoffs

Partitions determine ordering boundaries and constrain useful consumer parallelism within a group. Replication and in-sync replica settings affect durability and availability tradeoffs; acknowledge settings and producer idempotence require compatible configuration. Adding partitions can change key-to-partition mapping and deserves review for ordered business streams. Retention governs replay availability, not business-record retention in PostgreSQL. Broker infrastructure redundancy and application-level deduplication solve different problems and should both appear in the failure analysis.

## 5. Monitor progress and rehearse operational incidents

Consumer lag indicates distance between produced records and a group’s progress; lag age, handler errors, and business delay provide additional context. Watch relevant broker, storage, network, and replica-health metrics for the selected deployment mode. A consumer can acknowledge progress too early and lose effects, or too late and repeat effects. Rebalances and rolling maintenance should be normal operational events the application tolerates. Verify recovery and replay procedures without claiming a broker metric alone proves end-to-end business delivery.

## Source or illustrative example

**Actual source anchor:** [outbox and notification inbox architecture](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/docs/architecture.md) describes why duplicates are expected today. **New illustrative MSK proposal:** retain the same event identity while replacing the broker endpoint and implementing compatible TLS/authentication. That proposal is not an existing Terraform resource, a completed migration, or a measured throughput result.

## Safe exercise

Run a local deduplication demonstration:

```sh
node --input-type=module <<'JS'
const deliveries = ['event-7','event-7','event-8'];
const inbox = new Set();
for (const id of deliveries) {
  if (!inbox.has(id)) { inbox.add(id); console.log('effect:', id); }
}
console.log('effects:', inbox.size);
JS
```

Expected outcome: two effects for three deliveries. The in-memory Set is an illustration only; real crash-safe deduplication needs durable uniqueness and transactional effect handling. Draw crash points before and after producer acknowledgment, outbox marking, consumer commit, and offset advancement.

## Failure diagnosis

If bootstrap connects but produce fails, inspect broker metadata addresses, network reachability, TLS, and topic authorization. Authentication errors are different from a denied group or topic operation. Increasing consumer replicas does not help after the relevant partition parallelism is exhausted. Growing lag with normal broker health may indicate a slow database or poison event. Replayed events creating duplicate notifications indicate a consumer effect/idempotency defect rather than proof that MSK failed its infrastructure responsibilities.

## Recall and answers

### Does MSK make the outbox-to-notification flow exactly once?

No. Cross-system crash windows still require durable idempotent effects.

### Why can bootstrap connectivity be insufficient?

Kafka clients discover and connect to broker addresses from metadata, so the full broker path must work.

## Mastery check

Explain one complete publish-and-consume crash timeline, a partition ordering boundary, and an authentication/authorization distinction. Produce a proposed MSK security checklist and a lag diagnosis tree. Identify every unimplemented component rather than claiming the local Kafka broker is MSK.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [MSK security](https://docs.aws.amazon.com/msk/latest/developerguide/security.html)
- [MSK monitoring](https://docs.aws.amazon.com/msk/latest/developerguide/monitoring.html)
- [MSK IAM access control](https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html)
- [MSK SCRAM secret requirements](https://docs.aws.amazon.com/msk/latest/developerguide/msk-password-tutorial.html)

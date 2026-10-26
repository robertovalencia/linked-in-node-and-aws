---
title: "Cloud data choices: PostgreSQL, Kafka and managed alternatives"
topic: "Cloud data choices: PostgreSQL, Kafka and managed alternatives"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 28 · Cloud data choices: PostgreSQL, Kafka and managed alternatives

**Prerequisites:** 07,09–10 and 25–27; transactions, outbox and consumer offsets.

[Previous: 27](27-aws-s3-artifacts-and-secrets.md) · [Next: 29](29-aws-observability-and-incidents.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Start with access patterns and invariants

The existing product needs relational ownership, filtering, inquiry transitions and atomic inquiry/outbox insertion. PostgreSQL supplies those transactions and constraints. Notifications deduplicate by event identity before offset acknowledgment. Cloud hosting does not remove these application requirements. Choose a managed service based on access pattern and operational needs, not because its name appears in a job description.

## 2. Identify the implemented failure domain

Four database roles/databases share one PostgreSQL container; Kafka is a single broker/controller. Both persist to volumes on the host root disk. Container restart tests demonstrate specific restart behavior, not multi-zone resilience. One host outage can stop every capability even though its logical service/data boundaries remain separate.

## 3. Evaluate RDS as a proposed extension

Moving PostgreSQL to a managed relational service would require connectivity, credentials/rotation, TLS policy, backup/restore objectives, connection limits and migration planning. Multi-AZ failover and read replicas solve different problems; a replica is not automatically a writable replacement or a substitute for a restore drill. This source provisions neither. Preserve service ownership and prevent cross-database shortcuts during a move.

## 4. Evaluate managed Kafka or queues deliberately

A Kafka migration needs compatible client authentication/TLS, partition/group semantics, replay retention, offsets, monitoring and a cutover plan. Replacing Kafka with SQS/SNS/EventBridge is not a configuration rename: routing, replay, acknowledgment, ordering and delivery behavior must be redesigned. Keep stable business/event identity and consumer idempotency regardless of platform.

## 5. Make a database decision explainable

A document/key-value service such as DynamoDB is an extension exercise, not part of this Node AWS stack. Describe keys/access patterns, consistency, conditional writes and indexes before proposing it. Do not claim a cross-service atomic transaction between an external database, Kafka and PostgreSQL. The existing outbox makes durable intent visible precisely because that global transaction does not exist.

## Walk the real project

[infra/aws-dev/compose.yaml · lines 15–24](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/compose.yaml#L15-L24)

```yaml
    postgres: {condition: service_healthy}
    kafka: {condition: service_healthy}
  logging: {driver: json-file, options: {max-size: 10m, max-file: '3'}}
x-env: &env
  JWT_SECRET: ${JWT_SECRET:?required}
  INTERNAL_API_KEY: ${INTERNAL_API_KEY:?required}
  KAFKA_BROKERS: kafka:9092
  NODE_ENV: development
  SEED_DEMO: "true"
services:
```

[infra/aws-dev/compose.yaml · lines 56–62](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/compose.yaml#L56-L62)

```yaml
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_LOG_DIRS: /var/lib/kafka/data
      KAFKA_HEAP_OPTS: -Xmx512m -Xms256m
      CLUSTER_ID: MDEyMzQ1Njc4OWFiY2RlZg
    volumes: [kafka-data:/var/lib/kafka/data]
```

Read the real Kafka replication settings and volume paths. Then trace the inquiry transaction in the Node backend and its publisher. Application-level delivery guarantees must survive any managed-service redesign; a managed broker does not eliminate duplicate-delivery windows.

## Practice step by step

1. Draw which component owns accounts, providers, inquiries/outbox and notifications.
2. Build a decision table comparing current single-host setup, proposed managed PostgreSQL and proposed managed Kafka: failure domain, cost drivers, network/auth changes and recovery evidence.
3. Write a migration sequence: establish contracts/IDs → provision separately → test shadow/replay safely → cut over → reconcile → retire old path.
4. Pick one required restore test and one consumer replay test.

**Expected evidence:** A reasoned decision table and migration plan explicitly labeled as proposed, preserving current invariants.

## Check your understanding

### Does moving PostgreSQL to a managed service fix inquiry/Kafka atomicity?

No. Keep the transactional outbox and idempotent consumers; managed hosting changes operations, not that distributed commit boundary.

### Is a single Kafka broker equivalent to a multi-zone managed cluster?

No. Replication/failure domains and operational evidence differ. Name the actual settings instead of inferring resilience from the Kafka brand.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [AWS service overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)

- [RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
- [RDS read replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html)
- [Managed Streaming for Apache Kafka](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html)
- [DynamoDB data modeling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html)

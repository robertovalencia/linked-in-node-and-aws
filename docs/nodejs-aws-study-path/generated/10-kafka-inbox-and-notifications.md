---
title: KafkaJS, outbox publishing and deduplicated notifications
topic: Messaging
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# From committed inquiry to provider inbox

Prerequisite: 09. The event is inquiry.created.v1. Producer and consumer are separate runtime workers registered only for inquiries and notifications respectively. Kafka carries a fact; the notification UI later reads persisted inbox records through HTTP. This application does not implement email delivery, WebSockets or a separate inbox table.

## Publisher walkthrough

backend/src/common/messaging.ts constructs KafkaJS with configured brokers, timeouts, retry limits and optional TLS. OutboxPublisher starts an asynchronous loop, connects a producer and polls every 500 ms. publishBatch uses a DB transaction to select up to 25 unpublished rows in creation order with FOR UPDATE SKIP LOCKED. Each event is sent with key inquiry_id and acks:-1; after acknowledgement its published_at is updated. Other publishers can skip locked batches rather than duplicate that concurrent work.

The transaction holds locks while network publishing happens. That simplifies claiming rows but can hold connections/locks during broker delay. A proposed lease/claim design must preserve recovery when a publisher dies. Kafka acknowledgement configuration also depends on broker replication and in-sync replica settings; acks:-1 on a single local broker does not provide multi-zone durability.

## Consumer walkthrough

InquiryConsumer uses group marketplace-notifications-v1, subscribes with fromBeginning:true, and awaits NotificationsService.consume inside eachMessage. Existing committed group offsets determine normal restart position; fromBeginning is relevant when no valid offset exists. It does not replay every event on every restart.

consume validates eventSchema and inserts a notification using ON CONFLICT(event_id) DO NOTHING. The notification table's UNIQUE event_id is the deduplication record and effect in one statement. There is no distinct inbox-receipts table. Only after awaited processing can KafkaJS continue its acknowledgement/offset machinery. A replay following a crash therefore repeats the insert attempt safely for that identity.

## Crash table to explain aloud

| Failure boundary | Durable state | Recovery |
|---|---|---|
| Before inquiry/outbox commit | Neither new row committed | Client retries logical operation |
| After commit, before publish | Pending outbox | Publisher retries later |
| After Kafka ack, before published_at commit | Kafka may contain event; outbox still pending | Publish again; consumer deduplicates |
| After notification insert, before committed group offset | Inbox effect exists | Replay; unique event_id suppresses second effect |

This is at-least-once delivery with idempotent effects. It is not an exactly-once transaction across PostgreSQL and Kafka.

## Executable lab

With local dependencies running, read scripts/failure-drill.mjs before invoking node scripts/failure-drill.mjs. It intentionally manipulates the isolated local lab; record the actual stopped component, submitted inquiry, recovery, IDs and counts. Do not run it against shared or cloud infrastructure. Run focused backend coverage/workflow tests to inspect duplicate event behavior. Extend a test with a malformed event and confirm validation failure; a poison message needs an explicit production retry/quarantine policy. A dead-letter queue is proposed, not present.

## Debugging and senior tradeoffs

If inquiries exist but notifications do not, check pending outbox age, producer readiness/errors, topic configuration, consumer group state, schema failures and recipient filtering in order. Broker up does not imply consumer ready. WorkerHealth changes on worker connection events, but readiness is an operational signal with limits, not end-to-end delivery evidence. Partition ordering is per key/partition rather than global across topics or unrelated inquiries.



### Why use inquiry ID as the message key?

It groups one inquiry's messages for partition ordering, subject to topic partitioning behavior.

### Can a duplicate event cause another notification?

The same eventId is deduplicated; a producer wrongly issuing a new eventId for the same semantic fact is a different identity and requires a broader business invariant.

- [ ] Explain every crash boundary without saying exactly once.
- [ ] Locate deduplication in notifications SQL.
- [ ] Explain consumer groups, offsets, fromBeginning and message keys.
- [ ] Produce observed recovery evidence and identify a poison-event extension.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [KafkaJS consuming](https://kafka.js.org/docs/consuming) — accessed 2026-10-22.
- [producing](https://kafka.js.org/docs/producing) — accessed 2026-10-22.
- [Project source: backend/src/common/messaging.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/messaging.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/notifications/notifications.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/notifications/notifications.service.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/migrations/notifications.001.sql](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/migrations/notifications.001.sql) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/health.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/health.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: scripts/failure-drill.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/scripts/failure-drill.mjs) — local baseline inspected 2026-10-22; private published source may lag.

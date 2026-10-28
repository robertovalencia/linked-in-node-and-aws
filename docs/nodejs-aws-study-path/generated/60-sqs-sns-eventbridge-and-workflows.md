---
title: "SQS, SNS, EventBridge, and workflow orchestration"
topic: "SQS, SNS, EventBridge, and workflow orchestration"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 60 · SQS, SNS, EventBridge, and workflow orchestration

**Prerequisites:** 59; retries, idempotency, and event contracts.

[Previous: 59](59-msk-kafka-security-and-operations.md) · [Next: 61](61-lambda-apigateway-and-serverless-design.md) · [Study path](../README.md)

**Implementation boundary:** SQS, SNS, EventBridge, and Step Functions are absent from the current project. The application currently uses Kafka; the alternatives below are educational selection exercises.

A queue distributes work among competing consumers. Pub/sub sends an event to multiple independent subscribers. An event bus routes events to targets according to rules. A workflow coordinates steps with persisted progress and explicit failure behavior. Amazon SQS, SNS, EventBridge, and Step Functions address these different needs. Kafka retains an ordered partitioned log for replay; deleting a successfully processed queue message has a different lifecycle. Choosing a managed messaging service requires preserving the business contract, not just replacing a client library.

## 1. Choose the communication pattern before the service

Use a work queue when one worker should handle each work item, independent subscriptions when several systems need their own copy, routing rules when targets depend on event content, and orchestration when steps have explicit progression, waits, or compensation. A shared SQS queue does not give every consumer its own copy. SNS can fan out into separate queues so each subscriber controls backlog and retry behavior. EventBridge routing and Kafka replay solve overlapping but different requirements.

## 2. Design SQS processing for duplicates

A standard queue can deliver a message more than once. Receiving hides it for the visibility timeout; successful processing must be followed by deletion. A crash after committing an effect but before deletion causes a retry, so durable idempotency remains necessary. Visibility must fit processing behavior and renewal strategy. A dead-letter queue (DLQ) isolates repeatedly failing work for investigation; moving a message there does not repair its business operation or guarantee an operator sees it without monitoring.

## 3. Bound FIFO claims and parallelism

FIFO ordering is scoped to a message group, not a magical total business order across all groups. Deduplication has a documented finite interval and does not make arbitrary database effects exactly once. A worker can still repeat after a visibility timeout or crash. Group selection affects concurrency: one busy ordered group can serialize work even with many workers. Preserve event identity beyond the broker deduplication interval and keep a clear strategy for poison messages that would block later ordered work.

## 4. Secure fan-out and routing boundaries

Resource policies authorize service-to-service writes to queues or topics, while IAM governs callers. Constrain service principals to the intended source ARN/account where supported to avoid confused-deputy exposure. Configure target failure behavior and DLQ permissions deliberately; a DLQ reference alone may not authorize delivery. Routing filters are part of the contract: an event that fails a filter may never reach a consumer. Do not place credentials or sensitive payloads into broadly readable event histories or diagnostic logs.

## 5. Design workflow and batch failure semantics

Step Functions tracks state transitions and can express retry, catch, waits, and compensation, but retrying a task still needs idempotent effects. Lambda polls SQS through an event source mapping and may receive batches. A whole-batch failure can retry successful items; configured partial batch responses can identify only failed message IDs. FIFO handlers must preserve group ordering and report unprocessed items appropriately. Distinguish synchronous poller invocation behavior from asynchronous SNS-to-Lambda delivery rather than applying one retry model everywhere.

## Source or illustrative example

**New illustrative design:** SNS fans `inquiry.created` into separate notification and analytics queues. Each queue has an independent consumer, retry policy, and durable event-id check. Another proposal uses an explicit workflow for multi-step onboarding with compensation. Neither is implemented, and neither changes the current Kafka/outbox contract without migration and application work.

## Safe exercise

Run this local partial-batch response exercise:

```sh
node --input-type=module <<'JS'
const records = [{messageId:'a', ok:true}, {messageId:'b', ok:false}];
const response = {batchItemFailures: records.filter(x => !x.ok)
  .map(x => ({itemIdentifier:x.messageId}))};
console.log(JSON.stringify(response));
JS
```

Expected outcome: `{"batchItemFailures":[{"itemIdentifier":"b"}]}`. This models a standard-queue batch response, not a configured event source mapping. Explain why returning it without enabling the matching integration behavior is insufficient. Then draw where a crash can repeat item `a` despite a successful business write.

## Failure diagnosis

Growing visible backlog can mean insufficient consumers, slow processing, throttling, or an unavailable downstream dependency. Repeated invisible messages suggest long processing, crashes, or visibility misconfiguration. An empty target queue after publishing may mean filtering or resource-policy rejection, not producer success end to end. A workflow retry storm can amplify an outage; inspect retry limits, jitter where supported, and idempotency. DLQ growth requires diagnosis and safe redrive, not unconditional replay into the same defect.

## Recall and answers

### Does FIFO guarantee a database side effect occurs exactly once?

No. Deduplication and ordered delivery do not remove consumer crash windows.

### Why use separate queues behind fan-out?

Each subscriber gets independent progress, backlog, and failure handling instead of competing for one copy.

## Mastery check

Choose a pattern for work distribution, independent subscriptions, content routing, and multi-step compensation. Explain queue deletion versus stream retention and per-group FIFO ordering. Produce one duplicate-safe consumer timeline and one partial-batch failure example, with every service marked as proposed.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [SQS at-least-once delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html)
- [SNS overview](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [EventBridge overview](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [Step Functions overview](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Lambda SQS error handling](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html)
- [SQS FIFO deduplication](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)
- [SQS message groups](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html)

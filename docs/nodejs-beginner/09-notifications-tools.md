# Messaging tools: KafkaJS, offsets, Buffer and deduplication

Prerequisites: lessons 03, 07 and 09. Distinguish delivery of a message from the durable business effect.

[Service guide index](README.md). Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## KafkaJS client, producer and consumer

**What:** KafkaJS is a Node client library. A producer sends records; a consumer reads topic partitions as part of a consumer group.

**How:** The shared factory configures brokers, request/connect timeouts, retries and optional TLS. A client ID labels the client; a group ID coordinates consumer membership and offsets.

**Real code:** [backend/src/common/messaging.ts · lines 133–141](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L133-L141).

```ts
return new Kafka({
  clientId: `marketplace-${serviceName()}`,
  brokers: required('KAFKA_BROKERS')
    .split(',')
    .map((v) => v.trim()),
  logLevel: logLevel.ERROR,
  connectionTimeout: 5000,
  requestTimeout: 10000,
  retry: { retries: 4 },
```

**Watch for:** A broker bootstrap address must lead to reachable advertised broker addresses.

### Is clientId the same thing as groupId?

No. Client identity labels connections; consumer-group identity coordinates partition work.

## Message keys and acknowledgments

**What:** The record key affects partition routing. The producer acknowledgment setting controls which broker acknowledgment it waits for.

**How:** This producer uses the inquiry ID as key and acks=-1. It waits for in-sync replica acknowledgments, but one broker still has one-host failure risk.

**Real code:** [backend/src/common/messaging.ts · lines 31–35](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L31-L35).

```ts
await this.producer!.send({
  topic: process.env.KAFKA_TOPIC ?? INQUIRY_TOPIC,
  acks: -1,
  messages: [{ key: event.inquiry_id, value: JSON.stringify(event.payload) }],
});
```

**Watch for:** Acks do not create an atomic transaction with the PostgreSQL update.

### Does acks=-1 mean the event cannot be duplicated?

No. A crash after broker acknowledgment and before the outbox transaction commits can cause another send.

## SKIP LOCKED and bounded batches

**What:** `FOR UPDATE SKIP LOCKED` lets a worker skip rows another transaction already holds.

**How:** The publisher takes up to 25 pending records, sends them, then marks them published in one SQL transaction. Waiting on Kafka holds that client and its selected-row locks.

**Real code:** [backend/src/common/messaging.ts · lines 28–29](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L28-L29).

```ts
  'SELECT event_id,inquiry_id,payload FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 25 FOR UPDATE SKIP LOCKED',
);
```

**Watch for:** If a later send fails, the batch transaction can roll back earlier published markers; those sends may repeat.

### Why is batch size a resource control?

It bounds the work and locks held per transaction, though it does not bound every downstream delay.

## Consumer groups and starting offsets

**What:** A partition offset names a position in a Kafka log. Committed group offsets support resuming work.

**How:** `fromBeginning` applies when there is no usable committed offset. It does not rewind the group on every restart; successful handling and offset commits remain separate failure boundaries.

**Real code:** [backend/src/common/messaging.ts · lines 101–104](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L101-L104).

```ts
await this.consumer.subscribe({
  topic: process.env.KAFKA_TOPIC ?? INQUIRY_TOPIC,
  fromBeginning: true,
});
```

**Watch for:** Throwing on an invalid event can block progress for its partition; there is no implemented dead-letter policy here.

### What does fromBeginning=true actually promise?

It selects the beginning when the group has no applicable stored starting position.

## Buffer → UTF-8 → JSON → Zod

**What:** Kafka carries bytes. The consumer decodes text, parses JSON, then validates the resulting unknown value.

**How:** A malformed byte payload, invalid JSON document or schema mismatch can fail at a different stage. Zod checks event IDs, email and date shape before the database insert.

**Real code:** [backend/src/common/messaging.ts · lines 110–110](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L110-L110).

```ts
await this.notifications.consume(JSON.parse(message.value.toString('utf8')));
```

**Watch for:** Successful JSON.parse only proves valid JSON syntax, not a valid event contract.

### Why still call eventSchema.parse after JSON.parse?

A syntactically valid JSON value may have entirely wrong fields and types.

## Unique event IDs make duplicate effects harmless

**What:** Idempotent consumption means replaying one event does not create another business effect.

**How:** The notification INSERT has ON CONFLICT(event_id) DO NOTHING. The table’s unique event_id constraint makes the database decide atomically even with concurrent delivery.

**Real code:** [backend/src/notifications/notifications.service.ts · lines 30–31](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31).

```ts
'INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(event_id) DO NOTHING',
[
```

**Watch for:** There is no separate inbox receipt table; the notification row serves both content and deduplication.

### What if the process dies after INSERT but before offset commit?

Delivery may repeat, and the unique event ID prevents a second notification row.

## Timers, unref and detached promises

**What:** A timer schedules a future callback. `unref` lets the process exit if that timer is the only remaining activity.

**How:** `void this.run()` starts a promise-returning loop without awaiting it in the bootstrap hook. The loop needs its own rejection handling; void itself does not catch errors.

**Real code:** [backend/src/common/messaging.ts · lines 8–12](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L8-L12).

```ts
const pause = (ms: number) =>
  new Promise<void>((resolve) => {
    setTimeout(resolve, ms).unref();
  });

```

**Watch for:** A sleep, unref call or stopping flag is not complete cancellation of an already running network operation.

### Why can HTTP start while Kafka is still connecting?

The hook launches the worker loop without awaiting the entire loop’s lifetime.

## Instrumentation events update readiness

**What:** An event listener reacts to a KafkaJS runtime signal such as group join, crash or disconnect.

**How:** Listeners update WorkerHealth; shutdown sets a stopping flag and disconnects. Readiness is a recent signal, not proof that every event has reached every recipient.

**Real code:** [backend/src/common/messaging.ts · lines 90–99](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L90-L99).

```ts
this.consumer.on(this.consumer.events.CRASH, (event) => {
  this.health.ready = false;
  this.logger.error(`Consumer crash: ${event.payload.error.message}`);
});
this.consumer.on(this.consumer.events.GROUP_JOIN, () => {
  this.health.ready = true;
});
this.consumer.on(this.consumer.events.DISCONNECT, () => {
  this.health.ready = false;
});
```

**Watch for:** The current outer loop does not prove automatic recovery from every possible internal consumer crash.

### Does GROUP_JOIN mean the inbox is caught up?

No. It establishes membership, not that all records have been persisted.

## Practice and mastery

- Explain these identities separately: inquiry key, Kafka group ID, event ID, partition offset.
- Draw the two replay windows: broker ack → outbox commit, and notification commit → consumer offset commit.
- Use the notification workflow tests to inspect duplicate-event behavior. Explain why a mock does not prove real broker recovery.
- Predict the failure stage for `not JSON`, `{}` and a valid duplicate event: JSON parsing, Zod validation, then harmless unique conflict.
- Run the optional broker outage exercise only in the isolated local environment. The guide describes the experiment; it is not a claim that it has run.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [KafkaJS consuming](https://kafka.js.org/docs/consuming)
- [KafkaJS producing](https://kafka.js.org/docs/producing)
- [KafkaJS instrumentation](https://kafka.js.org/docs/instrumentation-events)
- [Project example: KafkaJS client, producer and consumer](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L133-L141)
- [Project example: Message keys and acknowledgments](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L31-L35)
- [Project example: SKIP LOCKED and bounded batches](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L28-L29)
- [Project example: Consumer groups and starting offsets](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L101-L104)
- [Project example: Buffer → UTF-8 → JSON → Zod](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L110-L110)
- [Project example: Unique event IDs make duplicate effects harmless](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31)
- [Project example: Timers, unref and detached promises](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L8-L12)
- [Project example: Instrumentation events update readiness](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L90-L99)

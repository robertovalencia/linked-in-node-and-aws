---
title: "Reliability concepts: timeouts, budgets, consistency and recovery"
topic: "Reliability concepts: timeouts, budgets, consistency and recovery"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Reliability concepts: timeouts, budgets, consistency and recovery

Prerequisites: the mechanisms in lessons 07–10 and 15. Explain a tradeoff using an exact implementation boundary.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## A timeout is one bounded wait

**What:** A timeout limits waiting for a particular operation. An end-to-end deadline covers the whole request’s budget.

**How:** The Catalog fetch has a five-second signal, but connection acquisition, lock waiting and later SQL have their own behavior. Adding retries without a budget can multiply load and latency.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 64–64](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L64-L64).

```ts
signal: AbortSignal.timeout(5000),
```

**Watch for:** Timeouts do not establish whether a remote write committed.

### Why does one timeout not define a complete request SLA?

The request contains other waits before and after that operation.

## Liveness versus readiness

**What:** Liveness asks whether a process can respond. Readiness asks whether its current dependencies/worker state permit useful traffic.

**How:** The ready handler queries PostgreSQL and checks WorkerHealth. Flags can lag real failure detection, and neither endpoint proves the complete distributed user journey.

**Real code:** [backend/src/common/health.ts · lines 19–23](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/health.ts#L19-L23).

```ts
  await this.db.query('SELECT 1');
  if (!this.worker.ready) throw new Error('Messaging worker not ready');
} catch {
  throw new ServiceUnavailableException('Database or messaging dependency unavailable');
}
```

**Watch for:** A static nginx health response does not validate all backend services.

### Can a process be live but not ready?

Yes. The handler can execute while its database or messaging dependency is unavailable.

## At-least-once delivery and idempotent effect

**What:** At-least-once transport permits repeated delivery. Idempotent handling prevents repetitions from creating another logical effect.

**How:** The outbox preserves intent; the notification unique event ID protects its effect. No atomic commit spans PostgreSQL and Kafka here.

**Real code:** [backend/src/notifications/notifications.service.ts · lines 30–31](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31).

```ts
'INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(event_id) DO NOTHING',
[
```

**Watch for:** Do not turn successful deduplication into a claim that Kafka never sent a duplicate.

### Which failure window requires consumer deduplication?

A durable notification write followed by a crash before the consumer offset commit.

## Shared build versus independent failure domains

**What:** Separate services can own different data and processes while still sharing host or build dependencies.

**How:** The SERVICE map registers different capabilities from one build. Local PostgreSQL and the AWS instance remain shared resource/failure domains.

**Real code:** [backend/src/main.ts · lines 30–35](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L30-L35).

```ts
const providers: Record<string, Type[]> = {
  identity: [IdentityService],
  catalog: [CatalogService],
  inquiries: [InquiriesService, OutboxPublisher],
  notifications: [NotificationsService, InquiryConsumer],
};
```

**Watch for:** Microservices do not automatically provide high availability.

### When might a modular monolith be simpler?

When operational cost and team size matter more than independent scaling or release boundaries.

## Concurrency protection versus stale-user conflict

**What:** A row lock prevents conflicting writes from interleaving on that row. Optimistic version checking detects that a client edited an outdated representation.

**How:** Catalog serializes updates and preserves protected fields, but there is no explicit profile version/ETag comparison. Two accepted full updates can still overwrite editable fields.

**Real code:** [backend/src/catalog/catalog.service.ts · lines 52–54](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L52-L54).

```ts
  'SELECT id,document FROM providers WHERE owner_email=$1 FOR UPDATE',
  [email],
);
```

**Watch for:** Serial execution is not the same as detecting a stale business decision.

### What would a version field add?

A condition that rejects a client update based on an older resource version.

## Practice and mastery

Choose one scenario and answer in five short steps: observed symptom, constrained resource, source evidence, proposed repair, verification.

- Catalog responds slowly: reason about transaction time, pool occupancy and lock waits before increasing max connections.
- Kafka accepts a send, then the publisher crashes: explain replay and the exact deduplication identity.
- An accepted profile update overwrites a user’s earlier change: distinguish a lock from an optimistic conflict policy.
- Design backup/restore and schema-compatible rollback as proposals; an old image alone does not restore data.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [PostgreSQL isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
- [AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [Project example: A timeout is one bounded wait](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L64-L64)
- [Project example: Liveness versus readiness](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/health.ts#L19-L23)
- [Project example: At-least-once delivery and idempotent effect](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31)
- [Project example: Shared build versus independent failure domains](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L30-L35)
- [Project example: Concurrency protection versus stale-user conflict](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L52-L54)

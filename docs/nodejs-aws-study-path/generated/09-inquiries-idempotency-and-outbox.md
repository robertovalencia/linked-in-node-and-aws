---
title: "Inquiries tools: fetch, hashes, UUIDs and transaction locks"
topic: "Inquiries tools: fetch, hashes, UUIDs and transaction locks"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Inquiries tools: fetch, hashes, UUIDs and transaction locks

Prerequisites: validation, promises and pg transactions. These tools coordinate one retryable write.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Native fetch and two failure channels

**What:** `fetch` resolves to a Response when an HTTP response arrives. An HTTP 404 is not normally a rejected fetch promise.

**How:** Network/abort failures go to catch. The service separately checks response.status/ok, then parses and validates the returned JSON.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 72–75](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L72-L75).

```ts
if (response.status === 404) throw new NotFoundException('Provider not found');
if (!response.ok) throw new ServiceUnavailableException('Catalog lookup failed');
try {
  return z
```

**Watch for:** A 200 response can still contain malformed or unexpected data.

### Why catch fetch and also check response.ok?

Transport failure and a received non-success HTTP response are different outcomes.

## AbortSignal.timeout and URL encoding

**What:** A timeout signal can abort a fetch. Encoding a path component prevents characters in an ID from becoming URL structure.

**How:** This lookup passes a five-second signal and a separate internal-authentication header. Timing out the client does not undo work the remote server may already have performed.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 61–65](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L61-L65).

```ts
`${required('CATALOG_URL').replace(/\/$/, '')}/internal/providers/${encodeURIComponent(id)}`,
{
  headers: { 'X-Internal-Key': required('INTERNAL_API_KEY') },
  signal: AbortSignal.timeout(5000),
},
```

**Watch for:** This timeout does not enforce a total deadline for every part of the whole inquiry operation.

### Why is the internal key not a browser JWT?

It authenticates a different server-to-server boundary and must stay out of browser code.

## SHA-256 fingerprint versus retry key

**What:** The retry key names one logical submission. The fingerprint detects whether the submission’s validated content changed.

**How:** The code serializes a fixed-order array of parsed fields, then hashes it. Field order is deliberate; hashing arbitrary JSON objects without a canonical policy can compare representations incorrectly.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 16–25](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L16-L25).

```ts
return createHash('sha256')
  .update(
    JSON.stringify([
      input.providerId,
      input.subject,
      input.message,
      input.budget,
      input.clientType,
    ]),
  )
```

**Watch for:** SHA-256 here is a change detector, not password storage or payload encryption.

### Same key but changed budget: what should happen?

The stored fingerprint differs and the service rejects the conflicting retry with 409.

## randomUUID: record identity is separate

**What:** A UUID supplies a generated identifier. The inquiry ID and event ID identify different things.

**How:** A new inquiry receives one ID and its announcement receives another. A replay returns the existing inquiry before generating either new identifier.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 105–107](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L105-L107).

```ts
const id = randomUUID();
const eventId = randomUUID();
const createdAt = new Date().toISOString();
```

**Watch for:** An unpredictable ID does not replace authorization or prove a request was not replayed.

### Why not use the event ID as the retry key?

Retry identity belongs to the client operation; the event is created later after a new operation is accepted.

## Advisory locking across async handlers

**What:** Two handlers can interleave whenever they await work. A JavaScript object or boolean cannot coordinate separate replicas.

**How:** The PostgreSQL lock serializes the client/key decision. After waiting, a second transaction checks the committed previous inquiry and either returns it or rejects changed content.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 91–99](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L91-L99).

```ts
// The transaction-scoped lock serializes the same client/key across every replica.
await client.query('SELECT pg_advisory_xact_lock(hashtextextended($1,0))', [
  JSON.stringify([actor.email, key]),
]);
const previous = await client.query(
  'SELECT * FROM inquiries WHERE client_email=$1 AND idempotency_key=$2',
  [actor.email, key],
);
if (previous.rows[0]) {
```

**Watch for:** The internal Catalog fetch happens while the transaction holds its connection and lock.

### Does await serialize all incoming requests?

No. It sequences one function’s continuation; the database lock coordinates this shared invariant.

## Outbox: one database transaction, two records

**What:** An outbox stores event intent beside the business write. Both records commit or roll back together.

**How:** The same checked-out client inserts the inquiry and event. Kafka publishing happens later; no transaction here spans both PostgreSQL and Kafka.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 135–140](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L135-L140).

```ts
await client.query('INSERT INTO outbox(event_id,inquiry_id,payload) VALUES($1,$2,$3)', [
  eventId,
  id,
  event,
]);
return inquiryView(inserted.rows[0]);
```

**Watch for:** A committed inquiry can exist before its notification is visible.

### What does HTTP success prove?

The handler’s database transaction committed, not that every downstream consumer already processed its event.

## Constraints and state transitions

**What:** A unique constraint is a database-enforced invariant. Application locks make the decision sequence orderly; constraints protect the stored result.

**How:** The migration makes client/key unique. Provider decisions separately lock the inquiry row and enforce allowed terminal-state behavior.

**Real code:** [backend/migrations/inquiries.001.sql · lines 6–7](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/migrations/inquiries.001.sql#L6-L7).

```sql
 idempotency_key text NOT NULL, request_hash text NOT NULL, UNIQUE (client_email,idempotency_key)
);
```

**Watch for:** Uniqueness, permitted status values and resource ownership are different checks.

### Why retain the constraint when the service already locks?

It remains a durable backstop if another code path or future implementation bypasses the expected sequence.

## Practice and mastery

- Draw three separate values: retry key, inquiry ID and event ID. State who creates each.
- Run the existing duplicate and changed-payload tests: `npm --prefix backend test -- --runTestsByPath test/workflows.spec.ts`.
- For a lost response, keep the original key and body. Explain why generating a new key can create another valid inquiry.
- For load reasoning, calculate how many of ten pool connections can be held by slow five-second Catalog calls.
- Optional live retry exercise: use the full local script in the beginner service guide; record observed results rather than assuming the lab ran.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Node fetch](https://nodejs.org/api/globals.html#fetch)
- [Node crypto](https://nodejs.org/api/crypto.html)
- [pg transactions](https://node-postgres.com/features/transactions)
- [Project example: Native fetch and two failure channels](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L72-L75)
- [Project example: AbortSignal.timeout and URL encoding](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L61-L65)
- [Project example: SHA-256 fingerprint versus retry key](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L16-L25)
- [Project example: randomUUID: record identity is separate](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L105-L107)
- [Project example: Advisory locking across async handlers](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L91-L99)
- [Project example: Outbox: one database transaction, two records](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L135-L140)
- [Project example: Constraints and state transitions](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/migrations/inquiries.001.sql#L6-L7)

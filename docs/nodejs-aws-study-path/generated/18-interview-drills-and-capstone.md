---
title: "Interview practice: explain the mechanism, then prove it"
topic: "Interview practice: explain the mechanism, then prove it"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Interview practice: explain the mechanism, then prove it

Prerequisites: lessons 01–17. Answer in 30 seconds, then give a source example and a failure case.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Explain a callback-to-promise adapter

**What:** Start with the API contract: callback(error, result) becomes a promise that rejects or resolves.

**How:** Use password.ts to explain promisify, awaited native work and the returned Buffer. Avoid replacing the mechanism with a general login workflow description.

**Real code:** [backend/src/identity/password.ts · lines 3–3](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L3-L3).

```ts
const scrypt = promisify(scryptCallback);
```

**Watch for:** Do not claim promisify creates a worker thread for any supplied function.

### What would a strong short answer say?

promisify adapts the error-first callback; Node’s async scrypt implementation supplies the native worker work.

## Explain a validated runtime boundary

**What:** State which data is untrusted, which schema checks it, and which type becomes available after parsing.

**How:** Use the search query schema to explain numeric coercion and the explicit true/false transform. Name the public error behavior for rejected data.

**Real code:** [backend/src/catalog/provider.schema.ts · lines 54–59](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L54-L59).

```ts
maxRate: z.coerce.number().int().min(0).max(1e6).optional(),
available: z
  .enum(['true', 'false'])
  .transform((v) => v === 'true')
  .optional(),
sort: z.enum(['recommended', 'rate-asc', 'rating']).default('recommended'),
```

**Watch for:** A compiler type or assertion does not establish a valid runtime object.

### Why is Boolean("false") a bad query parser?

It produces true because the text is nonempty; use a defined set of accepted strings.

## Explain a transaction without hand-waving

**What:** Name the checked-out client, the transaction boundary and the resource that must be released.

**How:** Then explain the specific lock and durable constraint. A useful answer separates function sequencing, database coordination and crash behavior.

**Real code:** [backend/src/common/database.ts · lines 70–76](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L70-L76).

```ts
const client = await this.pool.connect();
try {
  await client.query('BEGIN');
  const result = await operation(client);
  await client.query('COMMIT');
  return result;
} catch (error) {
```

**Watch for:** Do not use pool.query for one of the statements that must remain in the same transaction.

### What must be true for two inserts to commit atomically?

They must run in the same database transaction through the same client/session.

## Explain a duplicate message

**What:** Start at the exact crash boundary: a durable effect can exist before the broker offset commit.

**How:** Then identify the stable event ID and SQL unique conflict policy. Avoid promising exactly-once transport when the code supplies idempotent effects.

**Real code:** [backend/src/notifications/notifications.service.ts · lines 30–31](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31).

```ts
'INSERT INTO notifications(id,event_id,inquiry_id,recipient_email,message,created_at) VALUES($1,$2,$3,$4,$5,$6) ON CONFLICT(event_id) DO NOTHING',
[
```

**Watch for:** A new random notification candidate ID is not the deduplication identity.

### How can delivery repeat without creating another inbox row?

The repeated event carries the same event ID and the unique constraint makes its insert a no-op.

## Explain a stale React response

**What:** Describe which request owns the current result and when that ownership changes.

**How:** The effect’s cleanup aborts its request; the callback checks whether it was abandoned. Use the existing controlled-promise test to demonstrate the older result arriving last.

**Real code:** [frontend/src/hooks/useMarketplace.test.tsx · lines 12–15](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.test.tsx#L12-L15).

```tsx
it("ignores late search results after filters change even if transport ignores abort", async () => {
  let resolveFirst!: (value: Response) => void;
  vi.stubGlobal(
    "fetch",
```

**Watch for:** Do not use a slow-network anecdote as the only reproducible regression test.

### What evidence should accompany the explanation?

A deterministic test that fails when the stale-result guard is removed and passes when restored.

## Practice and mastery

**Capstone: a proposed minRate filter.** Use lesson 12’s vertical lab as the implementation scope.

1. Write acceptance examples before editing: absent filter preserves results; valid bounds filter correctly; inverted bounds return 400.
2. Change the runtime schema and parameterized SQL. Add focused negative and positive tests.
3. Wire a controlled React input through the query helper. Demonstrate loading, error, empty and success states.
4. Run checks, tests and build. Record actual outputs; keep AWS deployment as planned unless separately performed.
5. Explain each tool you touched: Zod, closures, pg parameters, React state, effects and HTTP errors.

- Pass when you can explain the code without reading the prose, reproduce one failure and defend one tradeoff.
- Give an honest narrative: distinguish prior experience, locally demonstrated skills and remaining gaps. Reading the pack does not establish senior production experience.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Project source repository](https://github.com/robertovalencia/linked-in-node-and-aws)
- [Project example: Explain a callback-to-promise adapter](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L3-L3)
- [Project example: Explain a validated runtime boundary](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L54-L59)
- [Project example: Explain a transaction without hand-waving](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L70-L76)
- [Project example: Explain a duplicate message](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31)
- [Project example: Explain a stale React response](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.test.tsx#L12-L15)

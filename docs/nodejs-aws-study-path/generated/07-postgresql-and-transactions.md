---
title: "pg tools: pools, transactions, locks and migrations"
topic: "pg tools: pools, transactions, locks and migrations"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# pg tools: pools, transactions, locks and migrations

Prerequisites: promises and SQL basics. The Database wrapper is shared by all four services.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Pool versus connection

**What:** `pg.Pool` manages reusable database connections. A connection is one PostgreSQL session.

**How:** The pool lends an idle connection, creates one up to max, or queues the request. Here max is 10 per process; four processes can request up to 40 connections.

**Real code:** [backend/src/common/database.ts · lines 10–14](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L10-L14).

```ts
readonly pool = new Pool({
  connectionString: required('DB_URL'),
  max: 10,
  connectionTimeoutMillis: 5000,
  ssl:
```

**Watch for:** Increasing pool size can overload PostgreSQL instead of fixing a slow dependency.

### Does every request create its own pool?

No. The injected Database provider owns a reusable pool in that service process.

## pool.query versus checked-out client

**What:** `pool.query` is convenient for one independent SQL statement. A checked-out client preserves one session across several statements.

**How:** A transaction must send BEGIN, every statement, and COMMIT/ROLLBACK through the same client. Another pool.query call may use another connection.

**Real code:** [backend/src/common/database.ts · lines 70–75](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L70-L75).

```ts
const client = await this.pool.connect();
try {
  await client.query('BEGIN');
  const result = await operation(client);
  await client.query('COMMIT');
  return result;
```

**Watch for:** A transaction callback does not make unrelated pool queries join its transaction.

### Where is transaction state stored?

On the PostgreSQL session represented by that checked-out client.

## try, catch and finally protect resources

**What:** `catch` handles a rejected awaited operation. `finally` runs on successful returns and on thrown errors.

**How:** The wrapper attempts ROLLBACK on failure and releases the client in finally. Releasing returns the connection to the pool; ending the pool belongs to shutdown.

**Real code:** [backend/src/common/database.ts · lines 76–82](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L76-L82).

```ts
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

**Watch for:** A failed ROLLBACK can itself throw; the current helper does not preserve every possible original-error detail.

### Why release after both success and failure?

Otherwise repeated requests can exhaust the pool even when the database is healthy.

## Parameters and result conversion

**What:** `query(sql, values)` sends values separately from SQL syntax. The result exposes rows and rowCount.

**How:** TypeScript’s row generic describes an expected shape. It does not decode or validate every returned value; this code explicitly converts numeric money and timestamps at its API boundary.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 48–51](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L48-L51).

```ts
budget: Number(row.budget),
clientType: row.client_type,
status: row.status,
createdAt: new Date(row.created_at).toISOString(),
```

**Watch for:** PostgreSQL numeric values may arrive as strings to avoid implicit precision loss.

### Does query<InquiryRow> validate each row?

No. The generic helps the compiler; runtime representation still needs deliberate handling.

## Row locks versus advisory locks

**What:** A row lock protects an existing row. An advisory lock coordinates an application-defined key, even before a row exists.

**How:** Inquiry creation derives a key from client email and retry key. The transaction-scoped advisory lock is released when the transaction ends; the unique constraint remains the durable invariant.

**Real code:** [backend/src/inquiries/inquiries.service.ts · lines 92–94](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L92-L94).

```ts
await client.query('SELECT pg_advisory_xact_lock(hashtextextended($1,0))', [
  JSON.stringify([actor.email, key]),
]);
```

**Watch for:** Hash collisions can serialize unrelated requests; they do not make different requests the same inquiry.

### Why is SELECT FOR UPDATE not enough before insertion?

There may be no existing row to lock for the new logical request.

## Migration checksums: filesystem plus crypto

**What:** A migration is a versioned SQL change. The runner lists service-specific files and computes a SHA-256 checksum.

**How:** An already-applied version must retain its checksum. `readFile` reads the small SQL file asynchronously; hashing detects edited history, not whether a migration is reversible.

**Real code:** [backend/src/common/database.ts · lines 46–50](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L46-L50).

```ts
const checksum = createHash('sha256').update(sql).digest('hex');
const applied = await client.query(
  'SELECT checksum FROM schema_migrations WHERE version=$1',
  [version],
);
```

**Watch for:** A filename change or checksum edit is not a safe way to rerun production migration history.

### How should the next schema change be made?

Add a new numbered migration and plan compatibility with old and new application versions.

## Pool events and TLS settings

**What:** An EventEmitter-style listener receives asynchronous pool errors. TLS can encrypt the database connection and authenticate its certificate.

**How:** The pool registers an error listener. When DB_SSL is enabled, it requires certificate verification and can use a configured CA; it does not silently disable verification.

**Real code:** [backend/src/common/database.ts · lines 17–20](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L17-L20).

```ts
    rejectUnauthorized: true,
    ...(process.env.DB_SSL_CA ? { ca: process.env.DB_SSL_CA } : {}),
  }
: undefined,
```

**Watch for:** TLS configuration, database credentials and SQL permissions are separate controls.

### Does a successful connection prove every later query is healthy?

No. Connections and dependencies can fail after startup.

## Practice and mastery

Use the existing local container credentials without printing them:

```bash
docker compose exec postgres sh -c 'PGPASSWORD="$CATALOG_DB_PASSWORD" psql -U catalog -d catalog'
```

In this local-only session, run `BEGIN; SELECT id FROM providers WHERE id='ava-martinez' FOR UPDATE;`.

Open a second session with the same command. Run the same BEGIN/SELECT; it should wait. Run `ROLLBACK;` in the first session, observe the second return, then `ROLLBACK;` there too.

- This reads and locks an existing seeded row; it does not alter provider data. Release both transactions promptly.
- Explain why two sessions cannot share a TEMP table.
- Draw which exact connection receives BEGIN, SELECT and ROLLBACK.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [pg pooling](https://node-postgres.com/features/pooling)
- [pg transactions](https://node-postgres.com/features/transactions)
- [PostgreSQL locks](https://www.postgresql.org/docs/current/explicit-locking.html)
- [Project example: Pool versus connection](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L10-L14)
- [Project example: pool.query versus checked-out client](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L70-L75)
- [Project example: try, catch and finally protect resources](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L76-L82)
- [Project example: Parameters and result conversion](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L48-L51)
- [Project example: Row locks versus advisory locks](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L92-L94)
- [Project example: Migration checksums: filesystem plus crypto](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L46-L50)
- [Project example: Pool events and TLS settings](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L17-L20)

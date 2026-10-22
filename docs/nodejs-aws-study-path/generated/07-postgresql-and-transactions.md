---
title: PostgreSQL, parameterized SQL, migrations and locks
topic: Persistence
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Durable data is a separate system

Prerequisites: 05–06. Each capability owns a database and login even though the local environment shares one PostgreSQL server. The pg library is a SQL driver; there is no Prisma, TypeORM or JPA layer here. Read backend/src/common/database.ts and backend/migrations/*.sql before drawing database relationships.

## Transaction mechanics

A pool manages reusable connections. Database.transaction checks out one client, begins a transaction, awaits the operation, commits on success, rolls back on failure and releases the client in finally. All transaction queries must use that same client. Calling pool.query between BEGIN and COMMIT can execute on another connection and break atomicity.

Inquiries and outbox are written in one transaction. If the outbox insert fails, the inquiry insert rolls back. That prevents a committed inquiry without a recorded notification intent. It does not atomically commit PostgreSQL and Kafka; lesson 09 explains that separate boundary.

Parameterized queries send values separately: WHERE email=$1 with [email]. Concatenating user input into the SQL string is unsafe. Placeholders cannot choose arbitrary table names or ORDER BY expressions; catalog constructs ordering from a fixed allowlist and parameters for values. The catalog stores profile data in JSONB while keeping id and owner_email relational. That enables flexible documents, but runtime/schema constraints and indexing still matter.

## Migrations and startup

Database selects migration files named for SERVICE, sorts them, takes a transaction-scoped advisory migration lock, creates schema_migrations if needed and records SHA-256 checksums. A previously applied file with changed contents triggers an error. Add a new numbered migration rather than editing an executed one. Startup migration is convenient locally; production deployments need a deliberate compatibility and concurrency strategy.

## Safe SQL lab

Use the isolated local catalog database after npm run up. From the repository root, this command opens psql inside the PostgreSQL container using the catalog service's existing password environment variable without displaying it:

~~~bash
docker compose -p linked-in-node-local exec postgres sh -c 'PGPASSWORD="$CATALOG_DB_PASSWORD" exec psql -h 127.0.0.1 -U catalog -d catalog'
~~~

Expect a catalog=> prompt. The following transaction uses only a temporary lesson table and ends with ROLLBACK, so no provider data is changed. Never use a production connection. If Compose reports a missing variable, first complete npm run setup from the root rather than pasting a password. Execute:

~~~sql
BEGIN;
CREATE TEMP TABLE lesson_accounts(id int PRIMARY KEY, balance numeric NOT NULL);
INSERT INTO lesson_accounts VALUES (1,100), (2,50);
SAVEPOINT before_transfer;
UPDATE lesson_accounts SET balance=balance-10 WHERE id=1;
UPDATE lesson_accounts SET balance=balance+10 WHERE id=2;
SELECT sum(balance) FROM lesson_accounts;
ROLLBACK TO SAVEPOINT before_transfer;
SELECT * FROM lesson_accounts ORDER BY id;
ROLLBACK;
~~~

Expect sum 150, then restored balances 100/50, then no lasting lesson table. Temporary tables are session-local, so do not use that temporary row for the next two-session experiment.

For a brief no-write lock demonstration in this isolated seeded catalog, open two terminals and run the same psql connection command in each. In session A execute:

~~~sql
BEGIN;
SELECT id FROM providers WHERE id='ava-martinez' FOR UPDATE;
~~~

Expect the seeded ID immediately. Leave that transaction open only for this short lab. In session B execute the same BEGIN and SELECT. Expect its SELECT to wait because A holds the row lock. Return to session A and execute ROLLBACK; session B then returns the ID. In B execute ROLLBACK too, then exit both clients with \q. No profile data was updated, but while the lock is held it can delay concurrent updates to that demo provider, so never use this experiment in a shared or production environment. If the seed ID is absent, complete the local demo setup rather than creating arbitrary production rows. A unit-test fake cannot prove that lock behavior.

For the actual catalog, use EXPLAIN on a representative search in the disposable environment. Explain rows scanned, sorting and expected index usefulness; do not add indexes based only on table size guesses. For latency evidence, EXPLAIN ANALYZE executes the statement, so apply it only to safe reads or deliberate disposable experiments.

## Debugging and senior tradeoffs

A ten-client pool can be exhausted by unreleased clients or long transactions. Inspect waiters, active queries, transaction age and downstream waits. The current inquiry transaction awaits catalog while holding a client and advisory lock; its bounded timeout trades simplicity for capacity. Offset pagination can degrade at deep pages; a cursor is an extension with a different contract. Numeric money values can require explicit string-to-number conversion; avoid silently losing precision when scale grows.



### Why both a lock and a unique constraint?

The lock serializes decision logic for a logical key across replicas; uniqueness remains a durable final invariant.

### Does sharing a database server violate service ownership?

Distinct databases/logins preserve ownership, but still share an outage and resource domain.

- [ ] Demonstrate rollback and one-connection transaction semantics.
- [ ] Explain parameter values versus allowlisted SQL structure.
- [ ] Find schema constraints, partial indexes and migration checksums.
- [ ] Diagnose a pool wait without blindly increasing max connections.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [node-postgres transactions](https://node-postgres.com/features/transactions) — accessed 2026-10-22.
- [PostgreSQL locking](https://www.postgresql.org/docs/current/explicit-locking.html) — accessed 2026-10-22.
- [Project source: backend/src/common/database.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/database.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/migrations/inquiries.001.sql](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/migrations/inquiries.001.sql) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/migrations/catalog.001.sql](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/migrations/catalog.001.sql) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/catalog/catalog.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/catalog/catalog.service.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/postgres/init-databases.sh](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/infra/postgres/init-databases.sh) — local baseline inspected 2026-10-22; private published source may lag.

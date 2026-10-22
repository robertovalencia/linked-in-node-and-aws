# 1. How the services start and get wired together

[Guide index](README.md) · [Next: the four services](02-four-services.md)

## A process is a running program

Node.js executes JavaScript outside the browser. TypeScript adds checks while developing; the compiler emits JavaScript for Node to execute. NestJS is the framework that connects HTTP routes, classes, and dependencies. PostgreSQL stores durable data. Kafka transports events. None of these names means the same thing as the others.

The repository builds **one backend image**, then runs it four times. Compare [backend/Dockerfile](../../backend/Dockerfile) with [compose.yaml](../../compose.yaml). Every backend container executes `node dist/main.js`. Its `SERVICE` value tells `bootstrap` which business capability to register. Each process has its own heap, dependency instances, port, and database pool. Sharing an image does not share memory or turn the services into one process.

| `SERVICE` | HTTP port | Registered business controller | Registered business providers |
|---|---:|---|---|
| `identity` | 8181 | `IdentityController` | `IdentityService` |
| `catalog` | 8182 | `CatalogController` | `CatalogService` |
| `inquiries` | 8183 | `InquiriesController` | `InquiriesService`, `OutboxPublisher` |
| `notifications` | 8184 | `NotificationsController` | `NotificationsService`, `InquiryConsumer` |

Each selection also gets `HealthController`, `Database`, `AuthGuard`, and `WorkerHealth`. These maps are in [main.ts](../../backend/src/main.ts), not four separate application module files. Importing a class into a file does not register it as an active Nest provider in every application. The `@Module` metadata determines that registration.

```text
shared source -> TypeScript compiler -> shared image
                                      |- SERVICE=identity      -> process A -> identity DB
                                      |- SERVICE=catalog       -> process B -> catalog DB
                                      |- SERVICE=inquiries     -> process C -> inquiries DB
                                      `- SERVICE=notifications -> process D -> notifications DB
```

## Follow startup, one step at a time

Open [main.ts: bootstrap](../../backend/src/main.ts), [config.ts: validateConfig](../../backend/src/common/config.ts), and [database.ts: Database](../../backend/src/common/database.ts) together.

1. `reflect-metadata` is imported before Nest uses decorator metadata. The compiler options `experimentalDecorators` and `emitDecoratorMetadata` in [tsconfig.json](../../backend/tsconfig.json) support constructor injection.
2. `validateConfig()` fails early if `SERVICE` is unknown, JWT secret is too short, or the database URL is not PostgreSQL. Catalog and Inquiries also need an internal key of at least 32 characters. Inquiries needs an HTTP(S) Catalog URL. Inquiries and Notifications need broker addresses. This validation checks shape/presence; it does not prove those remote services are reachable.
3. `serviceName()` selects the controller/provider entries. `ApplicationModule` is declared inside `bootstrap` with this metadata.
4. `NestFactory.create` creates the dependency graph. When a controller asks for a service and the service asks for `Database`, Nest supplies the registered objects. Constructors do not manually call `new Database()`.
5. Express's default body parser is disabled. The application installs Helmet headers and its own JSON parser with a `128kb` limit. `ErrorFilter` converts errors to `{status, detail}`; unhandled internal errors become a generic 500 response while the server logs the stack. A malformed JSON request can become 400; an oversized request can become 413.
6. `enableShutdownHooks()` lets Nest call shutdown hooks for process signals. The DB pool and Kafka objects have cleanup hooks. Graceful shutdown reduces abandoned work; it does not remove the need for crash-safe persistence.
7. During application initialization triggered by `listen`, `Database.onModuleInit()` reads only migrations prefixed with the selected service name, sorts them, and executes unapplied files. It stores SHA-256 checksums in `schema_migrations`. An already-applied file with different content aborts initialization: add a new migration rather than editing history.
8. Nest calls `onApplicationBootstrap()` after module initialization. Identity prepares a dummy password hash and optionally seeds accounts; Catalog optionally seeds profiles. Their async bootstrap hooks are awaited. Messaging hooks launch a background `run()` with `void`, so the web server can finish starting while broker work is still connecting.
9. `listen` binds the validated port on `0.0.0.0` inside the process. Local Compose publishes that port only on host loopback. A bootstrap rejection is logged and sets exit status 1.

The distinction between steps 7 and 8 explains why seeds can rely on migration-created tables. Do not generalize this into “any two providers' `onModuleInit` hooks always run in the order I list them.” The reliable boundary here is module initialization before application bootstrap. Nest documents that lifecycle and awaits returned initialization promises in its [lifecycle guide](https://docs.nestjs.com/fundamentals/lifecycle-events).

## Dependency injection in plain language

Read this signature in [InquiriesService](../../backend/src/inquiries/inquiries.service.ts):

```ts
constructor(private readonly db: Database) {}
```

`constructor` runs when Nest creates the service. `db` becomes a field on the object because TypeScript supports constructor parameter properties. `private` means other TypeScript code should not use the field directly. `readonly` prevents reassignment of that field; it does not make the database immutable. The `Database` type plus emitted metadata tells Nest which dependency to supply.

Think of Nest as an assembly table: it creates a database adapter, hands that adapter to the inquiry service, then hands the inquiry service to the controller. The dependency graph is `InquiriesController -> InquiriesService -> Database`. `OutboxPublisher -> Database + WorkerHealth` is a separate branch. Nest does the wiring; your service still owns the business rule. The guard does not magically know which provider owns a particular row.

In a unit test you can supply a fake database object to isolate the rule. This helps test 403 or 409 behavior quickly. A fake cannot prove PostgreSQL transaction locks or broker delivery; those require integration evidence.

## Configuration: different addresses from different places

| Setting | Why it exists | Where to inspect its assembly |
|---|---|---|
| `SERVICE`, `PORT` | Select capability and listener | [Compose](../../compose.yaml), [dev launcher](../../scripts/dev.mjs) |
| `DB_URL` | Service-owned database/user | Same files; [database initializer](../../infra/postgres/init-databases.sh) creates the roles/databases |
| `JWT_SECRET` | Signs/verifies laboratory HS256 tokens | [auth.ts](../../backend/src/common/auth.ts) |
| `INTERNAL_API_KEY` | Protects Catalog's private owner lookup | [CatalogController.internal](../../backend/src/catalog/catalog.controller.ts) |
| `CATALOG_URL` | Inquiries' HTTP destination | [InquiriesService.provider](../../backend/src/inquiries/inquiries.service.ts) |
| `KAFKA_BROKERS`, optional `KAFKA_TOPIC` | Broker destinations/topic | [messaging.ts: kafka](../../backend/src/common/messaging.ts) |
| `SEED_DEMO` | Opts into synthetic data seeding | Identity/Catalog bootstrap hooks |
| `DB_SSL`, `DB_SSL_CA`, `KAFKA_SSL` | Optional TLS client settings | [Database.pool](../../backend/src/common/database.ts), `kafka()` |

Inside Compose, `postgres:5432`, `catalog:8182`, and `kafka:9092` use container network DNS names. From your laptop, the database is `127.0.0.1:55432` and Kafka is `127.0.0.1:19092`. `localhost` inside an API container means that API container, not the PostgreSQL container. Kafka advertises addresses to clients; picking the correct bootstrap address alone is insufficient if the advertised address is unreachable.

[setup-local.sh](../../scripts/setup-local.sh) creates an independent `.env` with random local secrets only if one does not exist. It uses restrictive permissions and preserves existing credentials. Do not copy it into a document or output the entire environment while troubleshooting. Secrets in `.env` are inputs, not learning content.

The PostgreSQL initialization script creates four databases and four login roles and revokes public connect permissions on those databases. These are boundaries inside one server, not four independent PostgreSQL servers. One server outage still affects all four. Initialization scripts run when a fresh PostgreSQL volume is initialized, not on every restart. Changing a password in `.env` alone does not change an existing database user's password.

## What a transaction really does

In [Database.transaction](../../backend/src/common/database.ts), the pool lends one `PoolClient`. The wrapper issues `BEGIN`, awaits your callback, issues `COMMIT`, and releases the connection in `finally`. If the callback throws, it attempts `ROLLBACK` and rethrows.

```ts
// Illustrative shape; read the real helper and callers in source.
await db.transaction(async (client) => {
  await client.query('INSERT ...', values);
  await client.query('INSERT ...', otherValues);
});
```

Every statement in that transaction must use the **same `client`**. Calling `db.query` inside the callback would ask the pool for an arbitrary connection and would not safely participate in that transaction. This is a constraint of PostgreSQL connections, explained in the [node-postgres transaction documentation](https://node-postgres.com/features/transactions).

The migration runner uses a transaction-scoped advisory lock to coordinate migration startup. Inquiry creation uses another transaction-scoped advisory lock derived from client email/key. Profile and status changes use `FOR UPDATE` row locks. These are different locks for different invariants; `await` itself is not a lock.

The pool is limited to 10 connections **per process**. Four processes can create up to 40 connections. More replicas multiply that count. A connection held during a slow HTTP call or Kafka publish cannot serve another request. This project intentionally makes that tradeoff visible: inquiry creation performs Catalog HTTP inside its transaction, and the publisher waits for Kafka while holding its batch transaction.

### Two requests arriving together

Imagine requests A and B carry the same verified client and the same key. A reaches `await client.query(...)`; Node can start processing B while A waits for PostgreSQL. Both functions exist at once. A acquires the transaction-scoped advisory lock for that client/key; B waits for that same lock. A finds no prior row, performs the Catalog lookup, inserts one inquiry plus one outbox event, and commits. Its commit releases the lock. B then acquires it, reads the already-committed inquiry, and returns its original ID when the parsed fingerprint matches. With changed content, B instead gets 409. The database's unique client/key constraint is a backstop. There is one logical event row, even though the publisher may later send that event more than once.

[Lab 2](04-debugging-and-practice.md#lab-2-safe-retry-conflict-and-authorization) issues both calls with `Promise.all` and checks same ID plus one inquiry, one logical outbox event, and one inbox effect. That exercise records your observed run; the lock and unique constraint explain why the invariant is designed to hold beyond a single JavaScript process. `await` schedules the work; PostgreSQL coordinates the competing transactions.

## Health is more precise than “it started”

Read [HealthController](../../backend/src/common/health.ts).

| Endpoint/condition | What it establishes | What it does not establish |
|---|---|---|
| `/health/live` returns UP | Process can serve this handler | Database or Kafka is healthy |
| `/health/ready` executes `SELECT 1` | This database is queryable at that moment | Every query will succeed under load |
| Inquiries worker flag true | Publisher connected and completed a batch iteration | Backlog is empty forever; no later disconnect |
| Notifications worker flag true | Consumer joined its group | All messages are processed; no later poison event |
| Frontend `/health` | nginx serves its own simple health response | All downstream services are ready |

Identity and Catalog start with a true messaging flag because they have no Kafka worker. Inquiries/Notifications start false. Publisher errors, consumer disconnects, and consumer crash events lower the relevant flag. These are useful signals, not a continuous distributed health proof. In particular a true flag can be stale between a failure and detection, and readiness is not enforced as a per-request authorization gate. A running Inquiries handler can still persist an outbox during a broker outage if Catalog and PostgreSQL are available.

## Build and development are different paths

[backend/package.json](../../backend/package.json) pins the repository's Nest packages and declares Node `>=22 <25`; [Dockerfile](../../backend/Dockerfile) uses Node `22.22.0-alpine`. These are this project's baseline, not a claim about the newest or best version today. `npm ci` installs according to the lockfile. `tsc` emits `dist` JavaScript. `type: module` and `NodeNext` explain imports ending in `.js` even in `.ts` source: those are runtime output paths. `sourceMap: true` supports mapping compiled code back to TypeScript in a debugger.

The container build compiles, prunes development dependencies, then copies compiled output, runtime dependencies, migrations, and seeds into a second stage run as user `node`. It still needs migration files at runtime. In host development, [backend/scripts/dev.mjs](../../backend/scripts/dev.mjs) compiles into `dist-dev/<service>`, runs TypeScript watch, and runs Node watch with a loopback inspector port. [scripts/dev.mjs](../../scripts/dev.mjs) launches all four processes plus Vite and propagates shutdown signals.

**Checkpoint:** without running anything, point to where a missing secret fails, where a changed migration fails, where the database object is injected, and why Notifications may be live before it is ready.

# NestJS, contracts, security, databases and events

[Questionnaire and routes](node-backend-questionnaire.md) · [Acronym glossary](node-backend-questionnaire.md#acronyms-at-a-glance) · [Source excerpts](evidence/node-backend-source-context.md) · [Runtime lab](labs/node-runtime/README.md)

<a id="ns01"></a>

### NS01 · What do Nest decorators and modules do?

**Priority:** start now. **Implementation:** Current source.

Decorators attach information to classes and methods; Nest reads it to find routes and providers. The module registers which objects belong in this application. Here SERVICE selects one capability before Nest starts. Importing a class alone does not register it, and @Injectable does not itself open a database connection.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-ns01) · symbol: `@Module({`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/fundamentals/custom-providers) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/providers).

<a id="ns02"></a>

### NS02 · How does dependency injection supply a service?

**Priority:** start now. **Implementation:** Current source.

Dependency injection means Nest supplies required objects through a constructor. Database is registered as a provider, so CatalogService receives it. The default instance is shared inside one application context; another process has another instance. Interfaces disappear after compilation, so an interface needs a runtime injection token. private readonly stores the argument and prevents rebinding; the referenced pool remains mutable.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-ns02) · symbol: `constructor(private readonly db: Database)`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/providers) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/fundamentals/custom-providers).

<a id="ns03"></a>

### NS03 · What belongs in a controller versus a service?

**Priority:** start now. **Implementation:** Current source.

A controller translates a Hypertext Transfer Protocol (HTTP) request into a service call: it reads route parameters, headers and input. A service performs the business decision and database work. Catalog declares /me before /:id so the named route is not swallowed by a dynamic identifier. Keep ownership checks in the execution path even if the page already hides a button.

**Project:** [backend/src/catalog/catalog.controller.ts](evidence/node-backend-source-context.md#source-ns03) · symbol: `@Get('api/providers/me')`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/controllers).

<a id="ns04"></a>

### NS04 · When is asynchronous startup finished?

**Priority:** start now. **Implementation:** Current source.

Nest can await a Promise returned from an initialization hook. Database migrations complete in onModuleInit; Identity awaits a dummy password hash in onApplicationBootstrap. A detached background loop such as void this.run() does not delay startup until Kafka connects. Do not assume unrelated providers initialize in their array order; express required dependencies explicitly.

**Project:** [backend/src/identity/identity.service.ts](evidence/node-backend-source-context.md#source-ns04) · symbol: `async onApplicationBootstrap()`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/fundamentals/lifecycle-events).

<a id="ns05"></a>

### NS05 · Are Helmet, body parsing and validation interchangeable?

**Priority:** start now. **Implementation:** Current source.

No. Helmet adds security response headers. The JSON parser turns request bytes into a JavaScript value and rejects bodies beyond 128kb. Zod checks the resulting fields. JavaScript Object Notation (JSON) that parses successfully can still contain an invalid budget or unexpected fields. Here parsing is configured explicitly with Nest bodyParser disabled to avoid competing parser limits.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-ns05) · symbol: `app.use(json({ limit: '128kb' }));`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [helmet.js.org · reference 1](https://helmet.js.org/) · [expressjs.com · reference 2](https://expressjs.com/en/api/).

<a id="ns06"></a>

### NS06 · How do guards and exception filters differ?

**Priority:** start now. **Implementation:** Current source.

A guard allows or rejects entry to a route; AuthGuard verifies a token and attaches the actor. A filter turns thrown failures into HTTP responses. ErrorFilter maps schema failures to 400, preserves known HTTP statuses and hides unexpected 500 details. Passing a guard establishes an identity; the service must still check ownership of the requested row.

**Project:** [backend/src/common/errors.ts](evidence/node-backend-source-context.md#source-ns06) · symbol: `error instanceof ZodError`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/guards) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/exception-filters).

<a id="ns07"></a>

### NS07 · Does installing RxJS make these services reactive?

**Priority:** next. **Implementation:** Absent implementation.

RxJS, Reactive Extensions for JavaScript, offers Observables: subscriptions can receive multiple values and can be cancelled. This backend installs RxJS for Nest but its application services use Promises and KafkaJS callbacks. It has no custom Observable pipeline. Describe the mechanism actually present before proposing reactive operators.

**External worked example (not installed here):** In an isolated RxJS example, subscribe to the documented Observable that emits 1, 2 and 3 synchronously, then 4 after a delay and completes. Record the values in order and unsubscribe from a continuing source to stop future emissions. This is an extension, not a marketplace pipeline. [Official example](https://github.com/ReactiveX/rxjs/blob/master/apps/rxjs.dev/content/guide/observable.md).

**Project:** [backend/package.json](evidence/node-backend-source-context.md#source-ns07) · symbol: `"rxjs"`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md).

**Lesson relationship:** Lesson05 teaches that RxJS is installed without custom application Observable pipelines. The external subscription example is a worked extension, not an implemented marketplace feature.

**Official documentation:** [github.com · reference 1](https://github.com/ReactiveX/rxjs/blob/master/apps/rxjs.dev/content/guide/observable.md).

<a id="ns08"></a>

### NS08 · Why validate input when TypeScript already has types?

**Priority:** start now. **Implementation:** Current source.

TypeScript checks code before it runs; incoming requests have no trustworthy TypeScript type. Zod parse validates an unknown value at runtime, returns the accepted value or throws. Here an invalid inquiry budget becomes 400 before persistence. A type assertion such as body as CreateInquiry only tells the compiler to trust you; it does not inspect the request.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns08) · symbol: `const input = inquirySchema.parse(body);`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md) · [08 · identity jwt and security](generated/08-identity-jwt-and-security.md) · [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [zod.dev · reference 1](https://zod.dev/basics).

<a id="ns09"></a>

### NS09 · How do coercion, transforms and defaults affect query parameters?

**Priority:** start now. **Implementation:** Current source.

Query parameters arrive as text. Catalog converts maxRate to a bounded integer, transforms only the strings true and false into booleans, and defaults a missing sort to recommended. Boolean("false") is true because nonempty text is truthy, so arbitrary Boolean coercion would be wrong. Check undefined explicitly so a supplied zero or false is not discarded.

**Project:** [backend/src/catalog/provider.schema.ts](evidence/node-backend-source-context.md#source-ns09) · symbol: `.enum(['true', 'false'])`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [zod.dev · reference 1](https://zod.dev/api).

<a id="ns10"></a>

### NS10 · What do strict schemas and inferred types guarantee?

**Priority:** start now. **Implementation:** Current source.

A strict object schema rejects unknown keys; each field separately decides whether it is required, optional or defaulted. Nested objects need their own strictness. z.infer derives a compile-time type from the schema but does not run validation. A valid Provider object still needs an ownership check before an update.

**Project:** [backend/src/catalog/provider.schema.ts](evidence/node-backend-source-context.md#source-ns10) · symbol: `export type Provider = z.infer<typeof providerSchema>;`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [zod.dev · reference 1](https://zod.dev/api).

<a id="ns11"></a>

### NS11 · How are SQL injection and wildcard surprises prevented?

**Priority:** start now. **Implementation:** Current source.

Structured Query Language (SQL) values travel separately from query text as $1, $2 and later parameters. Catalog’s add closure captures the values array and supplies the next position. Parameters cannot stand for column names or sort expressions; use fixed allowlisted branches. Escape percent and underscore separately when search should treat them literally: parameters alone do not remove LIKE wildcard meaning.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-ns11) · symbol: `const add = (value: unknown) => {`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md) · [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/queries) · [www.postgresql.org · reference 2](https://www.postgresql.org/docs/current/functions-matching.html).

<a id="ns12"></a>

### NS12 · How does PostgreSQL JSONB differ from a JavaScript object?

**Priority:** start now. **Implementation:** Current source.

JSONB is PostgreSQL’s binary JSON storage, queried inside the database. The -> operator returns JSON and ->> extracts text. Catalog casts hourlyRate text to numeric before comparison and sorting; text ordering would put 100 before 20. An array predicate uses jsonb_array_elements_text for skills. Validate stored documents and consider measured indexes when the dataset grows.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-ns12) · symbol: `(document->>'hourlyRate')::numeric`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/functions-json.html).

<a id="ns13"></a>

### NS13 · How does this catalog paginate consistently?

**Priority:** next. **Implementation:** Current source.

The schema bounds page and size; SQL applies LIMIT and OFFSET after a deterministic sort with id as a tie breaker. A common table expression filters once for both total and page items. It can return an empty items array and a nonzero total for an out-of-range page. Large offsets still scan work; cursor pagination is a design extension, not implemented here.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-ns13) · symbol: `WITH filtered AS`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/18/sql-select.html).

<a id="ns14"></a>

### NS14 · Why preserve server-owned fields during a profile update?

**Priority:** start now. **Implementation:** Current source.

A client must not award itself a rating. Catalog locks the owner’s row, checks that the submitted profile ID matches, then puts stored rating, reviewCount and completedProjects after the submitted fields. Later object properties override earlier ones. This preserves protected values while accepting validated edits; neither schema validity nor a lock alone supplies that business policy.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-ns14) · symbol: `rating: row.document.rating,`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/explicit-locking.html).

<a id="ns15"></a>

### NS15 · What is a connection pool, and how big is this one?

**Priority:** start now. **Implementation:** Current source.

A pool reuses database sessions rather than establishing one for every query. This pool allows ten connections per process and waits up to five seconds for connection acquisition. Four service processes can use forty, before extra replicas or operations. Raising max can move overload into PostgreSQL; first measure active, idle and waiting work and shorten slow transactions.

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-ns15) · symbol: `max: 10,`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/pooling) · [node-postgres.com · reference 2](https://node-postgres.com/apis/pool).

<a id="ns16"></a>

### NS16 · Why must a transaction keep the same database client?

**Priority:** start now. **Implementation:** Current source.

BEGIN, statements and COMMIT must run on one checked-out client because a transaction belongs to that database session. Separate pool.query calls can use different sessions. The wrapper rolls back on failure and releases the client in finally on every path. Releasing without rollback can leave a bad transaction for the next borrower; forgetting release can exhaust the pool.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-ns16) · symbol: `const client = await this.pool.connect();`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/transactions).

<a id="ns17"></a>

### NS17 · Are database row types automatically the API types?

**Priority:** start now. **Implementation:** Current source.

No. A database numeric value may arrive as text, and timestamps may arrive as Date objects. inquiryView deliberately converts budget with Number and createdAt to an International Organization for Standardization (ISO) timestamp string. For larger financial precision, use an exact decimal or minor-unit contract rather than assuming every SQL number fits a JavaScript Number. A generic row annotation alone validates nothing.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns17) · symbol: `budget: Number(row.budget),`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md) · [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/types).

<a id="ns18"></a>

### NS18 · When should a row lock or an advisory lock be used?

**Priority:** start now. **Implementation:** Current source.

A row lock protects an existing row during a transaction; Catalog uses FOR UPDATE while editing an owned profile. An advisory lock protects an application-defined decision, even before the inquiry row exists. Inquiries hashes the client/key pair into a transaction-scoped lock shared across replicas. Keep database unique constraints too; they enforce the invariant even if another write path omits the lock.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns18) · symbol: `SELECT pg_advisory_xact_lock(hashtextextended($1,0))`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md) · [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/explicit-locking.html).

<a id="ns19"></a>

### NS19 · Does a transaction imply serializable isolation?

**Priority:** next. **Implementation:** Current source.

No. PostgreSQL normally uses Read Committed unless configured otherwise; this wrapper issues BEGIN without selecting a stronger level. Each statement can see a newer committed snapshot. Explicit locks and constraints protect specific decisions here. Serializable transactions can reject conflicting work and require retrying the entire transaction; they are not a free switch that removes every application policy.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-ns19) · symbol: `await client.query('BEGIN');`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** Lessons07/16 provide transaction and concurrency prerequisites. The explicit isolation-level comparison is a researched extension supported by PostgreSQL documentation.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/transaction-iso.html).

<a id="ns20"></a>

### NS20 · Why are migrations versioned, hashed and locked?

**Priority:** start now. **Implementation:** Current source.

A migration changes a database schema in a repeatable sequence. Startup reads only this service’s numbered SQL files, sorts them and records a Secure Hash Algorithm 256-bit (SHA-256) checksum. An advisory lock prevents two replicas applying the same sequence together. A changed applied file is rejected: add a new migration. Backups and compatible rollout still matter; a checksum cannot recover lost data.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-ns20) · symbol: `Migration ${version} changed after application`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/explicit-locking.html) · [node-postgres.com · reference 2](https://node-postgres.com/features/transactions).

<a id="ns21"></a>

### NS21 · What do pool error events and verified TLS protect?

**Priority:** start now. **Implementation:** Current source.

Idle database clients can fail outside an awaited query, so the pool also has an error listener. Transport Layer Security (TLS) encrypts the connection and verifies its peer. This configuration retains rejectUnauthorized: true and accepts a certificate authority (CA) chain. Do not repair a certificate error by disabling verification. Connection-string ssl settings can replace explicit pg settings; the project rejects that mixture.

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-ns21) · symbol: `rejectUnauthorized: true`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/ssl) · [node-postgres.com · reference 2](https://node-postgres.com/apis/pool).

<a id="ns22"></a>

### NS22 · How does promisify connect callbacks to async/await?

**Priority:** start now. **Implementation:** Current source.

Node’s scrypt callback follows the error-first convention: an error argument precedes the result. util.promisify wraps that convention in a Promise-returning function, so await can receive the derived bytes and a rejection can be caught. It does not move arbitrary JavaScript work to another thread. Methods that rely on this may also need binding before conversion.

**Project:** [backend/src/identity/password.ts](evidence/node-backend-source-context.md#source-ns22) · symbol: `const scrypt = promisify(scryptCallback);`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/util.html).

<a id="ns23"></a>

### NS23 · Why use a salt and scrypt for passwords?

**Priority:** start now. **Implementation:** Current source.

scrypt deliberately costs memory and computation; a fast general hash is unsuitable for passwords. A random salt prevents equal passwords from sharing an encoded result and is stored beside the hash. Here 16 random bytes become 32 hexadecimal characters. Async hashing still consumes finite worker capacity, so limit login load and review work factors against current security guidance rather than calling library defaults production hardening.

**Project:** [backend/src/identity/password.ts](evidence/node-backend-source-context.md#source-ns23) · symbol: `const salt = randomBytes(16).toString('hex');`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/crypto.html) · [cheatsheetseries.owasp.org · reference 2](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

<a id="ns24"></a>

### NS24 · Does timingSafeEqual make the whole login constant-time?

**Priority:** start now. **Implementation:** Current source.

No. It avoids content-dependent early exit in that equal-length byte comparison. This verifier checks the stored encoding and derives a candidate Buffer first; the rest of login has other timing behavior. A dummy derivation also runs for a missing account to reduce obvious differences, followed by an explicit account-exists check. It cannot authenticate a missing user and does not prove complete timing resistance.

**Project:** [backend/src/identity/password.ts](evidence/node-backend-source-context.md#source-ns24) · symbol: `return timingSafeEqual(candidate, Buffer.from(hash, 'hex'));`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/crypto.html).

<a id="ns25"></a>

### NS25 · What does this JWT prove, and what stays readable?

**Priority:** start now. **Implementation:** Current source.

A JSON Web Token (JWT) carries readable encoded claims and a signature, not encrypted private data. This token expires in one hour. HS256 means Hash-based Message Authentication Code with SHA-256: signers and verifiers share a secret. Any verifier possessing it can also mint tokens, so separate asymmetric identity issuance is a production extension. Never put secrets in its payload.

**Project:** [backend/src/common/auth.ts](evidence/node-backend-source-context.md#source-ns25) · symbol: `algorithm: 'HS256'`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [github.com · reference 1](https://github.com/auth0/node-jsonwebtoken) · [www.rfc-editor.org · reference 2](https://www.rfc-editor.org/rfc/rfc7519.html).

<a id="ns26"></a>

### NS26 · Why verify JWT claims as well as its signature?

**Priority:** start now. **Implementation:** Current source.

A valid signature alone does not mean the token was intended for this API. verifyActor allowlists HS256 and checks issuer, audience, expiry and the expected principal fields; its subject must equal email. Decoding alone is not verification. Invalid or expired credentials produce 401. A verified actor can still receive 403 when its role or ownership does not allow the requested action.

**Project:** [backend/src/common/auth.ts](evidence/node-backend-source-context.md#source-ns26) · symbol: `algorithms: ['HS256']`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [github.com · reference 1](https://github.com/auth0/node-jsonwebtoken) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/guards).

<a id="ns27"></a>

### NS27 · How do authentication, roles and ownership differ?

**Priority:** start now. **Implementation:** Current source.

Authentication establishes who called; a role narrows which class of action they may attempt. Ownership decides whether they may act on this particular record. Here only the target provider may resolve an inquiry and only the notification recipient may mark it read. Read queries also filter by the actor. A browser-supplied email or a hidden button is not an authorization control.

**Project:** [backend/src/notifications/notifications.service.ts](evidence/node-backend-source-context.md#source-ns27) · symbol: `if (row.recipient_email !== actor.email)`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md) · [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md) · [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/security/authorization).

<a id="ns28"></a>

### NS28 · What does the in-memory login throttle actually limit?

**Priority:** next. **Implementation:** Current source.

A Map stores counts and expiry per request IP address, with a limit of thirty attempts per minute in each process. Mutating a retrieved object changes that stored object; expired entries are removed on later requests. Another replica has another Map, and restart clears it. This is not a shared distributed limit. Proxy trust and a bounded shared store need deliberate design before public exposure.

**Project:** [backend/src/identity/identity.controller.ts](evidence/node-backend-source-context.md#source-ns28) · symbol: `private readonly attempts = new Map`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/security/rate-limiting) · [expressjs.com · reference 2](https://expressjs.com/en/guide/behind-proxies.html).

<a id="ns29"></a>

### NS29 · Why handle fetch rejection and response status separately?

**Priority:** start now. **Implementation:** Current source.

fetch rejects for network or abort failures, but an HTTP 404 is normally a resolved Response. The provider lookup therefore catches transport errors, handles 404, checks response.ok, then parses JSON and validates its shape. A successful status with malformed data is still a failed dependency contract. The caller receives a controlled error, not a partly trusted owner record.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns29) · symbol: `if (!response.ok)`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/globals.html) · [fetch.spec.whatwg.org · reference 2](https://fetch.spec.whatwg.org/).

<a id="ns30"></a>

### NS30 · What do a fetch timeout and URL encoding guarantee?

**Priority:** start now. **Implementation:** Current source.

AbortSignal.timeout bounds this lookup to five seconds; encodeURIComponent keeps the provider ID inside one path component. Neither supplies an end-to-end request deadline or authorization. The lookup uses a distinct internal service key, not a browser JWT. Its database transaction and advisory lock remain occupied during the lookup, so slow dependencies can consume pool capacity.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns30) · symbol: `signal: AbortSignal.timeout(5000),`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/globals.html).

<a id="ns31"></a>

### NS31 · How does an idempotency key differ from a payload fingerprint?

**Priority:** start now. **Implementation:** Current source.

The key names one logical submission and is scoped to the authenticated client. The fingerprint hashes a fixed-order array of validated fields to detect changed content. Reusing the same key and content returns the original inquiry; changed content yields 409. Generate and preserve the key before sending. A timeout is uncertain outcome, so retry the original key and payload rather than creating a second submission.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns31) · symbol: `export function fingerprint(input: CreateInquiry): string {`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/crypto.html) · [www.postgresql.org · reference 2](https://www.postgresql.org/docs/current/ddl-constraints.html).

<a id="ns32"></a>

### NS32 · Why generate separate inquiry and event UUIDs?

**Priority:** start now. **Implementation:** Current source.

A Universally Unique Identifier (UUID) labels one record; randomUUID generates one without a central counter. The inquiry ID identifies the business request, while the event ID identifies the notification-producing occurrence. Neither replaces the client’s retry key. Keeping these identities separate lets a durable event replay retain its identity and allows future events about the same inquiry.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns32) · symbol: `const eventId = randomUUID();`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/crypto.html).

<a id="ns33"></a>

### NS33 · How does an outbox avoid losing an event intent?

**Priority:** start now. **Implementation:** Current source.

The inquiry row and outbox row commit in one PostgreSQL transaction. Either both exist or neither does. A later publisher sends the persisted event, waits for Kafka acknowledgment and marks it published. An HTTP success proves a durable inquiry and event intent; it does not prove inbox delivery. No transaction here atomically covers both Kafka and PostgreSQL, so consumer deduplication is required.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns33) · symbol: `INSERT INTO outbox(event_id,inquiry_id,payload)`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md) · [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/transactions) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/reliability/outbox).

<a id="ns34"></a>

### NS34 · What makes inquiry status transitions safe?

**Priority:** start now. **Implementation:** Current source.

The inquiry row is locked while the service checks ownership and current status. PENDING may become ACCEPTED or DECLINED. Repeating the same final decision returns that state; trying the other decision after resolution yields 409. Database checks restrict stored status values, and the unique client/key constraint protects submission identity. A valid enum alone cannot enforce ownership or transition order.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-ns34) · symbol: `if (row.status !== 'PENDING' && row.status !== input.status)`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/ddl-constraints.html).

<a id="ns35"></a>

### NS35 · What are Kafka’s client, producer, consumer and group?

**Priority:** start now. **Implementation:** Current source.

KafkaJS connects Node to a broker. A producer sends topic records; a consumer reads assigned partitions. clientId labels an application for diagnostics, whereas groupId identifies consumers sharing partition work and resume positions. Notifications uses one stable group. Starting another group reads independently and can reproduce effects unless the destination still deduplicates event identities.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-ns35) · symbol: `groupId: 'marketplace-notifications-v1'`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [kafka.js.org · reference 1](https://kafka.js.org/docs/configuration) · [kafka.js.org · reference 2](https://kafka.js.org/docs/consuming).

<a id="ns36"></a>

### NS36 · Do keys and acks=-1 guarantee exactly-once processing?

**Priority:** start now. **Implementation:** Current source.

No. The inquiry ID key helps route related records to a partition, where offsets give order. acks=-1 waits for the in-sync replicas required by the broker configuration; a one-broker setup still has one copy. A publisher can crash after acknowledgment but before marking the outbox row. Its retry may resend the same event. There is no global order across partitions.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-ns36) · symbol: `acks: -1,`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [kafka.js.org · reference 1](https://kafka.js.org/docs/producing).

<a id="ns37"></a>

### NS37 · Why publish a bounded SKIP LOCKED batch?

**Priority:** start now. **Implementation:** Current source.

FOR UPDATE SKIP LOCKED lets competing publishers take unlocked outbox rows without waiting on each other. LIMIT 25 bounds each transaction’s batch; it does not bound the entire backlog. Publishing happens while row locks and the database client are held, so broker delays lengthen transactions. Multiple publishers may deliver batches out of creation order; strict ordering would need an additional design.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-ns37) · symbol: `LIMIT 25 FOR UPDATE SKIP LOCKED`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/18/sql-select.html).

<a id="ns38"></a>

### NS38 · Does fromBeginning replay every record on every restart?

**Priority:** start now. **Implementation:** Current source.

No. A consumer group normally resumes at its committed offset, which is its saved position per partition. fromBeginning: true chooses the earliest available position only when no valid committed position exists. Retention may already have removed older records. Rebalancing redistributes partitions as members join or fail; it can cause replay around unfinished work.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-ns38) · symbol: `fromBeginning: true,`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [kafka.js.org · reference 1](https://kafka.js.org/docs/consuming).

<a id="ns39"></a>

### NS39 · Why decode, parse and validate an event separately?

**Priority:** start now. **Implementation:** Current source.

Kafka transports bytes. Buffer.toString decodes UTF-8, an encoding of text into bytes; JSON.parse then creates a JavaScript value. Zod finally checks its required fields and types. Valid JSON can still be an invalid event. The consumer awaits durable notification insertion before its handler succeeds; failures must not be treated as successfully processed records.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-ns39) · symbol: `await this.notifications.consume(JSON.parse(message.value.toString('utf8')));`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/buffer.html) · [kafka.js.org · reference 2](https://kafka.js.org/docs/consuming).

<a id="ns40"></a>

### NS40 · How can repeated event delivery produce one inbox row?

**Priority:** start now. **Implementation:** Current source.

Notifications stores a unique event_id and uses INSERT ... ON CONFLICT DO NOTHING. The receipt identity and inbox effect are the same database write. A crash after insertion but before offset commit may replay the event; that insertion becomes a no-op. This is an idempotent effect with at-least-once transport, not proof that the event was transported exactly once.

**Project:** [backend/src/notifications/notifications.service.ts](evidence/node-backend-source-context.md#source-ns40) · symbol: `ON CONFLICT(event_id) DO NOTHING`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/sql-insert.html).

<a id="ns41"></a>

### NS41 · Why can HTTP start while the messaging worker reconnects?

**Priority:** start now. **Implementation:** Current source.

The bootstrap hook starts a background Promise without awaiting the whole loop. Startup connection failures are caught and retried; consumer failures after run starts follow KafkaJS’s separate crash/restart policy and can leave a stopped worker. The pause uses an unreferenced timer, which alone will not keep Node alive. void does not catch rejections. Graceful completion and shutdown races still need tests.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-ns41) · symbol: `void this.run();`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/timers.html) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/fundamentals/lifecycle-events).

<a id="ns42"></a>

### NS42 · What do KafkaJS instrumentation events say about health?

**Priority:** start now. **Implementation:** Current source.

The consumer updates a local flag on group join, crash and disconnect. KafkaJS instrumentation listeners run asynchronously, which differs from ordinary synchronous Node EventEmitter listeners. A group join proves membership at that point, not a caught-up inbox or successful business processing. Observe lag and processing errors too; a flag may lag a failure or remain true while a poison record blocks progress. Inspect the CRASH restart flag and actual offset/insert progress: a stopped consumer can leave this application’s outer loop sleeping.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-ns42) · symbol: `this.consumer.events.GROUP_JOIN`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [kafka.js.org · reference 1](https://kafka.js.org/docs/instrumentation-events).

<a id="ns43"></a>

### NS43 · Why expose three different health checks?

**Priority:** start now. **Implementation:** Current source.

Liveness reports a responding process. Serving health queries the database and permits durable inquiry writes while messaging retries. Readiness also checks the messaging worker flag where applicable. Neither a green probe nor nginx’s static /health proves a login-to-inquiry-to-notification journey. Restarting a live process for every dependency failure can turn one outage into a restart storm.

**Project:** [backend/src/common/health.ts](evidence/node-backend-source-context.md#source-ns43) · symbol: `@Get('health/serve')`.

**Lessons:** [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/recipes/terminus).

<a id="ns44"></a>

### NS44 · Does a shared backend image mean one service or one failure domain?

**Priority:** start now. **Implementation:** Current source.

One build contains the code, but SERVICE selects one controller, provider set and service-owned database per process. There are four capability boundaries. Their shared PostgreSQL host can still fail all four locally; an image or shared library defect can affect them together. Independent processes enable separate scaling but do not automatically create high availability or independent data ownership.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-ns44) · symbol: `const providers: Record<string, Type[]> = {`.

**Lessons:** [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/fundamentals/custom-providers).

<a id="ns45"></a>

### NS45 · Does FOR UPDATE prevent a stale profile overwrite?

**Priority:** next. **Implementation:** Absent implementation.

It serializes database writers while the transaction runs. It does not know that a user opened an older profile in a second tab. Catalog has no profile version or entity tag comparison, so two accepted full updates can overwrite editable fields. Optimistic concurrency would compare a version and reject a stale update so the user can reload and merge.

**External worked example (not installed here):** Practice with a separate conditional-update server: GET version 7 with its entity tag, send an update with If-Match for version 7 and advance to 8; repeat the old condition and expect 412 Precondition Failed. Persist and compare the version atomically. The marketplace does not currently expose this contract. [Official example](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match).

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-ns45) · symbol: `WHERE owner_email=$1 FOR UPDATE`.

**Lessons:** [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** Lesson16 teaches the row-lock versus stale-user conflict distinction and labels optimistic version checking absent. The If-Match worked example is an external extension.

**Official documentation:** [www.rfc-editor.org · reference 1](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match).

<a id="ns46"></a>

### NS46 · How do CORS and CSRF differ from login protection?

**Priority:** extension. **Implementation:** Absent implementation.

Cross-origin resource sharing (CORS) controls browser access across origins; it is not an authorization boundary for arbitrary clients. Cross-site request forgery (CSRF) abuses credentials a browser attaches automatically, especially cookies. This app uses same-origin proxies and explicit bearer headers; it does not implement a cookie-session CSRF flow. If that design changes, add explicit origin and CSRF controls rather than treating Helmet as a substitute.

**External worked example (not installed here):** In a separate Nest app, enable CORS for one explicit test origin and PUT, with Authorization allowed. Send an OPTIONS preflight from that origin and inspect the allowed-origin/method headers; repeat from another origin and verify no readable cross-origin response. Then test server authorization directly because CORS does not stop non-browser callers. [Official example](https://docs.nestjs.com/security/cors).

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-ns46) · symbol: `app.use(helmet());`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** Lessons08/16 are security and reliability prerequisites; they do not teach CORS or CSRF. This is a researched extension taught by the linked official documentation and external worked example.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/security/cors) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/security/csrf).

<a id="ns47"></a>

### NS47 · How do sessions, OAuth and OpenID Connect differ from this JWT login?

**Priority:** extension. **Implementation:** Absent implementation.

A server session normally stores login state server-side and sends a session identifier cookie. OAuth 2.0 delegates access; OpenID Connect adds an identity layer. This project implements neither federation nor refresh/session revocation: it issues its own one-hour bearer token. A logged-out browser can discard it, but an already copied valid token stays usable until expiry unless server-side revocation is added.

**External worked example (not installed here):** Use Appendix B’s Proof Key for Code Exchange (PKCE) test vector in a separate local script: SHA-256 hash the published verifier, then base64url encode the bytes. Expect challenge E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM. In an authorization-code flow, bind that challenge at authorization and require the original verifier at code exchange. This demonstrates code binding, not a deployed identity provider. [Official example](https://www.rfc-editor.org/rfc/rfc7636.html#appendix-B).

**Project:** [backend/src/common/auth.ts](evidence/node-backend-source-context.md#source-ns47) · symbol: `expiresIn: '1h'`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** Lesson08 provides JWT authentication prerequisites; it does not teach sessions, OAuth, OpenID Connect or PKCE. These are researched extensions taught by the linked official specifications and external worked example.

**Official documentation:** [expressjs.com · reference 1](https://expressjs.com/en/resources/middleware/session/) · [openid.net · reference 2](https://openid.net/specs/openid-connect-core-1_0.html) · [datatracker.ietf.org · reference 3](https://datatracker.ietf.org/doc/html/rfc9700).

<a id="ns48"></a>

### NS48 · What does graceful shutdown promise here?

**Priority:** next. **Implementation:** Current source.

Nest shutdown hooks are enabled, database destruction ends its pool, and messaging destruction sets stopping and disconnects the client. A shutdown signal is not a guarantee that every in-flight request or detached loop drained before termination. The process needs time to finish; a forced kill skips hooks. Test shutdown under active work and verify durable retries instead of assuming every hook establishes lossless delivery.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-ns48) · symbol: `app.enableShutdownHooks();`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/fundamentals/lifecycle-events).

<a id="ns49"></a>

### NS49 · What should application logs prove without leaking secrets?

**Priority:** next. **Implementation:** Current source.

Logs should identify the failing operation and enough safe context to connect it with a request or event. ErrorFilter hides unexpected server details from clients while logging the error internally; worker logs name retry failures. Do not log bearer tokens, passwords or connection strings. Structured correlation across requests and events is an extension; the existing logger alone is not a distributed trace.

**Project:** [backend/src/common/errors.ts](evidence/node-backend-source-context.md#source-ns49) · symbol: `this.logger.error(error instanceof Error ? error.stack : String(error))`.

**Lessons:** [16 · reliability and senior design](generated/16-reliability-and-senior-design.md) · [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md).

**Lesson relationship:** Lessons16/17 provide reliability and delivery prerequisites. Safe correlation-log design is a researched extension; current ErrorFilter output is the project example.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/techniques/logger).

<a id="ns50"></a>

### NS50 · In which order do middleware, guards, pipes and interceptors run?

**Priority:** extension. **Implementation:** Absent implementation.

On the usual successful path, middleware runs first, then guards, interceptor entry, pipes and the controller/service; interceptor response handling unwinds in reverse order. Filters handle uncaught failures rather than a mandatory success stage. Middleware handles requests broadly, a guard decides access, a pipe validates/transforms arguments and an interceptor wraps execution. This project uses middleware, AuthGuard and ErrorFilter; it calls Zod directly and has no custom application pipe/interceptor.

**External worked example (not installed here):** In the official ParseIntPipe route example, bind ParseIntPipe to an id parameter. Request /cats/42 and inspect a number passed to the handler; request /cats/nope and expect 400 before the handler. Add a logging interceptor in an isolated app to observe its before/after execution around that handler. These are practice additions, not current marketplace registrations. [Official example](https://docs.nestjs.com/pipes).

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-ns50) · symbol: `app.useGlobalFilters(new ErrorFilter());`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [19 · source and requirement coverage](generated/19-source-and-requirement-coverage.md).

**Lesson relationship:** Lessons05/19 provide Nest wiring and source-inventory prerequisites. Full middleware/guard/pipe/interceptor ordering is a researched extension; custom application pipes and interceptors are absent.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/faq/request-lifecycle) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/pipes) · [docs.nestjs.com · reference 3](https://docs.nestjs.com/interceptors).

<a id="ns51"></a>

### NS51 · Does this project use ConfigModule?

**Priority:** extension. **Implementation:** Absent implementation.

No. validateConfig and required read process.env directly and fail startup for missing or invalid settings. Nest ConfigModule is an optional configuration package, not automatically installed by using Nest. Both approaches still need runtime checks, separate environment values and secret handling. Never print a whole environment object while troubleshooting.

**External worked example (not installed here):** In a separate Nest example, register ConfigModule.forRoot with a validation function that rejects a nonnumeric PORT. Start with PORT=abc and expect startup rejection; use a valid port and read the validated value through ConfigService. Do not assume this marketplace has ConfigService injection or automatic .env loading. [Official example](https://docs.nestjs.com/techniques/configuration).

**Project:** [backend/src/common/config.ts](evidence/node-backend-source-context.md#source-ns51) · symbol: `export function validateConfig(): void {`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [19 · source and requirement coverage](generated/19-source-and-requirement-coverage.md).

**Lesson relationship:** Lessons05/19 provide Nest wiring and source-inventory prerequisites. ConfigModule usage is a researched extension and is absent from this project.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/techniques/configuration).

<a id="ns52"></a>

### NS52 · Is pg an object-relational mapper?

**Priority:** extension. **Implementation:** Absent implementation.

No. pg sends SQL and returns rows; this project explicitly writes queries, transactions and migrations. An object-relational mapper (ORM) maps entities to database operations; TypeORM and Prisma are absent. An ORM can reduce mapping code but does not remove query planning, ownership checks or transaction boundaries. Do not invent repositories or entity decorators when explaining this source.

**External worked example (not installed here):** In the separate official TypeORM example, define a User entity, register TypeOrmModule.forFeature([User]) and inject its Repository into UsersService. Insert a synthetic user, find it, restart and read it again from the configured database. Examine generated SQL and ensure the database is isolated; none of these entity/repository registrations exists here. [Official example](https://docs.nestjs.com/data/typeorm#repository-pattern).

**Project:** [backend/package.json](evidence/node-backend-source-context.md#source-ns52) · symbol: `"pg"`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md) · [19 · source and requirement coverage](generated/19-source-and-requirement-coverage.md).

**Lesson relationship:** Lessons07/19 teach the actual pg/SQL approach and source inventory. The TypeORM repository example is a researched external extension; an ORM is absent here.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/techniques/database) · [docs.nestjs.com · reference 2](https://docs.nestjs.com/techniques/sql) · [docs.nestjs.com · reference 3](https://docs.nestjs.com/data/typeorm).

<a id="ns53"></a>

### NS53 · Does AuthGuard here use Passport strategies?

**Priority:** extension. **Implementation:** Absent implementation.

No. It is the project’s own Nest guard calling jsonwebtoken directly. Passport is an authentication integration with strategies such as local credentials or bearer-token validation; its Nest module is absent. Switching adapters would still require verified claims and resource ownership checks, and would not create external identity federation by itself.

**External worked example (not installed here):** Follow the external local-strategy example in an isolated Nest app: implement validate(username,password), register the strategy and use AuthGuard("local") on a test login route. A valid synthetic user reaches the handler as request.user; a wrong password yields 401. Keep marketplace JWT and ownership behavior intact if evaluating a migration. [Official example](https://docs.nestjs.com/recipes/passport).

**Project:** [backend/src/common/auth.ts](evidence/node-backend-source-context.md#source-ns53) · symbol: `export class AuthGuard implements CanActivate {`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md) · [19 · source and requirement coverage](generated/19-source-and-requirement-coverage.md).

**Lesson relationship:** Lessons08/19 provide actual JWT-guard and source-inventory prerequisites. Passport strategies are a researched external extension and are absent here.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/recipes/passport).

<a id="ns54"></a>

### NS54 · Are these API schemas generated by Swagger?

**Priority:** extension. **Implementation:** Absent implementation.

No. CONTRACT.md documents the interface and Zod enforces input; there is no Swagger/OpenAPI module or generated specification in this app. OpenAPI is a machine-readable API description and Swagger tooling can render it. Documentation generation and runtime validation are separate; a page of schemas does not prove actual route behavior matches.

**External worked example (not installed here):** In the external Nest Swagger bootstrap example, build a document using DocumentBuilder and SwaggerModule.createDocument, then mount it with SwaggerModule.setup. Inspect the resulting paths and try a synthetic endpoint. Verify 400/401/error responses separately against real requests; this marketplace does not expose that generated document. [Official example](https://docs.nestjs.com/openapi/introduction).

**Project:** [backend/package.json](evidence/node-backend-source-context.md#source-ns54) · symbol: `"zod"`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md) · [19 · source and requirement coverage](generated/19-source-and-requirement-coverage.md).

**Lesson relationship:** Lessons06/19 provide runtime-schema and source-inventory prerequisites. Generated Swagger/OpenAPI documentation is a researched external extension and is absent here.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/openapi/introduction).

<a id="nsi01"></a>

### NSI01 · Login returns 401 even with a token: where do you look?

**Priority:** start now. **Implementation:** Current source.

Separate a missing or invalid credential from a permission failure. Use a synthetic test account, never print its bearer token in evidence.

**Symptom:** Authenticated requests return 401 after login or between services.

**Checks:** Check the Authorization Bearer header, expiry, clock, issuer/audience, allowlisted algorithm and that service secret configuration belongs to the same environment; inspect names/presence without exposing values.

**Repair:** Restore the intended environment configuration or log in again for an expired token. Keep verification and claim checks enabled.

**Recovery verification:** A fresh valid token returns /api/auth/me; an expired or tampered token remains 401, and another owner still cannot edit protected data.

**Project:** [backend/src/common/auth.ts](evidence/node-backend-source-context.md#source-nsi01) · symbol: `throw new UnauthorizedException('Invalid or expired bearer token');`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [github.com · reference 1](https://github.com/auth0/node-jsonwebtoken).

<a id="nsi02"></a>

### NSI02 · Catalog returns 400 or an unexpected search page: how do you diagnose it?

**Priority:** start now. **Implementation:** Current source.

Distinguish schema rejection from query behavior; changing validation just to make a request pass can break the API contract.

**Symptom:** A search returns 400, false behaves like true, or rate sorting looks wrong.

**Checks:** Compare query strings with searchSchema: available accepts only true/false, page is zero-based and size is 1–50. Inspect numeric casts and deterministic id sorting in CatalogService.

**Repair:** Correct the caller’s query and use the explicit boolean transform and numeric SQL cast. Keep bounds and unknown-key rejection.

**Recovery verification:** available=false&size=2 returns 200 with at most two matching items; available=yes stays 400. Rates sort numerically and equal rates have stable id ordering.

**Project:** [backend/src/catalog/provider.schema.ts](evidence/node-backend-source-context.md#source-nsi02) · symbol: `.enum(['true', 'false'])`.

**Lessons:** [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [zod.dev · reference 1](https://zod.dev/api).

<a id="nsi03"></a>

### NSI03 · All database-backed requests slow down: what do you measure first?

**Priority:** start now. **Implementation:** Current source.

Pool exhaustion can be a symptom of long work, leaked clients or locks. More connections are not an automatic repair.

**Symptom:** Requests queue or fail near the five-second connection-acquisition limit.

**Checks:** Inspect pool totalCount, idleCount and waitingCount in an isolated diagnostic; inspect pg_stat_activity and pg_locks for long transactions and blocked queries. Check finally release paths and the catalog lookup held inside inquiry transactions.

**Repair:** Fix leaked-client paths or slow/blocking work, bound dependency waits and tune capacity to database limits. Do not terminate sessions or increase max blindly.

**Recovery verification:** Under the same bounded test load, waitingCount returns to zero after completion, transaction age falls, and repeated successful and failed requests do not steadily consume connections.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nsi03) · symbol: `client.release();`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/pooling) · [www.postgresql.org · reference 2](https://www.postgresql.org/docs/current/monitoring-stats.html).

<a id="nsi04"></a>

### NSI04 · Startup reports a changed migration checksum: what is safe?

**Priority:** start now. **Implementation:** Current source.

The refusal protects reproducibility; deleting the recorded checksum hides drift rather than repairing it.

**Symptom:** A service fails startup because an already applied migration changed.

**Checks:** Compare the deployed migration version/checksum with the intended source and review the edited SQL. Verify which service-owned database and environment are selected.

**Repair:** Restore the original applied file and express the change in a new numbered migration. Rehearse against an isolated database and retain a backup/recovery path.

**Recovery verification:** Old checksums still match, the new migration appears once, a second startup applies nothing, and service acceptance confirms compatible reads/writes.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nsi04) · symbol: `changed after application; create a new migration`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/transactions).

<a id="nsi05"></a>

### NSI05 · An inquiry response timed out: should you submit again?

**Priority:** start now. **Implementation:** Current source.

A lost response does not reveal whether the write committed. Preserve its original identity while investigating.

**Symptom:** The browser times out after submitting an inquiry and the user is unsure whether it exists.

**Checks:** Recover the original client-scoped key and exact validated payload; check the participant inquiry list and the service’s idempotency path. Identify whether failure happened at catalog lookup, SQL commit or response transport.

**Repair:** Retry with the same key and payload. If content must change, first reconcile the original result; do not rotate the key automatically after timeout.

**Recovery verification:** Sequential and concurrent identical retries return one inquiry ID and one outbox event; changed content with the original key returns 409; no unrelated actor can retrieve it.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-nsi05) · symbol: `Idempotency key already used for a different inquiry`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/current/ddl-constraints.html) · [node-postgres.com · reference 2](https://node-postgres.com/features/transactions).

<a id="nsi06"></a>

### NSI06 · Inquiry exists but the inbox is empty: how do you isolate the stage?

**Priority:** start now. **Implementation:** Current source.

Follow the durable record through publication and consumption instead of treating an empty inbox as proof the inquiry vanished.

**Symptom:** The client sees a committed inquiry while its provider sees no notification.

**Checks:** In local service-owned databases, inspect the inquiry’s outbox published_at and event identity, publisher retry logs, broker/topic availability and recipient filter. Inspect consumer CRASH error classification and its restart flag, group membership, committed offsets and actual offset/insert progress. A background consumer may have stopped while the outer loop still sleeps; a green serving probe or stale worker flag is insufficient.

**Repair:** Repair the failing local broker/configuration or database dependency. Publisher retries can resume its durable outbox work. For a stopped non-restarting consumer, perform a controlled LOCAL notifications-process restart after the cause is fixed, retaining its group ID, committed offsets and event IDs. Do not insert a replacement inquiry, rotate the group or mark an unsent row published.

**Recovery verification:** During a local rehearsal, verify the original outbox row becomes published, consumer offsets and durable inserts advance, the expected recipient receives one inbox row, replay still leaves one row and an unrelated actor sees none. Explicitly record whether restart was manual; these criteria do not prove automatic recovery.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-nsi06) · symbol: `UPDATE outbox SET published_at=now()`.

**Lessons:** [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md) · [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [kafka.js.org · reference 1](https://kafka.js.org/docs/producing) · [kafka.js.org · reference 2](https://kafka.js.org/docs/consuming).

<a id="nsi07"></a>

### NSI07 · A consumer repeatedly fails on one record: what happens next?

**Priority:** start now. **Implementation:** Absent implementation.

Malformed JSON or a schema failure prevents the handler from completing. KafkaJS may stop on a non-retriable processing error while this application’s outer loop keeps sleeping; automatic reconnect is not guaranteed. A quarantine/dead-letter workflow is absent. Skipping needs an explicit policy and durable evidence.

**Symptom:** The consumer logs the same parse/validation error and its partition makes no useful progress.

**Checks:** Identify topic, partition, offset and safe event identity; inspect the failure category without publishing private payloads. Read the CRASH restart flag and check actual processing progress and group membership. Distinguish transient database failures from deterministic malformed JSON or schema incompatibility; readiness alone cannot prove progress.

**Repair:** Repair transient dependencies or producer/schema compatibility. If the consumer stopped without restart, perform a controlled LOCAL process restart with the same group and offsets only after fixing the cause. The same poison record will fail again unless corrected or handled through a designed durable quarantine/replay policy; do not delete offsets merely to make readiness green.

**Recovery verification:** A local rehearsal must show the original failing record is successfully processed after compatible repair, or durably retained/quarantined by a separately implemented policy; later valid records advance and replay produces no duplicate inbox effect. Record the manual restart. Existing source does not establish quarantine or automatic recovery.

**External worked example (not installed here):** The current Nest outbox tutorial provides a separate order service with persistent dead-letter records and administrative requeue. In that example, force a handler to fail through its retry limit, inspect the recorded reason, repair the handler and requeue the same message. Verify one resulting business effect. Its package/version and storage setup are an external design example; this marketplace has no such quarantine flow. [Official example](https://docs.nestjs.com/reliability/outbox#retries-and-the-dead-letter-queue).

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-nsi07) · symbol: `throw new Error('Event payload missing; offset is not acknowledged');`.

**Lessons:** [10 · kafka inbox and notifications](generated/10-kafka-inbox-and-notifications.md).

**Lesson relationship:** Lesson10 teaches decoding, validation and offset failure boundaries. Crash/restart classification and the external durable quarantine policy are researched extensions; quarantine is absent from current implementation.

**Official documentation:** [kafka.js.org · reference 1](https://kafka.js.org/docs/consuming).

<a id="nsi08"></a>

### NSI08 · Local TLS connection fails after certificate changes: what stays enabled?

**Priority:** start now. **Implementation:** Current source.

Keep peer verification while checking certificate trust, hostname, expiry and configuration; an encrypted connection to an unverified peer is insufficient.

**Symptom:** A database or Kafka client fails with certificate, hostname or authentication errors.

**Checks:** Inspect the configured host, certificate authority chain and expiry, clock, TLS flag and environment scope. For pg, check that URL ssl parameters do not replace the explicit CA object. For Kafka, distinguish broker reachability from SCRAM credentials.

**Repair:** Restore the correct CA/hostname/credential configuration for the selected environment. Retain rejectUnauthorized true and fix the trust chain instead of disabling checks.

**Recovery verification:** The intended peer connects with verification enabled; a wrong CA or hostname still fails. Re-run a real local query or message round trip, not only a TCP connection probe.

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-nsi08) · symbol: `DB_URL ssl parameters`.

**Lessons:** [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/ssl) · [kafka.js.org · reference 2](https://kafka.js.org/docs/configuration).

<a id="nsi09"></a>

### NSI09 · Login rate limiting changes behind a proxy or replica: why?

**Priority:** start now. **Implementation:** Current source.

Process-local state and proxy address interpretation affect the observed rate limit. A public fix needs tests for both abuse resistance and legitimate users.

**Symptom:** Many users share a 429 limit, or adding replicas allows more attempts than expected.

**Checks:** Inspect request.ip and trusted proxy configuration using synthetic traffic; compare counts per process and the one-minute expiry. Check whether load balancing distributes attempts across independent Maps.

**Repair:** Configure only the actual trusted proxy hops and adopt a bounded shared counter if a global limit is required. Do not trust arbitrary forwarded headers or remove throttling.

**Recovery verification:** Synthetic users receive the intended independent limits; spoofed forwarding headers cannot bypass them; repeated attempts across replicas follow the documented policy and expire as expected.

**Project:** [backend/src/identity/identity.controller.ts](evidence/node-backend-source-context.md#source-nsi09) · symbol: `const key = request.ip ?? 'unknown';`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/security/rate-limiting) · [expressjs.com · reference 2](https://expressjs.com/en/guide/behind-proxies.html).

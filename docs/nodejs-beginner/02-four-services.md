# 2. Walk through each service

[Guide index](README.md) · [Previous: runtime](01-runtime-and-wiring.md) · [Next: the full journey](03-browser-events-and-aws.md)

For each endpoint, ask five questions: which handler receives it, what input is trusted, what rule is enforced, which database is changed, and what the caller sees on failure. A controller is the HTTP entrance.

A service contains application rules and, in this small repository, explicit SQL persistence. There is no separate ORM repository layer to find.

The common request route is `Express -> optional AuthGuard -> controller -> service -> pg -> response`. Middleware parses JSON before the handler. `AuthGuard` is only applied to guarded routes; public discovery and login do not require it.

Thrown exceptions reach [ErrorFilter](../../backend/src/common/errors.ts). Runtime schemas use Zod, not a global class-validator pipe.

## Identity: “Who is this?”

Read [IdentityController](../../backend/src/identity/identity.controller.ts), [IdentityService](../../backend/src/identity/identity.service.ts), [password helpers](../../backend/src/identity/password.ts), [auth helpers](../../backend/src/common/auth.ts), and [identity migration](../../backend/migrations/identity.001.sql).

| Public entry | Handler chain | Expected outcome |
|---|---|---|
| `POST /api/auth/login` | `IdentityController.login -> loginSchema.parse -> IdentityService.login -> signActor` | 200 with token/id/email/name/role |
| `GET /api/auth/me` | `AuthGuard -> IdentityController.me` | 200 with verified actor; no password hash |

### Startup and login, step by step

1. `Database.onModuleInit` creates `accounts` from `identity.001.sql` if not already applied. Email is the primary key, role has a `CLIENT/PROVIDER` SQL constraint, and the stored password is a hash.
2. `IdentityService.onApplicationBootstrap` computes a dummy hash even if demo seeding is off. When `SEED_DEMO=true`, it reads the provider seed file, creates provider actors plus two client actors, hashes the synthetic demo password, and inserts missing accounts in one transaction. `ON CONFLICT(email) DO NOTHING` avoids overwriting existing accounts. It does not reset a changed password on every boot.
3. `IdentityController.login` counts attempts by `request.ip` in an in-memory map with a one-minute window. The first 30 in a window proceed; the next is 429. This map is per process and clears on restart. No distributed rate limiter is implemented. The current nginx configuration does not forward a client identity header or configure Express trust proxy; behind that proxy, IP-based counts can aggregate users rather than represent each individual client accurately.
4. `loginSchema` accepts a strict object containing a valid email (up to 254 characters) and a password of 1–200 characters. Unknown extra fields fail with 400. TypeScript alone cannot validate HTTP JSON.
5. `IdentityService.login` lowercases the email for a parameterized query. `$1` is a placeholder; the email is passed separately. The SQL does not splice a user's email into its syntax.
6. If the account exists, `verifyPassword` checks its hash. If not, it still checks the dummy hash so the unknown-account path also performs hashing work. This reduces a timing discrepancy; it is not a guarantee that every request has identical timing.
7. `hashPassword` generates 16 random salt bytes, uses asynchronous Node `scrypt` to derive a 64-byte value, and encodes `scrypt:<salt hex>:<hash hex>`. Verification rejects malformed formats, derives a candidate, and uses `timingSafeEqual`. A salt is not the password and need not be secret. A password hash is not reversible encryption. Do not log either the submitted password or stored hash.
8. A missing account or mismatched password produces the same 401 message, `Invalid email or password`. A valid actor is signed as an HS256 JWT with issuer/audience `marketplace`, subject equal to email, and a one-hour expiry.

### A token is a signed claim, not a permission to do everything

`AuthGuard.canActivate` expects `Authorization: Bearer <token>`. `verifyActor` restricts the algorithm to HS256, checks signature/issuer/audience/expiry, and validates the principal's email/name/id/role relationship. It attaches the actor to `request.actor`.

Missing/malformed/expired/tampered tokens produce 401.

`GET /me` returns that actor. It does not re-read the accounts table on every request; changes to account state would need an explicit revocation/session design to take immediate effect.

No refresh-token, logout revocation list, user registration, password reset, or MFA workflow is implemented. Logging out in this UI removes the browser token; it does not invalidate every copy of that JWT.

HS256 uses the same secret for signing and verification. All four laboratory processes receive it; a compromised verifier could also mint tokens. **Production extension:** asymmetric issuer, key rotation, revocation/session policy, and hardened browser session handling.

Do not describe these as existing functionality.

**Check yourself:** explain why decoding a JWT without verifying it is unsafe, why a valid `CLIENT` token cannot edit a profile, and why the demo password should never be reused for a real account.

## Catalog: “Which provider, and who owns this profile?”

Read [CatalogController](../../backend/src/catalog/catalog.controller.ts), [CatalogService](../../backend/src/catalog/catalog.service.ts), [provider/search schemas](../../backend/src/catalog/provider.schema.ts), and [catalog migration](../../backend/migrations/catalog.001.sql).

The `providers` table stores `id`, private `owner_email`, and a public JSONB `document`. JSONB is PostgreSQL's structured JSON storage.

A SQL check ensures the document ID matches the row ID. Owner email is unique, so one account owns at most one profile here.

This is one service's storage, not a cross-service account foreign key.

### Public discovery

`GET /api/providers` calls `CatalogService.search`. `searchSchema` validates a strict query object. URL query values are strings: `maxRate/page/size` are coerced into numbers, `available` accepts only the strings `true` or `false`, page defaults to 0, and size defaults to 12 with a maximum of 50.

Passing `available=yes` or an unsupported sort gives 400. The frontend normally requests six items, which is different from the API default.

The method builds optional PostgreSQL predicates over JSONB fields. A text search escapes SQL LIKE wildcard characters and uses `ILIKE` for case-insensitive matching.

Category is compared case-insensitively; skill examines the skills array; max rate and availability filter typed JSON values. Values are always query parameters.

SQL fragments for sorting are selected from fixed code, not a user-provided SQL expression.

`rate-asc` sorts by price then ID. Both `recommended` and `rating` currently sort by rating descending then ID.

“Recommended” is not a personalized recommendation engine. The ID tie-breaker keeps order deterministic.

A common table expression computes the total independently from the page array, so an out-of-range page can return `items: []` with a nonzero `total`. An empty catalog search is a normal 200 response, not 404.

`GET /api/providers/:id` calls `get -> row`. `row` parameterizes the ID and throws 404 when no row exists. `get` returns only `document`; it does not expose owner email.

### Provider-owned editing

`GET /api/providers/me` is declared before `:id` so the literal word `me` is not treated as a provider slug. Both GET/PUT `/me` use `AuthGuard` and `requireRole(actor, 'PROVIDER')`.

Wrong role is 403; missing token is 401.

1. `mine` queries by the actor's verified email, never a browser-supplied owner email. No matching profile is 404.
2. `update` parses the full strict `providerSchema` before entering its transaction. This is a full profile PUT; sending only `{hourlyRate: 80}` fails validation. Allowed categories, HTTPS portfolio links, bounded arrays/text, integer rate 5–1000, and other fields are checked. Schema-valid input can still fail a business authorization rule.
3. The transaction selects the caller's row `FOR UPDATE`, locking it while the update proceeds. If absent, 404. If the supplied profile ID differs from the caller's stored ID, 403.
4. The server preserves the stored `rating`, `reviewCount`, and `completedProjects` even when the submitted document contains different valid values. Ownership and reputation cannot be assigned just by changing the UI payload.
5. It updates the JSONB document using parameters and returns the saved document. The transaction commits before the HTTP operation resolves. Restarting the service preserves that profile because storage is PostgreSQL and seeding does not overwrite existing rows.

There is no profile deletion endpoint. An exercise on CRUD design should discuss deletion rules before inventing a destructive route.

The row lock serializes concurrent writers but there is no optimistic version/ETag; two successful full PUT requests can overwrite each other's editable fields. **Extension:** version checks and a clear conflict UX.

### The private lookup

`GET /internal/providers/:id` compares `X-Internal-Key` with the configured internal key using length checking plus timing-safe comparison, then returns `{id, ownerEmail, name}`. Wrong/missing key is 403, missing provider is 404.

This is how Inquiries learns the recipient without exposing owner email through the public profile.

The edge only proxies `/api/...`; `/internal/...` is absent from [nginx](../../frontend/nginx.conf) and [Vite](../../frontend/vite.config.ts) API routing. An nginx request to that unproxied path may receive the SPA HTML fallback with 200; that is **not** a successful internal API lookup.

In local Compose the backend ports are intentionally published on loopback, so a developer can reach Catalog directly at 8182. The key still protects its internal handler.

Proxy omission is an exposure reduction, not a replacement for authentication or network controls.

**Check yourself:** identify the exact SQL that protects owner identity, why browser input cannot pick `owner_email`, and which three fields are preserved by the update service.

## Inquiries: “Record one logical request safely”

Read [InquiriesController](../../backend/src/inquiries/inquiries.controller.ts), [InquiriesService](../../backend/src/inquiries/inquiries.service.ts), [inquiry/event schemas](../../backend/src/inquiries/inquiry.schema.ts), and [inquiries migration](../../backend/migrations/inquiries.001.sql).

The entire controller uses `AuthGuard`. Its routes create, list, and respond.

There is no delete route. An inquiry row contains a snapshot of provider/client names, emails, the message/budget, status, and its retry identity.

Those private emails do not appear in `inquiryView`, the function that builds the public response. Numeric PostgreSQL values are converted with `Number` and dates with `toISOString` at that boundary.

### Creation: distinguish three different identities

`actor.email` says **who is asking**. `providerId` says **who should receive the inquiry**. `Idempotency-Key` says **which logical submission this HTTP request belongs to**. The random inquiry ID identifies the stored business record; the event ID identifies the event that announces it.

These values solve different problems.

1. `create` requires role `CLIENT`; a provider gets 403. The key must contain 8–100 letters/digits/underscores/hyphens; missing or invalid key is 400.
2. `inquirySchema` rejects unknown fields, validates provider slug, trims subject/message, requires subject 5–160 characters and message 20–5000 characters, validates budget 1–9,999,999,999.99 with at most two decimal places, and restricts `clientType` to COMPANY/INDIVIDUAL. The current UI's budget input has a stricter maximum than the backend, so UI and API constraints should be explained separately.
3. `fingerprint` hashes a fixed-order JSON array of the **parsed** fields. That means equivalent object key order does not create a different hash; trimmed text is compared in its parsed form. The SHA-256 digest detects payload mismatch for a key; it is not password hashing or message encryption.
4. A transaction acquires `pg_advisory_xact_lock(hashtextextended(...))` derived from `[actor.email, key]`. Two simultaneous calls with the same client/key wait for one another even if handled by different process replicas. `await` would not provide this coordination.
5. It queries a previous row by that client/key. Same fingerprint returns the original inquiry; changed fingerprint produces 409. This check happens before a new Catalog lookup, so a persisted retry can return the existing result even if Catalog later goes down. The SQL unique constraint on `(client_email,idempotency_key)` is another invariant.
6. For a new key, `provider` calls Catalog's private route using Node's built-in `fetch`, an encoded ID, the internal header, and a five-second `AbortSignal.timeout`. A network timeout/error gives 503 with same-key retry guidance. Catalog 404 becomes 404; another non-success or an invalid JSON/schema response becomes 503.
7. Still using the transaction's checked-out client, the method inserts the inquiry and then an outbox row. PostgreSQL supplies default `PENDING` status. The event includes a fresh event UUID, inquiry UUID, recipient email, provider/client names, subject, and creation time.
8. The callback returns an inquiry view; `Database.transaction` commits before resolving to Nest. The POST uses Nest's default created status, 201. A same-key replay also goes through the same POST route and returns 201 with the original view; status alone does not tell you whether a new row was inserted.

The outbox is a database table of announcements waiting to be sent. It makes “save inquiry” and “remember to publish” atomic.

It does not make Kafka and PostgreSQL one transaction. The POST can succeed before the recipient sees a notification.

A successful commit followed by a lost HTTP response leaves the browser uncertain; the safe recovery is repeating the original key and payload.

Catalog HTTP occurs while the SQL transaction and advisory lock are held. This simplifies one logical operation but spends database connection time waiting on a network dependency. **Extension/design discussion:** bound timeouts, connection budgeting, caching owner snapshots with freshness rules, or a different operation design.

Do not casually move a dependency lookup outside the transaction without evaluating repeat semantics and race conditions.

### Listing and provider decisions

`GET /api/inquiries` runs a participant-filtered query: `client_email=$1 OR provider_email=$1`. It returns only rows where the verified actor participates, newest first, rather than loading all rows and filtering in the browser.

A valid unrelated client sees an empty array, not somebody else's inquiry.

`PATCH /api/inquiries/:id/status` requires a provider, validates an ACCEPTED/DECLINED strict body and UUID ID, then locks the row `FOR UPDATE`. Missing row is 404.

A different provider is 403. PENDING can move to either terminal status.

Repeating the same terminal choice succeeds; changing ACCEPTED to DECLINED or the reverse gives 409. Locking serializes two competing decisions.

The response is the updated view with 200. No status-changed Kafka event or notification to the client is implemented.

**Check yourself:** draw the point where an HTTP response can be lost after commit; explain why creating a fresh key after that loss can create a duplicate business request.

## Notifications: “Turn a delivered event into one durable inbox effect”

Read [NotificationsController](../../backend/src/notifications/notifications.controller.ts), [NotificationsService](../../backend/src/notifications/notifications.service.ts), [InquiryConsumer](../../backend/src/common/messaging.ts), and [notifications migration](../../backend/migrations/notifications.001.sql).

This service has two entrances: Kafka events and guarded HTTP routes. It owns a `notifications` table, not the Inquiries database.

Its `inquiry_id` is a UUID reference carried by the event; there is deliberately no cross-database foreign key.

1. Nest registers `InquiryConsumer` only in the notifications process. Its bootstrap hook starts a background loop.
2. KafkaJS creates consumer group `marketplace-notifications-v1`, connects and subscribes to the configured topic (default `inquiry.created.v1`). `fromBeginning: true` controls the starting position when the group has no usable committed offset; it does not rewind that group's saved offset on every restart.
3. `eachMessage` requires a nonempty value and parses its JSON. It awaits `NotificationsService.consume`. Malformed JSON, schema errors, or database failures throw; the code does not deliberately acknowledge a failed write and discard the event.
4. `consume` parses strict `eventSchema` with valid UUIDs/email/bounded names/subject/ISO datetime. It inserts a new notification with a generated ID and a message such as “Morgan at Acme sent a new inquiry: Build customer portal”. The message is inbox text, not an email delivery.
5. The INSERT includes `ON CONFLICT(event_id) DO NOTHING`; the migration makes event ID unique. That one SQL statement records both event identity and inbox content atomically. There is no separate inbox-receipts table. A repeated event ID has no second notification effect, even though its generated candidate notification ID would differ.
6. Only after that awaited durable operation resolves can KafkaJS complete successful message handling. KafkaJS manages offset resolution/automatic commits; it is not a separate synchronous PostgreSQL-and-Kafka commit. A crash after the SQL write and before the offset is committed may replay the event. The unique constraint makes that replay harmless. See [KafkaJS consuming documentation](https://kafka.js.org/docs/consuming).

`GET /api/notifications` returns only `recipient_email = actor.email`, with 200 and an array. `PATCH /api/notifications/:id/read` validates a UUID, locks the row, checks it exists (404), checks the actor is its recipient (403), and sets `read=true`. Repeating the read is harmless and returns 200 with the notification view.

No provider-only role restriction is applied in this controller; recipient ownership is the rule. The frontend service types this mutation as `void` because its caller ignores the returned view, but the backend actually returns it.

A malformed event can repeatedly fail and block progress for its partition. There is no implemented dead-letter topic, schema registry, quarantine UI, or operator replay tool. **Extension:** design and test a poison-event policy without silently discarding important events.

Never “fix” a learning failure by skipping offsets without understanding what data is being lost.

**Check yourself:** explain why a unique inquiry ID alone would not necessarily be a suitable event identity if more event types are added, and why email delivery is not an existing feature just because a recipient email appears in the payload.

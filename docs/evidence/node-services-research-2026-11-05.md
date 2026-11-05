# Service questionnaire builder research · November 5, 2026

Builder output: `docs/nodejs-aws-study-path/node-services-items.json`. This is research and local metadata validation, not independent approval. The final guide and archive require the separate critic’s decision.

Read the marketplace AGENTS, README, contract, requirements and architecture and the Interview process root AGENTS before writing. The NodeJs/AWS profile has no child AGENTS. Read both projects’ lessons 05–10 and16; `diff -q` produced no differences for these seven files. Read the beginner handbook mechanism headings and current controller, service, connection, health, authentication, migration and messaging source. All63 items have source-file SHA-256 values and literal excerpts captured from the actual checkout, not inferred from historical line numbers.

## Reference inspected before authoring

Opened [Devinterview Node.js repository](https://github.com/Devinterview-io/node-interview-questions) before writing. Its visible README gives useful general interview prompts but describes ordinary event-emitter callbacks as asynchronous and broadens concurrency into parallelism. Our service explanations must distinguish ordinary Node events from KafkaJS’s explicitly asynchronous instrumentation listeners. The new material adds the actual SQL/Kafka acknowledgment crash window, client-scoped retry identity, database locks and observable recovery criteria; it does not claim a benchmark win before independent comparison.

## Primary sources actually opened

The card JSON contains the exact relevant URLs. These source groups were read through the web tool on November5:

| Source | What was checked against actual project source |
|---|---|
| [Nest providers](https://docs.nestjs.com/providers), [custom providers](https://docs.nestjs.com/fundamentals/custom-providers), [controllers](https://docs.nestjs.com/controllers) | Registration, constructor injection, erased interfaces, singleton scope and named-route ordering |
| [Nest lifecycle](https://docs.nestjs.com/fundamentals/lifecycle-events), [guards](https://docs.nestjs.com/guards), [filters](https://docs.nestjs.com/exception-filters) | Awaited initialization, opt-in shutdown hooks, authorization entry and exception mapping |
| [Helmet](https://helmet.js.org/), [Express API](https://expressjs.com/en/api/), [Zod API](https://zod.dev/api), [Zod basics](https://zod.dev/basics) | Header hardening versus parsing versus runtime schemas; coercion and unknown-key policy |
| [pg queries](https://node-postgres.com/features/queries), [transactions](https://node-postgres.com/features/transactions), [pooling](https://node-postgres.com/features/pooling), [Pool API](https://node-postgres.com/apis/pool), [types](https://node-postgres.com/features/types), [TLS](https://node-postgres.com/features/ssl) | Positional values versus identifiers, same-session transactions, release/failure paths, result conversion and explicit certificate verification |
| [PostgreSQL JSON](https://www.postgresql.org/docs/current/functions-json.html), [pattern matching](https://www.postgresql.org/docs/current/functions-matching.html), [SELECT](https://www.postgresql.org/docs/18/sql-select.html), [locks](https://www.postgresql.org/docs/current/explicit-locking.html), [isolation](https://www.postgresql.org/docs/current/transaction-iso.html), [constraints](https://www.postgresql.org/docs/current/ddl-constraints.html), [INSERT](https://www.postgresql.org/docs/current/sql-insert.html), [statistics](https://www.postgresql.org/docs/current/monitoring-stats.html) | JSON/text casts, wildcard semantics, bounded batches, row/advisory locks, default isolation, durable deduplication and diagnostic views |
| [Node crypto](https://nodejs.org/api/crypto.html), [util](https://nodejs.org/api/util.html), [globals](https://nodejs.org/api/globals.html), [Buffer](https://nodejs.org/api/buffer.html), [timers](https://nodejs.org/api/timers.html) | Actual scrypt/promisify/Buffer/timeout/unref mechanics; only APIs already present in repository source are taught as implemented |
| [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [jsonwebtoken maintainer README](https://github.com/auth0/node-jsonwebtoken), [JWT specification](https://www.rfc-editor.org/rfc/rfc7519.html), [Nest authorization](https://docs.nestjs.com/security/authorization) | Password derivation versus fast hashes; signature and claim checks; actor roles versus ownership |
| [KafkaJS configuration](https://kafka.js.org/docs/configuration), [producing](https://kafka.js.org/docs/producing), [consuming](https://kafka.js.org/docs/consuming), [instrumentation](https://kafka.js.org/docs/instrumentation-events) | Broker/client/group identity, acknowledgment scope, partition order, committed-offset precedence, awaited handlers and instrumentation readiness limits |
| [RxJS official guide source](https://github.com/ReactiveX/rxjs/blob/master/apps/rxjs.dev/content/guide/observable.md) | Observable subscription/teardown worked example; custom application pipelines remain explicitly absent |
| [Fetch standard](https://fetch.spec.whatwg.org/), [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [Nest CORS](https://docs.nestjs.com/security/cors), [CSRF](https://docs.nestjs.com/security/csrf), [rate limiting](https://docs.nestjs.com/security/rate-limiting), [Express proxy trust](https://expressjs.com/en/guide/behind-proxies/), [sessions](https://expressjs.com/en/resources/middleware/session/) | Separate transport/status failures, conditional-update proposal, browser-origin protections, process-local limits, cookie sessions and proxy identity |
| [OAuth security](https://datatracker.ietf.org/doc/html/rfc9700), [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.html), [PKCE Appendix B](https://www.rfc-editor.org/rfc/rfc7636.html#appendix-B) | Federated authentication explicitly absent; useful external code-challenge vector rather than invented marketplace sign-in |
| [Nest outbox tutorial](https://docs.nestjs.com/reliability/outbox), [health guidance](https://docs.nestjs.com/recipes/terminus), [logger](https://docs.nestjs.com/techniques/logger) | Outbox dual-write explanation, external durable dead-letter example, probes and safe logs |

Current documentation can describe newer packages than the locked project. Actual backend/package.json declares Nest12.2.0; older lesson prose is not evidence of the current dependency version. CSRF built-ins described in current documentation are not configured in main.ts, so no card claims they protect this application. The outbox tutorial is an explicitly external package/version example; the marketplace uses its own SQL outbox, not `@nestjs/outbox`.

## Failures retained and repaired

- `https://node-postgres.com/api/pool` returned404. Followed the official navigation to `/apis/pool` and repaired the cards.
- The invented-looking `/reliability/transactional-outbox` could not be read. Followed Nest’s own navigation to the real `/reliability/outbox` tutorial and repaired the reference.
- Nest `/modules` and `/reliability/idempotency` repeatedly timed out. These are not claimed read: card references use the read custom-provider and PostgreSQL-constraint documentation instead.
- The current PostgreSQL SELECT URL timed out. Its official versioned PostgreSQL18 URL loaded and is used for the SELECT/batch explanations.
- The RxJS rendered guide requires JavaScript, so its official repository Markdown was opened instead.
- Node latest-v22 URLs were inaccessible to the browser tool; current Node API pages loaded. Only established APIs visible in actual project code were used; no runtime-upgrade claim is made.

## Builder checks actually executed

A local Python metadata check read all63 current source files/excerpts and checked exact hashes, symbol containment, excerpt containment, a maximum of12 lines and every lesson path. It passed. The same check compared card concept tags against every mechanism heading in lessons05–10/16: respectively7/7,7/7,7/7,9/9,7/7,8/8 and5/5; this is50 mapped headings, not a coverage percentage or independent teaching-quality verdict.

The external PKCE Appendix B vector was executed with Node `createHash('sha256')` and `digest('base64url')`, asserted using `node:assert/strict`, and printed:

```text
PKCE Appendix B vector PASS: E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
```

No AWS operation, publication, secret-value inspection, live delivery claim or application runtime acceptance was performed by this builder. Incident recovery criteria are future rehearsal checks unless final execution evidence separately records them. Extended cloud-adjacent lessons57–61/67–68 were flagged to the coordinating builder for separate coverage.

## Final builder repair before critic handoff

NSI06/NSI07 now distinguish publisher retries from a KafkaJS consumer that crashed without restart. They inspect the CRASH restart flag, membership and actual offset/insert progress; after the underlying cause is repaired, a controlled LOCAL restart retains the same group/offset/event identity. A poison record remains blocked without compatible repair or a separately implemented durable quarantine policy. No runtime repair or automatic-recovery test is claimed. NS42 also distinguishes a stalled background consumer from an updating readiness flag.

Added NS50–NS54 after inspecting lesson19’s package index and opening official [request lifecycle](https://docs.nestjs.com/faq/request-lifecycle), [pipes](https://docs.nestjs.com/pipes), [interceptors](https://docs.nestjs.com/interceptors), [configuration](https://docs.nestjs.com/techniques/configuration), [database integration](https://docs.nestjs.com/techniques/database), [Passport](https://docs.nestjs.com/recipes/passport) and [Swagger](https://docs.nestjs.com/openapi/introduction) documentation. They label custom pipe/interceptor, ConfigModule, ORM, Passport and generated OpenAPI implementations absent and supply external worked examples. Source alternatives remain literal current code. Final section:54 questions and9 incidents; every item retains a source hash/excerpt and lesson links.

## Critic terminology and lesson-provenance repair

NS34 now says the inquiry row is locked, correcting the ambiguous “provider’s row” wording. Added explicit `lesson_relation` metadata to NS46/NS47: their security/reliability lessons are prerequisites, not evidence those lessons teach CORS/CSRF/sessions/OAuth/OpenID Connect/PKCE. Also marked the corresponding prerequisite-versus-researched-extension relationship for NS19/NS49/NS50–NS54 and clarified taught comparison versus external example for NS07/NS45/NSI07. No original lesson was edited; external examples remain labeled absent implementation.

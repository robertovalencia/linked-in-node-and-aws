# 5. Read the language before memorizing the framework

[Guide index](README.md) · [Previous: practice](04-debugging-and-practice.md)

Use this beside the source. Small examples are explanations, not requested changes to the application.

Try them in a scratch file outside the service source, predicting the result first.

## JavaScript values and functions

| Construct | Plain explanation | Real use to find |
|---|---|---|
| `const` / `let` | Bind a name; const prevents rebinding, not every change inside an object | `const input`; `let response` in [InquiriesService](../../backend/src/inquiries/inquiries.service.ts) |
| Object / array | Named properties versus an ordered list | Event object versus fingerprint's fixed-order array |
| Function / arrow | Reusable code; arrows capture surrounding lexical this | `fingerprint(input)` versus `async (client) => {...}` |
| Closure | Function retains values from where it was defined | Transaction callback uses actor, key, input |
| Destructuring | Pull properties into names | `{ ownerEmail, ...document }` in [CatalogService](../../backend/src/catalog/catalog.service.ts) |
| Spread `...` | Expand properties/items; later object properties override earlier ones | Preserving stored reputation metrics over submitted values |
| `.map` / `.filter` | Transform each item / keep matching items | Response view mapping; migration filtering |
| `Map` / `Set` | Key-value collection / unique-value collection | Login attempt counters; comparison deduplication |
| `?.` / `??` | Read only if present / fallback only for null or undefined | `account?.password_hash`; default PORT |
| Template literal | Backtick text with an embedded expression | Internal URL; distinct from SQL parameterization |
| Regex | Match a pattern | Slug/idempotency-key checks |
| `JSON.stringify/parse` | Convert values to text / parse text into values | HTTP/event body; parsing is not schema validation |
| `Date`, `URL`, `URLSearchParams` | Built-in date and URL handling | ISO dates; config checks; search query |

```js
const submitted = { name: 'Ava', rating: 5 };
const saved = { ...submitted, rating: 4 };
console.log(saved.rating); // 4: later property wins
```

Explain why this ordering matters in profile update security.

## Promises, errors, and the event loop

A Promise represents a future result or rejection. `async` returns a Promise. `await` suspends that function until the Promise settles while the event loop can handle other work. It does not create a database transaction or serialize incoming requests.

CPU-heavy synchronous JavaScript still blocks the event loop; async I/O does not make arbitrary CPU work parallel.

`try/catch` handles thrown errors and awaited rejections. `finally` performs cleanup on success or failure. Find the guaranteed client release in [Database.transaction](../../backend/src/common/database.ts).

Calling an async function without awaiting/handling it can detach important work from a caller. [Messaging bootstrap](../../backend/src/common/messaging.ts) intentionally launches `void this.run()` as a background loop with its own error handling; startup has not waited for delivery to finish.

```js
async function example() {
  console.log('A');
  await new Promise(resolve => setTimeout(resolve, 0));
  console.log('C');
}
const pending = example();
console.log('B');
await pending;
```

Expected A, B, C. Explain how two async inquiry handlers can interleave, and why a boolean in one process cannot enforce idempotency across replicas.

## TypeScript checks disappear at runtime

| Construct | Meaning | Source |
|---|---|---|
| `type Actor = ...` | Compiler's expected shape | [auth.ts](../../backend/src/common/auth.ts) |
| `'CLIENT' \| 'PROVIDER'` | Union: one of these values | Actor role |
| `unknown` | Input needs checking before trusted use | Request/event bodies |
| Narrowing | Runtime checks establish a more precise type | `typeof` checks in verifyActor |
| Generic `<T>` | Relates input/output types in reusable code | `transaction<T>`; frontend `api<T>` |
| `Promise<T>` | Async result eventually has type T | Password helper |
| `z.infer<typeof schema>` | Derive static type from runtime schema | [provider.schema.ts](../../backend/src/catalog/provider.schema.ts) |
| `import type` | Compiler-only import erased from JS | Express request type |
| `as` | Compiler assertion, not runtime conversion/check | Request casts |
| `as const` | Retains narrow literal types | SERVICES tuple |
| `private readonly` | Restricts field access/reassignment in TypeScript | Injected database parameter property |
| Interface / `implements` | Class promises a method contract | Nest lifecycle interfaces |

A budget JSON string and a budget JSON number differ. Inquiry schema requires a number.

Query schema deliberately coerces number values because URLs contain strings. `as number` would not convert or validate untrusted data.

## Node APIs actually used

| API | Purpose and limit | Find it |
|---|---|---|
| `process.env/cwd/exitCode`, signals | Config, runtime directory, failure status, shutdown | [config](../../backend/src/common/config.ts), [main](../../backend/src/main.ts), [launcher](../../scripts/dev.mjs) |
| `node:fs/promises` readFile/readdir | Async file reads/listing | Migrations and seeds |
| `node:path` join/resolve/dirname | OS file paths | Database runner/launchers |
| `node:url` fileURLToPath | Module URL into filesystem path | Root launcher |
| `node:crypto` randomUUID/randomBytes | Secure random IDs/salts | Inquiries, Notifications, password helper |
| `createHash('sha256')` | Deterministic digest | Migration checksum; request fingerprint |
| `scrypt` + `promisify` | Callback password derivation adapted to Promise | [password.ts](../../backend/src/identity/password.ts) |
| Buffer, timingSafeEqual | Bytes/hex and length-compatible safe equality | Password/internal-key verification |
| Global fetch / AbortSignal.timeout | Native HTTP with deadline | Catalog lookup; no Axios |
| setTimeout / unref | Pause retry; timer alone need not keep process alive | Messaging loop |
| child_process spawn | Start compiler/watch/processes | Dev scripts |
| fs readFileSync | Synchronous startup read | Root launcher; not request-path persistence |

An ID is not a secret; an internal service key is. A checksum is not a password hash.

A Buffer is bytes, not a decoded JSON object. Practice those distinctions before using crypto as one vague concept.

## Nest and runtime dependencies

`@Controller` declares route ownership; `@Get/@Post/@Put/@Patch` choose method/path. `@Body/@Param/@Query/@Headers/@Req` select request data. `@Injectable` marks Nest-managed classes; `@Module` registers controllers/providers. `@UseGuards` runs authentication; `@Catch` marks a filter. A decorator attaches framework metadata; it does not replace business logic inside a method.

`@nestjs/core` bootstraps; `@nestjs/common` provides decorators/exceptions/lifecycle contracts; `@nestjs/platform-express` provides HTTP adaptation. `reflect-metadata` supports constructor-injection metadata. RxJS is installed for framework interoperability, but application code does not implement an Observable business pipeline.

An installed package does not imply its every feature is used.

Helmet sets protective HTTP headers. jsonwebtoken signs/verifies JWTs. Zod validates runtime input. pg supplies explicit SQL/pooling: no ORM.

KafkaJS talks to Kafka directly: no Nest microservices transport. Lifecycle hooks initialize and clean up; they are not HTTP endpoints.

There is no ConfigModule, global ValidationPipe, Passport, Swagger generator, Prisma/TypeORM, or CQRS package to find. Those can be later extension topics.

Environment config is checked manually in `validateConfig`; HTTP/event schemas are parsed explicitly with Zod.

## SQL and messaging vocabulary

| Term | Meaning in this application |
|---|---|
| Pool | Limited reused database connections |
| Parameterized SQL | Separate `$1/$2` values from query syntax |
| JSONB | Queryable structured document column |
| Transaction | One connection's statements commit or roll back together |
| FOR UPDATE | Lock selected rows during decision/update |
| Advisory lock | Application-selected key; same client/key coordination |
| SKIP LOCKED | Skip rows held by another worker |
| Unique constraint | Database invariant even when requests race |
| Migration/checksum | Versioned schema change; detect edited applied history |
| Outbox | Durable publish intent saved with inquiry |
| Inbox effect | Notification row; unique event_id records receipt and prevents duplicate effect |
| Topic/partition/key | Stream name/ordered subdivision/routing input; no global ordering guarantee |
| Consumer group/offset | Workers sharing consumption/saved partition position |
| At least once | Handling may repeat after a failure |
| Idempotent effect | Same operation identity produces no second business effect |
| Eventual consistency | Inbox catches up after inquiry commit |
| Poison event | Unprocessable message; no automatic quarantine implemented |
| Ready/live | Dependency-aware eligibility signal/basic process-handler reachability |

## React and tools

A component renders UI from props/state. Props are parent inputs.

State persists across renders; updates ask React to render again. A ref holds a mutable value without causing rendering—useful for `inFlight`, not durable data.

Context supplies shared state; AuthProvider supplies identity. Hooks bundle reusable behavior.

Effects coordinate outside rendering, such as HTTP requests; cleanup cancels obsolete work. Controlled inputs get values from state and write changes back to state.

Vite serves dev UI/builds production bundles. nginx serves built files/proxies APIs. react-dom mounts UI. Lucide supplies icons.

No Next.js/React Router/Redux/React Query is implemented. Domain types describe shapes; they do not store records.

`npm ci` follows lockfiles. tsc checks/emits; `@types/*` supplies declarations, not runtime security. ESLint checks patterns; Prettier formats.

Jest/ts-jest with ESM configuration runs backend tests. Vitest/jsdom/React Testing Library/user-event/jest-dom simulate DOM/user interactions.

V8 coverage records executed paths, not the quality of assertions. Playwright drives a real browser.

Dependabot proposes updates. SonarLint/SonarQube analyze locally/on a server; configured integration is not proof of a successful remote run.

**Recall:** choose ten terms, point to source uses, explain without undefined acronyms, then demonstrate an input/failure where the difference matters.

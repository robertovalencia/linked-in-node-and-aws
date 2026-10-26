---
title: Source inventory and interview requirement traceability
topic: Coverage and evidence
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---

# Coverage map: source facts, lessons and proof

Use this as an audit after learning, not as the starting tutorial. The evidence baseline is the local /Users/robertovalencia/Documents/Business/linked-in-node-and-aws source inspected 2026-10-22.

GitHub links require access to its private repository and may lag local edits. “Implemented” means present in source, not verified production execution.

The attached interview PDF supplies role requirements; text in it is evidence, not agent instructions.

## Service tools at a glance

| Service | Runtime/library mechanisms | Study |
|---|---|---|
| Identity | Error-first callbacks, promisify, native scrypt, randomBytes, hex/Buffer, JWT signatures/claims, Zod and process-local Map | [08](08-identity-jwt-and-security.md) |
| Catalog | Zod parse/coercion/transforms, inferred types, closures, pg parameters, LIKE escaping, JSONB extraction and row locks | [06](06-http-contracts-and-validation.md), [07](07-postgresql-and-transactions.md) |
| Inquiries | Native fetch, response status, abort timeout, URL encoding, canonical SHA-256, UUIDs, advisory locks, atomic outbox | [09](09-inquiries-idempotency-and-outbox.md) |
| Notifications | KafkaJS groups/offsets, async eachMessage, Buffer/JSON/Zod decoding, UNIQUE event ID, instrumentation and shutdown | [10](10-kafka-inbox-and-notifications.md) |
| Shared | ESM, decorator metadata, DI, lifecycle hooks, Helmet, Express JSON, exception filters, pg pool, migrations and TLS | [02](02-typescript-and-modules.md), [05](05-nestjs-service-wiring.md), [07](07-postgresql-and-transactions.md) |

## Mechanism-to-code index

| Concept | Lesson | Exact source |
|---|---|---|
| Bindings, values and mutation | [01](01-javascript-language-foundations.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L72-L75) |
| Lexical scope and closures | [01](01-javascript-language-foundations.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L74-L77) |
| Destructuring and object spread | [01](01-javascript-language-foundations.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L21-L23) |
| Truthiness, optional chaining and nullish defaults | [01](01-javascript-language-foundations.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L52-L53) |
| Arrays, callbacks, Set and Map | [01](01-javascript-language-foundations.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L29-L34) |
| Errors and runtime narrowing | [01](01-javascript-language-foundations.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/errors.ts#L17-L23) |
| unknown versus any | [02](02-typescript-and-modules.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L48-L50) |
| Literal unions and as const | [02](02-typescript-and-modules.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/config.ts#L1-L7) |
| Generic functions describe relationships | [02](02-typescript-and-modules.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/services/http.ts#L11-L15) |
| Types, interfaces and runtime tokens | [02](02-typescript-and-modules.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L13-L13) |
| ES modules and emitted file paths | [02](02-typescript-and-modules.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L6-L6) |
| Decorator metadata is a compiler/runtime agreement | [02](02-typescript-and-modules.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/tsconfig.json#L10-L13) |
| await suspends one continuation | [03](03-node-runtime-and-async.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L47-L50) |
| Worker pool versus JavaScript CPU work | [03](03-node-runtime-and-async.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L6-L7) |
| Promise aggregation is not a concurrency limiter | [03](03-node-runtime-and-async.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L123-L127) |
| Timers, delays and unref | [03](03-node-runtime-and-async.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L8-L12) |
| Detached promises need their own error policy | [03](03-node-runtime-and-async.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L22-L24) |
| Connection budgets create backpressure | [03](03-node-runtime-and-async.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L12-L13) |
| HTTP parsing versus application validation | [04](04-node-http-processes-and-streams.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L46-L47) |
| Buffer measures bytes | [04](04-node-http-processes-and-streams.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/config.ts#L17-L18) |
| fs/promises and bounded file reads | [04](04-node-http-processes-and-streams.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L31-L35) |
| cwd versus module location | [04](04-node-http-processes-and-streams.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L31-L31) |
| Child processes and watch mode | [04](04-node-http-processes-and-streams.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/scripts/dev.mjs#L1-L6) |
| Signals and graceful resource cleanup | [04](04-node-http-processes-and-streams.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L48-L52) |
| Decorators attach metadata | [05](05-nestjs-service-wiring.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L1-L3) |
| The dependency-injection container | [05](05-nestjs-service-wiring.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L36-L40) |
| Constructor parameter properties | [05](05-nestjs-service-wiring.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L13-L13) |
| Lifecycle hooks and awaited setup | [05](05-nestjs-service-wiring.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L11-L14) |
| Middleware: Helmet and the JSON parser | [05](05-nestjs-service-wiring.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L45-L47) |
| Guards and exception filters | [05](05-nestjs-service-wiring.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/errors.ts#L16-L22) |
| RxJS: installed versus used | [05](05-nestjs-service-wiring.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L32-L32) |
| Zod parse: a runtime boundary | [06](06-http-contracts-and-validation.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L70-L73) |
| Coercion, transforms and defaults | [06](06-http-contracts-and-validation.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L54-L59) |
| Strict objects and inferred types | [06](06-http-contracts-and-validation.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L48-L50) |
| Closures build positional SQL parameters | [06](06-http-contracts-and-validation.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L74-L77) |
| JSONB operators and explicit casts | [06](06-http-contracts-and-validation.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L89-L92) |
| Escaping LIKE patterns versus SQL parameters | [06](06-http-contracts-and-validation.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L79-L82) |
| Row locks and server-owned fields | [06](06-http-contracts-and-validation.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L59-L64) |
| Pool versus connection | [07](07-postgresql-and-transactions.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L10-L14) |
| pool.query versus checked-out client | [07](07-postgresql-and-transactions.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L70-L75) |
| try, catch and finally protect resources | [07](07-postgresql-and-transactions.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L76-L82) |
| Parameters and result conversion | [07](07-postgresql-and-transactions.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L48-L51) |
| Row locks versus advisory locks | [07](07-postgresql-and-transactions.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L92-L94) |
| Migration checksums: filesystem plus crypto | [07](07-postgresql-and-transactions.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L46-L50) |
| Pool events and TLS settings | [07](07-postgresql-and-transactions.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L17-L20) |
| Error-first callbacks become promises | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L3-L3) |
| scrypt: cost and asynchronous work | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L6-L7) |
| randomBytes, salt and hex encoding | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L5-L7) |
| Buffer and timingSafeEqual | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L18-L18) |
| Optional chaining and a dummy derivation | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L52-L54) |
| JWT signing: claims, encoding and HMAC | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/auth.ts#L14-L21) |
| jsonwebtoken: signature versus claims | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/auth.ts#L24-L29) |
| Map-based throttling and mutable objects | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.controller.ts#L26-L30) |
| Zod validates before service use | [08](08-identity-jwt-and-security.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.controller.ts#L15-L17) |
| Native fetch and two failure channels | [09](09-inquiries-idempotency-and-outbox.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L72-L75) |
| AbortSignal.timeout and URL encoding | [09](09-inquiries-idempotency-and-outbox.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L61-L65) |
| SHA-256 fingerprint versus retry key | [09](09-inquiries-idempotency-and-outbox.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L16-L25) |
| randomUUID: record identity is separate | [09](09-inquiries-idempotency-and-outbox.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L105-L107) |
| Advisory locking across async handlers | [09](09-inquiries-idempotency-and-outbox.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L91-L99) |
| Outbox: one database transaction, two records | [09](09-inquiries-idempotency-and-outbox.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L135-L140) |
| Constraints and state transitions | [09](09-inquiries-idempotency-and-outbox.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/migrations/inquiries.001.sql#L6-L7) |
| KafkaJS client, producer and consumer | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L133-L141) |
| Message keys and acknowledgments | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L31-L35) |
| SKIP LOCKED and bounded batches | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L28-L29) |
| Consumer groups and starting offsets | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L101-L104) |
| Buffer → UTF-8 → JSON → Zod | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L110-L110) |
| Unique event IDs make duplicate effects harmless | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31) |
| Timers, unref and detached promises | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L8-L12) |
| Instrumentation events update readiness | [10](10-kafka-inbox-and-notifications.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L90-L99) |
| Component functions and render snapshots | [11](11-react-foundations-and-state.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L7-L10) |
| Props and callback contracts | [11](11-react-foundations-and-state.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/inquiries/InquiryForm.tsx#L7-L16) |
| Controlled inputs and explicit conversion | [11](11-react-foundations-and-state.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/inquiries/InquiryForm.tsx#L42-L44) |
| Immutable updates and identity | [11](11-react-foundations-and-state.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L152-L154) |
| Refs versus state | [11](11-react-foundations-and-state.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useInquiryAttempt.ts#L41-L44) |
| Context and custom hooks | [11](11-react-foundations-and-state.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/contexts/AuthContext.tsx#L48-L50) |
| Effect setup and cleanup | [12](12-react-effects-http-and-accessibility.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L57-L63) |
| Abort plus stale-response guards | [12](12-react-effects-http-and-accessibility.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L73-L76) |
| fetch errors versus HTTP rejection | [12](12-react-effects-http-and-accessibility.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/services/http.ts#L24-L29) |
| Storage and transport recovery | [12](12-react-effects-http-and-accessibility.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useInquiryAttempt.ts#L58-L64) |
| Portals and DOM ownership | [12](12-react-effects-http-and-accessibility.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/common/Modal.tsx#L96-L101) |
| Refs keep a fresh callback | [12](12-react-effects-http-and-accessibility.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/components/common/Modal.tsx#L47-L50) |
| Jest spies isolate a service rule | [13](13-testing-and-debugging.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/test/workflows.spec.ts#L43-L51) |
| Vitest and controllable promises | [13](13-testing-and-debugging.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.test.tsx#L13-L20) |
| TypeScript transformation and ESM | [13](13-testing-and-debugging.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L51-L58) |
| Lint, format, typecheck and behavior | [13](13-testing-and-debugging.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L18-L23) |
| Playwright exercises a real browser | [13](13-testing-and-debugging.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/scripts/browser-smoke.mjs#L12-L15) |
| npm scripts and separate package scopes | [14](14-local-runtime-and-containers.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/package.json#L10-L13) |
| tsc emits; node executes | [14](14-local-runtime-and-containers.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/Dockerfile#L7-L13) |
| Docker image versus container | [14](14-local-runtime-and-containers.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/compose.yaml#L2-L9) |
| Container DNS and published ports | [14](14-local-runtime-and-containers.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/compose.yaml#L31-L34) |
| Child-process supervision and inspectors | [14](14-local-runtime-and-containers.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/scripts/dev.mjs#L6-L11) |
| Terraform resources, references and plans | [15](15-aws-terraform-and-delivery.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L13-L17) |
| Security groups and the actual access path | [15](15-aws-terraform-and-delivery.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L30-L36) |
| IAM roles and GitHub OIDC | [15](15-aws-terraform-and-delivery.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L122-L125) |
| ECR tags, digests and immutability | [15](15-aws-terraform-and-delivery.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L46-L52) |
| Secrets Manager and scoped reads | [15](15-aws-terraform-and-delivery.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L90-L98) |
| State storage, encryption and locking | [15](15-aws-terraform-and-delivery.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/bootstrap/main.tf#L16-L23) |
| Azure equivalents require a fresh design | [15](15-aws-terraform-and-delivery.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/docs/azure-mapping.md#L1-L5) |
| A timeout is one bounded wait | [16](16-reliability-and-senior-design.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/inquiries/inquiries.service.ts#L64-L64) |
| Liveness versus readiness | [16](16-reliability-and-senior-design.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/health.ts#L19-L23) |
| At-least-once delivery and idempotent effect | [16](16-reliability-and-senior-design.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31) |
| Shared build versus independent failure domains | [16](16-reliability-and-senior-design.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L30-L35) |
| Concurrency protection versus stale-user conflict | [16](16-reliability-and-senior-design.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/catalog.service.ts#L52-L54) |
| A specification is an executable-review target | [17](17-ai-assisted-engineering-and-toolchain.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/CONTRACT.md#L1-L6) |
| GitHub Actions jobs and dependency order | [17](17-ai-assisted-engineering-and-toolchain.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/workflows/verify.yml#L12-L19) |
| SonarLint versus a server quality gate | [17](17-ai-assisted-engineering-and-toolchain.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/workflows/deploy-dev.yml#L41-L42) |
| Dependabot and dependency-change review | [17](17-ai-assisted-engineering-and-toolchain.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/dependabot.yml#L2-L9) |
| OIDC, release manifests and serialization | [17](17-ai-assisted-engineering-and-toolchain.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/scripts/aws-remote-deploy.sh#L7-L11) |
| Jira, VS Code and architect collaboration | [17](17-ai-assisted-engineering-and-toolchain.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/docs/traceability.md#L1-L6) |
| Explain a callback-to-promise adapter | [18](18-interview-drills-and-capstone.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L3-L3) |
| Explain a validated runtime boundary | [18](18-interview-drills-and-capstone.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/catalog/provider.schema.ts#L54-L59) |
| Explain a transaction without hand-waving | [18](18-interview-drills-and-capstone.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L70-L76) |
| Explain a duplicate message | [18](18-interview-drills-and-capstone.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/notifications/notifications.service.ts#L30-L31) |
| Explain a stale React response | [18](18-interview-drills-and-capstone.md) | [Code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.test.tsx#L12-L15) |

## How to use the matrix

For every row name the source, explain the concept, complete its lab and record observed evidence. A lesson number means the linked guide in this profile, not a claim that reading completed the skill.

Stage an actual diff only in a practice copy/branch. External paid/cloud operations, messages and publication are separate actions; a local written plan can satisfy the learning checkpoint without inventing external completion.

## Direct dependency coverage

| Package or family present | Actual role and source | Lesson | Demonstration |
|---|---|---|---|
| @nestjs/common | Decorators, guards, lifecycle types, exceptions | [05](05-nestjs-service-wiring.md), [06](06-http-contracts-and-validation.md) | Draw graph and trace rejected request |
| @nestjs/core | NestFactory and application container | [05](05-nestjs-service-wiring.md) | Explain configured bootstrap |
| @nestjs/platform-express | HTTP adapter; Express json middleware imported via resolved dependency | [04](04-node-http-processes-and-streams.md), [05](05-nestjs-service-wiring.md) | Explain 128kb parser and route |
| helmet | HTTP security headers in main.ts | [08](08-identity-jwt-and-security.md) | Inspect headers; explain limited scope |
| jsonwebtoken | Sign/verify HS256 actor | [08](08-identity-jwt-and-security.md) | Tampered/invalid issuer/role cases |
| kafkajs | Producer/consumer/worker connection events | [10](10-kafka-inbox-and-notifications.md) | Crash table and duplicate replay |
| pg | Pool, SQL, checked-out transaction client | [07](07-postgresql-and-transactions.md) | Rollback and row-lock experiment |
| reflect-metadata | Runtime metadata support loaded before Nest bootstrap | [02](02-typescript-and-modules.md), [05](05-nestjs-service-wiring.md) | Explain decorator/DI contract |
| rxjs | Installed framework dependency; no application Observable pipeline | [02](02-typescript-and-modules.md), below | Explain Promise versus Observable; label extension |
| zod | Explicit runtime HTTP/event/schema validation | [06](06-http-contracts-and-validation.md) | Malformed body/query/event rejection |
| react, react-dom | Render/state/effects/context/root/portals | [11](11-react-foundations-and-state.md), [12](12-react-effects-http-and-accessibility.md) | State snapshot and modal cleanup |
| lucide-react | UI icon components | [12](12-react-effects-http-and-accessibility.md) | Verify icon button accessible name |
| typescript | Strict backend/frontend compile checking | [02](02-typescript-and-modules.md) | Narrowing failure/repair |
| @types/node/express/jest/jsonwebtoken/pg/react/react-dom | Declaration packages; do not change runtime behavior | [02](02-typescript-and-modules.md) | Explain type versus value import |
| eslint, @eslint/js, typescript-eslint, globals | JS/TS lint configuration; majors differ across packages | [13](13-testing-and-debugging.md) | Useful lint violation and repair |
| eslint-plugin-react-hooks | Hooks order/dependency diagnostics | [12](12-react-effects-http-and-accessibility.md) | Diagnose a missing effect dependency |
| prettier | Code formatting | [13](13-testing-and-debugging.md) | Format failure distinguished from behavior failure |
| jest, ts-jest | Backend test runner and TS/ESM transformation | [13](13-testing-and-debugging.md) | Focused regression with ESM config understood |
| vitest, @vitest/coverage-v8 | Frontend test runner/instrumentation | [13](13-testing-and-debugging.md) | Branch behavior and coverage scope |
| @testing-library/react, user-event, jest-dom | Component render/user behavior/assertions | [11](11-react-foundations-and-state.md), [12](12-react-effects-http-and-accessibility.md) | Labeled input, focus, error/success assertions |
| jsdom | DOM-like test environment; not full browser/network | [13](13-testing-and-debugging.md) | Contrast component and Playwright evidence |
| vite, @vitejs/plugin-react | Dev server, React transform, build and API proxy | [14](14-local-runtime-and-containers.md) | Explain Vite5183 versus nginx8180 |
| playwright | Root browser smoke tooling | [13](13-testing-and-debugging.md) | Real browser journey with actual server |
| js-yaml override | Transitive dependency override in backend package | [13](13-testing-and-debugging.md), [17](17-ai-assisted-engineering-and-toolchain.md) | Review lockfile/security rationale; not application YAML API |

### Does RxJS mean this application is reactive?

The package is installed for framework compatibility, but application code uses promises and KafkaJS callbacks rather than custom Observable operators. A Promise represents one eventual settlement; an Observable can represent a stream with subscription/unsubscription semantics.

A proposed learning extension can convert repeated events to a bounded Observable and handle teardown, but do not claim KafkaJS handlers already use RxJS or that streams automatically provide safe backpressure. Explain the actual mechanism before choosing another abstraction.

## Used Node/JavaScript/TypeScript pattern coverage

| Pattern/API in source | Where to read | Lesson/lab |
|---|---|---|
| const/let, coercion, truthiness, equality, object identity | catalog.service.ts; query schemas | 01 filter/copy/coercion |
| Closures, arrows/this, classes, array map/filter, spread/rest/destructure, Map/Set | catalog.service.ts; identity.controller.ts; useMarketplace.ts | 01 closure/copy and 11 state |
| Optional chaining/nullish fallback, regex, JSON, Date, URL/URLSearchParams | config/auth/schema and frontend hooks | 01, 04, 06 query boundary |
| unknown/narrowing, literal unions, generics, Record, ReturnType, Omit, type-only imports | config.ts, main.ts, http.ts, types | 02 compiler repair |
| ESM imports/exports, .js suffix, metadata/decorators | main.ts, tsconfig.json, package.json | 02/05 emitted-JS/DI trace |
| async/await, promises, catch/finally, bounded concurrency | all services, hooks | 03 concurrency runner |
| process.env/cwd/exitCode and signals | main/config/database and dev scripts | 04/14 wrong cwd and shutdown |
| readFile/readdir, path join | database.ts and seed bootstrap | 04 small-file/stream contrast |
| createHash/randomUUID/randomBytes/scrypt/timingSafeEqual, util.promisify | password.ts, auth/catalog/inquiries | 08 password + 09 fingerprint |
| Buffer UTF-8/hex/byteLength | config/password/messaging | 04 byte length experiment |
| Native fetch, AbortSignal.timeout and AbortController | inquiries.service.ts; frontend effects | 09 timeout and 12 stale-response repair |
| Timers, unref and cancellation | messaging.ts; toast effect | 03 timer blocking; 12 cleanup |
| child_process.spawn, readFileSync, fileURLToPath, dirname/resolve, process groups | scripts/dev.mjs; backend/scripts/dev.mjs | 14 inspect start/output/shutdown |
| Node HTTP/streams/backpressure/worker threads | Learning extension, not custom app implementation | 04 server/copy; 03 CPU alternatives |

## Service and frontend behavior coverage

| Actual capability/pattern | Source anchor | Lesson and observable proof |
|---|---|---|
| Four processes from SERVICE-selected module | backend/src/main.ts | 05 graph/ports/DI error |
| Config validation, body cap, error masking | common/config.ts, errors.ts | 04/06 invalid env/body/status |
| Service DB ownership, max10 pools, migrations/checksums/advisory lock/TLS | common/database.ts, migrations, init-databases.sh | 07 rollback/migration explanation |
| Seed-only demo accounts and profiles | identity/catalog service bootstrap | 05/08 explain SEED_DEMO |
| Login throttle, scrypt dummy hash, JWT guard | identity/, common/auth.ts | 08 security test |
| Public search/detail, private owner lookup, protected update preserving ratings | catalog/ | 06/07/08 contract/owner tests |
| CLIENT inquiry creation, canonical retry, unique lock identity | inquiries.service.ts + migration | 09 same/different payload table |
| Native internal fetch inside DB transaction | inquiries.service.ts | 03/09 pool and timeout tradeoff |
| Participants-only listing, target-provider locked state transitions | inquiries.service.ts | 16/18 state/ownership tests |
| Outbox batch25 SKIP LOCKED and acknowledged send | common/messaging.ts | 10 ack/commit crash table |
| Consumer group offsets/readiness; idempotent insert | messaging.ts, notifications.service.ts | 10 replay/poison-event limits |
| Recipient-only inbox/read state, no separate inbox receipt table | notifications/, notifications.001.sql | 08/10 owner and unique eventId |
| Health live/ready/worker flags | common/health.ts | 05/16 dependency failure reasoning |
| StrictMode, context, custom hooks, controlled forms, props/types | frontend/src/main.tsx, contexts/, hooks/, components/ | 11/12 snapshot/input trace |
| Central fetch/error helper and no runtime decoder in api<T> | frontend/src/services/http.ts | 02/12 error/abort distinctions |
| Submitted search, page/filter/compare max3, Promise.all, lazy storage | useMarketplace.ts | 11/12 list/compare/race lab |
| Token restore with abort+identity check | AuthContext.tsx | 12 stale-session test |
| Pending inquiry payload+key in sessionStorage, frozen uncertainty, refs | useInquiryAttempt.ts | 09 transport retry evidence |
| Portals, focus trap, inert background, latest callback ref, scroll cleanup | Modal.tsx | 12 keyboard and nested-dialog test |
| Vite/nginx same-origin proxy; domain data API-owned | vite.config.ts; frontend/nginx.conf | 14 browser→API route |

Read the verified filename links below, including frontend/nginx.conf. Do not infer a package such as React Router, Redux, React Query, Axios, Prisma, TypeORM, Passport, Nest ConfigModule, class-validator, Swagger or Nest microservices transport: those are absent here.

## Infrastructure and delivery coverage

| Current source capability | Lessons/proof |
|---|---|
| Separate npm scopes/lockfiles, Node22 Docker/CI, tsc + node watch, nonroot multi-stage image | 02/14 installation and process map |
| Isolated Compose ports/data, Postgres17.6 four DB/logins, Kafka4 KRaft one broker | 14 topology; 10 durability limits |
| AWS VPC/subnet/IGW/routes, no-ingress SG, AL2023 EC2, encrypted disk/IMDSv2 | 15 actual network/IAM diagram |
| SSM host access/tunnel, runtime Secrets Manager secret metadata/value separation | 15 request path and secret boundaries |
| ECR immutable repos/scans, private versioned SSE-S3 releases bucket, scoped roles | 15 release artifact trace |
| GitHub environment-constrained OIDC and S3/SSM digest deployment | 15/17 exact commit/digest/manifest |
| Private/versioned AES256 state bucket, locking, optional OIDC bootstrap; no custom KMS resource | 15 state/plan/apply; KMS proposal labeled |
| Verify lint/types/coverage/build/audit; Docker acceptance/browser; Terraform checks | 13/17 job graph and actual output |
| Sonar configured gate, Dependabot, VS Code and Jira import | 17 configuration versus observed integration |
| Smoke/rollback scripts, Trivy high/critical image scan and release evidence | 15/17 explain actual workflow; execution separately proven |
| Managed DB/broker, ECS/serverless/public TLS/observability/backup restore and Azure | 15/16 proposed extensions with cost/recovery reasoning |

## Interview PDF requirement matrix

These role IDs are defined here and intentionally prefixed ROLE to avoid confusing them with the application's separate R01–R12 specification IDs.

| ID | Role requirement evidence | Lesson | Required demonstration |
|---|---|---|---|
| ROLE01 | AI-first approximately95% application code using Claude Code | 17 | Bounded agent workflow; distinguish target, tool and measurement |
| ROLE02 | Turn business/technical needs into plans/specifications | 06/17/18 | Written capstone acceptance/edge cases/constraints |
| ROLE03 | Direct Claude Code during implementation | 17 | Small task, source context, feedback and repaired diff |
| ROLE04 | Heavy AI-assisted/vibe development | 17 | Working iterative slice with human accountability |
| ROLE05 | Review/validate generated code | 08/13/17 | Detect injected missing-owner check and repair |
| ROLE06 | Test/troubleshoot/correct/refine requirements | 12/13/18 | Failing behavioral test, diagnosis and passing repair |
| ROLE07 | Follow architecture/security/testing/docs/coding standards | 05–10/13/17 | ADR, contract, security negative tests and checks |
| ROLE08 | Collaborate with architect | 16/17 | Explain alternatives, recommendation and unresolved decision |
| ROLE09 | Complete development toolchain | 14/17 | Reproducible lockfile setup, debug and configuration map |
| ROLE10 | Automate builds/tests/quality/deployments/releases | 13/15/17 | Explain jobs/gates/digests/smoke/rollback; actual run evidence if available |
| ROLE11 | Requirements-to-release traceability | 17 | One completed-stage chain; unexecuted stages labeled |
| ROLE12 | React, TypeScript, Node, Nest, PostgreSQL | 01–14/18 | Explain and test a vertical feature |
| ROLE13 | Azure, AWS, Terraform | 15/16 | Actual AWS IaC explanation plus explicit Azure comparison/proposed lab |
| ROLE14 | Jira, VS Code, Claude Code, GitHub | 17 | Draft ticket, breakpoint, agent task and reviewable PR draft |
| ROLE15 | GitHub Actions and Terraform | 15/17 | Pipeline/IAM/state/plan walkthrough |
| ROLE16 | ESLint, Prettier, Vitest/Jest | 13 | Distinct useful failure/repair examples |
| ROLE17 | Dependabot, SonarLint/SonarQube | 13/17 | Review dependency change and editor/server gate distinction |

## Project specification coverage

The application's docs/specs/requirements.md R01–R12 map respectively to discovery(06/11/12), profiles/comparison(07/11), auth(08), owned updates(07/08), durable inquiries(09), lifecycle(16/18), eventual inbox(10), React architecture(11/12), local setup(14), AWS dev(15), delivery toolchain(13/17), and AI traceability(17). Reuse actual acceptance/test names when documenting proof; a lesson number alone is not a passed requirement.

## Coverage verification lab and mastery

Run npm --prefix backend ls --depth=0 and npm --prefix frontend ls --depth=0 after lockfile installation. Compare every direct dependency with this matrix.

Inspect package.json, backend/src, frontend/src, infra and .github when a row appears to drift. Choose one actual behavior, follow its source and tests, then explain it without reading.

Record any newly observed gap in your notebook and extend the appropriate lesson rather than checking it complete by assumption.

- [ ] Every direct package family and actually used runtime pattern has a lesson.
- [ ] Every role requirement has a concrete demonstration and honest status.
- [ ] Every architecture claim is grounded in code; docs discrepancies are called out.
- [ ] Proposed extensions are distinguishable from implemented and executed behavior.

## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases.

Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Project source: package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/package.json#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/package.json#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/package.json#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/specs/requirements.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/docs/specs/requirements.md#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/main.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/nginx.conf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/nginx.conf#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/aws-dev/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/bootstrap/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/bootstrap/main.tf#L1-L8) — local baseline inspected 2026-10-22; private published source may lag.


## Expanded AWS/Terraform coverage

| Learning area | Stepwise lessons | Real project reference | Evidence to produce |
|---|---|---|---|
| AWS identity, network and host |21–25 |infra/aws-dev/main.tf, user-data.sh |Identity matrix, traffic trace, data-lifetime table |
| Artifacts, secrets and managed-service choices |26–28 |ECR/S3/Secrets resources, AWS Compose |Digest chain, storage inventory, proposed migration tradeoffs |
| Operations, cost and production design |29–31 |aws-smoke.sh, costs.md, short-run.md |Diagnostic timeline, dated cost worksheet, clearly labeled production proposal |
| Terraform mechanics |32–39 |Both Terraform roots, backend.hcl.example, mocked tests |Credential-free lab output, state/lock/plan explanations, assertion evidence |
| Delivery and interview defense |40–43 |deploy-dev.yml, aws-release-local.mjs, aws-remote-deploy.sh |Exact-SHA gate trace, rollback limitations, scored rehearsal |

Start the [cloud roadmap](20-cloud-roadmap-and-lab.md). These additions expand interview preparation; they do not claim a live AWS deployment or every AWS service is covered.

# Node.js/backend interview questionnaire and troubleshooting

137 questions and 24 incidents, chosen from concept coverage across both lesson sets and researched gaps. Existing lesson IDs and personal progress stay unchanged. Researched 5 November 2026.

[Study path](README.md) · [AWS/Terraform companion](aws-terraform-questionnaire.md) · [Coverage ledger](node-backend-coverage.md) · [Live progress](node-backend-progress.md) · [Download](NodeJs-AWS-study-pack.zip)

Use **start now** for first-interview foundations, **next** for mechanisms and **extension** for alternatives. Read the answer aloud, explain its project symbol, then describe one failure and how you would verify recovery. The incidents are rehearsals unless the progress/evidence record explicitly says a check ran. An implementation label establishes source presence, not a verified running service.

Start locally: use Node within the backend’s declared `>=22 <25` range and Docker Desktop/Compose v2. From the repository root run `npm run setup`, then `npm run up`; open http://localhost:8180. For host hot reload, stop containers with `npm run down`, run `bash scripts/local.sh deps`, install backend/frontend dependencies and run `npm run dev`; open http://localhost:5183. The source-linked setup section explains credentials, host/container addresses and expected health. These local scripts do not invoke AWS.

## Choose a small session

- First 30 minutes: NO01–NO07 (setup), NR01/NR14–NR17/NR22 (runtime), NS01–NS10 (service boundaries).
- One request: NS25–NS34, then NSI05 and NSI06 (authentication → durable inquiry → eventual notification).
- One failure drill: choose an incident below, predict its checks, repair and recovery observations, then run only the stated local exercise.
- Runnable mechanics: from the repository root, `node docs/nodejs-aws-study-path/labs/node-runtime/run.mjs`. The same lab runs from the extracted ZIP; [instructions and expected groups](labs/node-runtime/README.md).
- Advanced backend design: the operations extensions connect the cloud lessons to cache/queue/handler/trace/recovery behavior. Infrastructure detail remains in the AWS/Terraform companion.

## Read evidence carefully

Four capability processes own separate databases: Identity, Catalog, Inquiries and Notifications. Shared image/code does not mean shared domain tables. The older handbooks and some numbered lesson excerpts describe historical source checkpoints; this companion’s literal source excerpts were inspected for this task. The selected ECS infrastructure source is separate from application activation. No current AWS inventory, release, hosted CI, Jira or Study Desk publication is established here.

The requested [reference repository](https://github.com/Devinterview-io/node-interview-questions) was fetched before drafting. Its public README contains 15 expanded answers and advertises a larger question bank. This companion is original project-specific teaching, with independent section reviews and anonymous equivalent-explanation comparisons recorded separately; counts alone do not establish a quality win.

## Acronyms at a glance

| Term | Meaning |
|---|---|
| API / HTTP / JSON | Application programming interface / Hypertext Transfer Protocol / JavaScript Object Notation |
| URL / HTTPS / REST / HTML | Uniform Resource Locator / HTTP secured by TLS / Representational State Transfer / Hypertext Markup Language |
| I/O / CPU / RAM | Input/output / central processing unit / random-access memory |
| IP / ID / TCP / UDP | Internet Protocol / identifier / Transmission Control Protocol / User Datagram Protocol |
| ESM / CJS / DI | ECMAScript modules / CommonJS modules / dependency injection |
| SQL / JSONB / ACID | Structured Query Language / PostgreSQL binary JSON / atomicity, consistency, isolation, durability |
| JWT / HMAC / HS256 | JSON Web Token / hash-based message authentication code / HMAC using SHA-256 |
| TLS / CA / DNS | Transport Layer Security / certificate authority / Domain Name System |
| CORS / CSRF / XSS | Cross-Origin Resource Sharing / cross-site request forgery / cross-site scripting |
| OAuth / OIDC | OAuth authorization framework / OpenID Connect identity layer |
| PKCE / LTS / VM | Proof Key for Code Exchange / long-term support / virtual machine |
| UTC / ISO | Coordinated Universal Time / International Organization for Standardization (here, standardized date format) |
| UUID / SHA / UTF-8 | Universally unique identifier / Secure Hash Algorithm / Unicode Transformation Format using 8-bit units |
| CI / ADR / ORM | Continuous integration / architecture decision record / object-relational mapper |
| TTL / DLQ / FIFO | Time to live / dead-letter queue / first in, first out |
| SLI / SLO / SLA | Service-level indicator / objective / agreement |
| RPO / RTO | Recovery point objective (allowed data loss) / recovery time objective (allowed recovery duration) |
| AWS / ECS / RDS / SQS / SNS | Amazon Web Services / Elastic Container Service / Relational Database Service / Simple Queue Service / Simple Notification Service |
| EC2 / S3 / KMS | Elastic Compute Cloud / Simple Storage Service / Key Management Service |
| SCRAM / ACL / ISR | Salted Challenge Response Authentication Mechanism / access control list / in-sync replicas |

## Sections and stable IDs

### JavaScript, TypeScript and the Node runtime

- [NR01 · What is Node.js, and when is it a good backend choice?](node-backend-runtime.md#nr01) — start now
- [NR02 · Does const make an object immutable?](node-backend-runtime.md#nr02) — start now
- [NR03 · What is a closure, and do two requests share its local variables?](node-backend-runtime.md#nr03) — start now
- [NR04 · What do destructuring, rest and spread actually copy?](node-backend-runtime.md#nr04) — start now
- [NR05 · How do truthiness, optional chaining and nullish defaults differ?](node-backend-runtime.md#nr05) — start now
- [NR06 · When should I use map, filter, Set or Map?](node-backend-runtime.md#nr06) — start now
- [NR07 · Can a catch block assume the thrown value is an Error?](node-backend-runtime.md#nr07) — start now
- [NR08 · How do unknown, any and type assertions affect input safety?](node-backend-runtime.md#nr08) — start now
- [NR09 · What are literal unions and as const useful for?](node-backend-runtime.md#nr09) — start now
- [NR10 · Does a generic return type validate a response?](node-backend-runtime.md#nr10) — start now
- [NR11 · Why can Nest inject a class but not an erased interface by itself?](node-backend-runtime.md#nr11) — start now
- [NR12 · Why do these TypeScript files import local .js paths?](node-backend-runtime.md#nr12) — start now
- [NR13 · Why can decorator settings break dependency injection?](node-backend-runtime.md#nr13) — start now
- [NR14 · Does await block every request or start a new thread?](node-backend-runtime.md#nr14) — start now
- [NR15 · How do callbacks, promises and async/await relate?](node-backend-runtime.md#nr15) — start now
- [NR16 · How is the native worker pool different from worker_threads?](node-backend-runtime.md#nr16) — start now
- [NR17 · Does Promise.all limit concurrency or cancel failed work?](node-backend-runtime.md#nr17) — start now
- [NR18 · Are timers exact, and what does unref change?](node-backend-runtime.md#nr18) — start now
- [NR19 · What order do promises, nextTick, setTimeout and setImmediate run in?](node-backend-runtime.md#nr19) — next
- [NR20 · Why is void backgroundWork() not an error handler?](node-backend-runtime.md#nr20) — start now
- [NR21 · What does backpressure mean beyond streams?](node-backend-runtime.md#nr21) — start now
- [NR22 · Is EventEmitter.emit asynchronous?](node-backend-runtime.md#nr22) — start now
- [NR23 · What does HTTP body parsing prove, and what does it not prove?](node-backend-runtime.md#nr23) — start now
- [NR24 · Why is string length different from Buffer byte length?](node-backend-runtime.md#nr24) — start now
- [NR25 · When are readFile and readdir appropriate?](node-backend-runtime.md#nr25) — start now
- [NR26 · How does process.cwd differ from the current module location?](node-backend-runtime.md#nr26) — start now
- [NR27 · What is a stream, and why use pipeline for large data?](node-backend-runtime.md#nr27) — next
- [NR28 · What should a producer do when writable.write returns false?](node-backend-runtime.md#nr28) — next
- [NR29 · How are child processes, watch mode and compiled output related?](node-backend-runtime.md#nr29) — start now
- [NR30 · Why choose spawn or execFile over a shell command string?](node-backend-runtime.md#nr30) — next
- [NR31 · What should SIGTERM and shutdown hooks accomplish?](node-backend-runtime.md#nr31) — start now
- [NR32 · When would worker threads or cluster help, and are they implemented here?](node-backend-runtime.md#nr32) — extension
- [NR33 · How do you keep a request ID across awaited operations?](node-backend-runtime.md#nr33) — extension
- [NR34 · Does fetch reject an HTTP error response, and what does abort guarantee?](node-backend-runtime.md#nr34) — start now
- [NR35 · How would you investigate memory growth without assuming a leak?](node-backend-runtime.md#nr35) — extension
- [NR36 · What do JSON.parse and JSON.stringify preserve?](node-backend-runtime.md#nr36) — start now
- [NR37 · How should a backend use regular expressions and number conversion?](node-backend-runtime.md#nr37) — start now
- [NR38 · Why serialize timestamps with toISOString?](node-backend-runtime.md#nr38) — start now
- [NR39 · When should I use URL, URLSearchParams and encodeURIComponent?](node-backend-runtime.md#nr39) — start now
- [NR40 · What do Record, ReturnType and Omit change at runtime?](node-backend-runtime.md#nr40) — start now
- [NR41 · Why use import type, and how is it different from a runtime import?](node-backend-runtime.md#nr41) — start now
- [NR42 · Why do launchers use fileURLToPath, dirname, resolve and process groups?](node-backend-runtime.md#nr42) — next
- [NR43 · How do arrow functions and class methods use this?](node-backend-runtime.md#nr43) — next
- [NRI01 · Compiled service reports ERR_MODULE_NOT_FOUND or require is not defined](node-backend-runtime.md#nri01) — start now; incident
- [NRI02 · Startup says ENOENT or No migrations found](node-backend-runtime.md#nri02) — start now; incident
- [NRI03 · All requests pause during one expensive handler](node-backend-runtime.md#nri03) — start now; incident
- [NRI04 · A background rejection terminates or silently stops work](node-backend-runtime.md#nri04) — start now; incident
- [NRI05 · A source edit never reaches the running service](node-backend-runtime.md#nri05) — start now; incident
- [NRI06 · The service hangs on shutdown or restarts mid-delivery](node-backend-runtime.md#nri06) — start now; incident

### NestJS, contracts, security, databases and events

- [NS01 · What do Nest decorators and modules do?](node-backend-services.md#ns01) — start now
- [NS02 · How does dependency injection supply a service?](node-backend-services.md#ns02) — start now
- [NS03 · What belongs in a controller versus a service?](node-backend-services.md#ns03) — start now
- [NS04 · When is asynchronous startup finished?](node-backend-services.md#ns04) — start now
- [NS05 · Are Helmet, body parsing and validation interchangeable?](node-backend-services.md#ns05) — start now
- [NS06 · How do guards and exception filters differ?](node-backend-services.md#ns06) — start now
- [NS07 · Does installing RxJS make these services reactive?](node-backend-services.md#ns07) — next
- [NS08 · Why validate input when TypeScript already has types?](node-backend-services.md#ns08) — start now
- [NS09 · How do coercion, transforms and defaults affect query parameters?](node-backend-services.md#ns09) — start now
- [NS10 · What do strict schemas and inferred types guarantee?](node-backend-services.md#ns10) — start now
- [NS11 · How are SQL injection and wildcard surprises prevented?](node-backend-services.md#ns11) — start now
- [NS12 · How does PostgreSQL JSONB differ from a JavaScript object?](node-backend-services.md#ns12) — start now
- [NS13 · How does this catalog paginate consistently?](node-backend-services.md#ns13) — next
- [NS14 · Why preserve server-owned fields during a profile update?](node-backend-services.md#ns14) — start now
- [NS15 · What is a connection pool, and how big is this one?](node-backend-services.md#ns15) — start now
- [NS16 · Why must a transaction keep the same database client?](node-backend-services.md#ns16) — start now
- [NS17 · Are database row types automatically the API types?](node-backend-services.md#ns17) — start now
- [NS18 · When should a row lock or an advisory lock be used?](node-backend-services.md#ns18) — start now
- [NS19 · Does a transaction imply serializable isolation?](node-backend-services.md#ns19) — next
- [NS20 · Why are migrations versioned, hashed and locked?](node-backend-services.md#ns20) — start now
- [NS21 · What do pool error events and verified TLS protect?](node-backend-services.md#ns21) — start now
- [NS22 · How does promisify connect callbacks to async/await?](node-backend-services.md#ns22) — start now
- [NS23 · Why use a salt and scrypt for passwords?](node-backend-services.md#ns23) — start now
- [NS24 · Does timingSafeEqual make the whole login constant-time?](node-backend-services.md#ns24) — start now
- [NS25 · What does this JWT prove, and what stays readable?](node-backend-services.md#ns25) — start now
- [NS26 · Why verify JWT claims as well as its signature?](node-backend-services.md#ns26) — start now
- [NS27 · How do authentication, roles and ownership differ?](node-backend-services.md#ns27) — start now
- [NS28 · What does the in-memory login throttle actually limit?](node-backend-services.md#ns28) — next
- [NS29 · Why handle fetch rejection and response status separately?](node-backend-services.md#ns29) — start now
- [NS30 · What do a fetch timeout and URL encoding guarantee?](node-backend-services.md#ns30) — start now
- [NS31 · How does an idempotency key differ from a payload fingerprint?](node-backend-services.md#ns31) — start now
- [NS32 · Why generate separate inquiry and event UUIDs?](node-backend-services.md#ns32) — start now
- [NS33 · How does an outbox avoid losing an event intent?](node-backend-services.md#ns33) — start now
- [NS34 · What makes inquiry status transitions safe?](node-backend-services.md#ns34) — start now
- [NS35 · What are Kafka’s client, producer, consumer and group?](node-backend-services.md#ns35) — start now
- [NS36 · Do keys and acks=-1 guarantee exactly-once processing?](node-backend-services.md#ns36) — start now
- [NS37 · Why publish a bounded SKIP LOCKED batch?](node-backend-services.md#ns37) — start now
- [NS38 · Does fromBeginning replay every record on every restart?](node-backend-services.md#ns38) — start now
- [NS39 · Why decode, parse and validate an event separately?](node-backend-services.md#ns39) — start now
- [NS40 · How can repeated event delivery produce one inbox row?](node-backend-services.md#ns40) — start now
- [NS41 · Why can HTTP start while the messaging worker reconnects?](node-backend-services.md#ns41) — start now
- [NS42 · What do KafkaJS instrumentation events say about health?](node-backend-services.md#ns42) — start now
- [NS43 · Why expose three different health checks?](node-backend-services.md#ns43) — start now
- [NS44 · Does a shared backend image mean one service or one failure domain?](node-backend-services.md#ns44) — start now
- [NS45 · Does FOR UPDATE prevent a stale profile overwrite?](node-backend-services.md#ns45) — next
- [NS46 · How do CORS and CSRF differ from login protection?](node-backend-services.md#ns46) — extension
- [NS47 · How do sessions, OAuth and OpenID Connect differ from this JWT login?](node-backend-services.md#ns47) — extension
- [NS48 · What does graceful shutdown promise here?](node-backend-services.md#ns48) — next
- [NS49 · What should application logs prove without leaking secrets?](node-backend-services.md#ns49) — next
- [NS50 · In which order do middleware, guards, pipes and interceptors run?](node-backend-services.md#ns50) — extension
- [NS51 · Does this project use ConfigModule?](node-backend-services.md#ns51) — extension
- [NS52 · Is pg an object-relational mapper?](node-backend-services.md#ns52) — extension
- [NS53 · Does AuthGuard here use Passport strategies?](node-backend-services.md#ns53) — extension
- [NS54 · Are these API schemas generated by Swagger?](node-backend-services.md#ns54) — extension
- [NSI01 · Login returns 401 even with a token: where do you look?](node-backend-services.md#nsi01) — start now; incident
- [NSI02 · Catalog returns 400 or an unexpected search page: how do you diagnose it?](node-backend-services.md#nsi02) — start now; incident
- [NSI03 · All database-backed requests slow down: what do you measure first?](node-backend-services.md#nsi03) — start now; incident
- [NSI04 · Startup reports a changed migration checksum: what is safe?](node-backend-services.md#nsi04) — start now; incident
- [NSI05 · An inquiry response timed out: should you submit again?](node-backend-services.md#nsi05) — start now; incident
- [NSI06 · Inquiry exists but the inbox is empty: how do you isolate the stage?](node-backend-services.md#nsi06) — start now; incident
- [NSI07 · A consumer repeatedly fails on one record: what happens next?](node-backend-services.md#nsi07) — start now; incident
- [NSI08 · Local TLS connection fails after certificate changes: what stays enabled?](node-backend-services.md#nsi08) — start now; incident
- [NSI09 · Login rate limiting changes behind a proxy or replica: why?](node-backend-services.md#nsi09) — start now; incident

### Setup, testing, client boundaries, delivery and extensions

- [NO01 · Which Node version should I install for this project?](node-backend-operations.md#no01) — start now
- [NO02 · What do package.json, a lockfile and npm ci each do?](node-backend-operations.md#no02) — start now
- [NO03 · How do I start all four services locally?](node-backend-operations.md#no03) — start now
- [NO04 · How can I run with hot reload and a debugger?](node-backend-operations.md#no04) — start now
- [NO05 · Why can localhost work on my laptop but fail in a container?](node-backend-operations.md#no05) — start now
- [NO06 · What must configuration validation establish before listening?](node-backend-operations.md#no06) — start now
- [NO07 · Why compile TypeScript before starting Node?](node-backend-operations.md#no07) — start now
- [NO08 · What is shared when four services use the same Docker image?](node-backend-operations.md#no08) — start now
- [NO09 · What does a mock prove compared with a real integration test?](node-backend-operations.md#no09) — start now
- [NO10 · How do I test a race without hoping it happens?](node-backend-operations.md#no10) — next
- [NO11 · What do type checking, linting, unit tests, build and acceptance each establish?](node-backend-operations.md#no11) — start now
- [NO12 · Why keep a real browser test after API tests pass?](node-backend-operations.md#no12) — next
- [NO13 · Why does fetch need both catch and a response-status check?](node-backend-operations.md#no13) — start now
- [NO14 · Why use abort plus a stale-response guard?](node-backend-operations.md#no14) — next
- [NO15 · Which state belongs in React and which belongs in the backend?](node-backend-operations.md#no15) — next
- [NO16 · Why preserve the original inquiry key after a network failure?](node-backend-operations.md#no16) — start now
- [NO17 · How do I explain a CI workflow without claiming deployment happened?](node-backend-operations.md#no17) — next
- [NO18 · What does a Sonar quality gate add, and what are its limits?](node-backend-operations.md#no18) — next
- [NO19 · How should I review a dependency update or security advisory?](node-backend-operations.md#no19) — next
- [NO20 · How are short-lived release identity and application identity different?](node-backend-operations.md#no20) — next
- [NO21 · Why serialize deployment and separate rollback from data recovery?](node-backend-operations.md#no21) — next
- [NO22 · What makes an AI-assisted backend change reviewable?](node-backend-operations.md#no22) — next
- [NO23 · How would cache-aside preserve correct provider results?](node-backend-operations.md#no23) — extension
- [NO24 · How would I model a DynamoDB query instead of replacing SQL with Scan?](node-backend-operations.md#no24) — extension
- [NO25 · Do many partition keys and TTL guarantee safe DynamoDB writes?](node-backend-operations.md#no25) — extension
- [NO26 · How do a queue, pub/sub, an event bus and a workflow differ?](node-backend-operations.md#no26) — extension
- [NO27 · What do FIFO groups and partial batch failure actually guarantee?](node-backend-operations.md#no27) — extension
- [NO28 · How would an event-triggered Lambda differ from this listening Nest process?](node-backend-operations.md#no28) — extension
- [NO29 · Why must Lambda retry and concurrency policy depend on its trigger?](node-backend-operations.md#no29) — extension
- [NO30 · What would useful tracing show across the inquiry and notification flow?](node-backend-operations.md#no30) — extension
- [NO31 · How do SLI, SLO and an error budget guide an incident?](node-backend-operations.md#no31) — extension
- [NO32 · How would a saga recover when several services cannot share one transaction?](node-backend-operations.md#no32) — extension
- [NO33 · What proves recovery after database failover or restoration?](node-backend-operations.md#no33) — next
- [NO34 · What changes when a Node service scales to more process replicas?](node-backend-operations.md#no34) — next
- [NO35 · Is a persistent volume a backup, and how do object, file and block storage differ?](node-backend-operations.md#no35) — next
- [NO36 · Why is secret rotation a state transition instead of a text edit?](node-backend-operations.md#no36) — extension
- [NO37 · How do logs, metrics, traces and administrative audit differ?](node-backend-operations.md#no37) — next
- [NO38 · What would prove that a monitoring alarm works?](node-backend-operations.md#no38) — extension
- [NO39 · Why can TypeScript tests fail on imports when the app builds?](node-backend-operations.md#no39) — next
- [NO40 · Where do the demo users come from, and is that a sign-up API?](node-backend-operations.md#no40) — next
- [NOI01 · Install or build fails before any service starts](node-backend-operations.md#noi01) — start now; incident
- [NOI02 · Port in use or the browser reaches the wrong runtime](node-backend-operations.md#noi02) — start now; incident
- [NOI03 · Database refuses the service after changing environment settings](node-backend-operations.md#noi03) — start now; incident
- [NOI04 · A fresh build starts but cannot find migrations](node-backend-operations.md#noi04) — start now; incident
- [NOI05 · The UI displays old results or reports failure after a committed write](node-backend-operations.md#noi05) — start now; incident
- [NOI06 · Tests pass but the API route fails through nginx](node-backend-operations.md#noi06) — start now; incident
- [NOI07 · A cache or proposed queue consumer returns stale or repeated work](node-backend-operations.md#noi07) — extension; incident
- [NOI08 · A rollback starts but expected records are missing](node-backend-operations.md#noi08) — start now; incident
- [NOI09 · After scaling, database saturation increases while request latency worsens](node-backend-operations.md#noi09) — start now; incident

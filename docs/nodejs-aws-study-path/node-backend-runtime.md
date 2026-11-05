# JavaScript, TypeScript and the Node runtime

[Questionnaire and routes](node-backend-questionnaire.md) · [Acronym glossary](node-backend-questionnaire.md#acronyms-at-a-glance) · [Source excerpts](evidence/node-backend-source-context.md) · [Runtime lab](labs/node-runtime/README.md)

<a id="nr01"></a>

### NR01 · What is Node.js, and when is it a good backend choice?

**Priority:** start now. **Implementation:** Current source.

Node.js runs JavaScript outside the browser. It supplies network, file and process APIs (application programming interfaces). V8 executes JavaScript; libuv supports event-loop and operating-system work. Waiting on many database or network calls suits this model. A long calculation still needs a capacity plan. Here Node runs four separate NestJS service processes, selected by SERVICE.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-nr01) · symbol: `const service = serviceName();`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md) · [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs).

<a id="nr02"></a>

### NR02 · Does const make an object immutable?

**Priority:** start now. **Implementation:** Current source.

No. const prevents assigning a different value to the binding; it does not freeze the referenced object. Catalog can push query parameters into its const values array. Example: const a = []; a.push(1) works, but a = [] fails. Shared nested objects can still change unless copied or deliberately protected.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-nr02) · symbol: `const values: unknown[] = [];`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/ecmascript-language-statements-and-declarations.html).

<a id="nr03"></a>

### NR03 · What is a closure, and do two requests share its local variables?

**Priority:** start now. **Implementation:** Current source.

A closure is a function that keeps access to the scope where it was created. Catalog search creates an add function that remembers that call’s values array. Another search call gets another array. Moving that array to a singleton field would change its lifetime and risk mixing requests. Closures can also retain large objects after they are no longer useful.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-nr03) · symbol: `const add = (value: unknown) => {`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/executable-code-and-execution-contexts.html#sec-environment-records).

<a id="nr04"></a>

### NR04 · What do destructuring, rest and spread actually copy?

**Priority:** start now. **Implementation:** Current source.

Destructuring extracts properties; rest collects the remaining properties. Object spread creates a shallow copy: nested arrays may still point at the same data. Catalog removes ownerEmail before storing the public document, then overrides protected rating fields after spreading an update. The later property wins. This is a data-shaping step, not a substitute for schema and ownership checks.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-nr04) · symbol: `const { ownerEmail, ...document } = entry;`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/ecmascript-language-expressions.html).

<a id="nr05"></a>

### NR05 · How do truthiness, optional chaining and nullish defaults differ?

**Priority:** start now. **Implementation:** Current source.

Optional chaining, ?. , stops property access on null or undefined. The ?? operator supplies a default only for those two values; || also replaces 0, false and empty text. Identity uses account?.password_hash ?? this.dummyHash. Catalog tests maxRate !== undefined so zero remains a real filter. The string "false" is truthy and needs an explicit conversion rule.

**Project:** [backend/src/identity/identity.service.ts](evidence/node-backend-source-context.md#source-nr05) · symbol: `const valid = await verifyPassword`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/ecmascript-language-expressions.html).

<a id="nr06"></a>

### NR06 · When should I use map, filter, Set or Map?

**Priority:** start now. **Implementation:** Current source.

map transforms array elements; filter selects them. Set keeps distinct values; Map stores key/value pairs without converting every key to text. The comparison hook filters saved input to strings, deduplicates IDs with Set and keeps at most three. Objects in Set compare by identity: two separately created objects with the same fields remain two entries. These collections live in memory, not in a durable database.

**Project:** [frontend/src/hooks/useMarketplace.ts](evidence/node-backend-source-context.md#source-nr06) · symbol: `...new Set(`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/indexed-collections.html) · [tc39.es · reference 2](https://tc39.es/ecma262/multipage/keyed-collections.html).

<a id="nr07"></a>

### NR07 · Can a catch block assume the thrown value is an Error?

**Priority:** start now. **Implementation:** Current source.

No. JavaScript can throw a string, null or another value. Narrow an unknown caught value before reading its properties. The project filter distinguishes Zod errors, HTTP exceptions and unexpected errors; unexpected details stay in server logs while the client receives a generic message. A surrounding try catches an awaited rejection, but does not automatically catch an unrelated later callback’s throw.

**Project:** [backend/src/common/errors.ts](evidence/node-backend-source-context.md#source-nr07) · symbol: `catch(error: unknown, host: ArgumentsHost): void {`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/narrowing.html).

<a id="nr08"></a>

### NR08 · How do unknown, any and type assertions affect input safety?

**Priority:** start now. **Implementation:** Current source.

unknown requires narrowing before use; any turns off useful checking. An assertion such as input as Provider changes the compiler’s opinion without checking a single incoming field. Catalog accepts unknown input and calls providerSchema.parse at runtime. JSON (JavaScript Object Notation) from a client or another service still needs validation after a successful TypeScript build.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-nr08) · symbol: `async update(email: string, input: unknown): Promise<Provider> {`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) · [www.typescriptlang.org · reference 2](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html).

<a id="nr09"></a>

### NR09 · What are literal unions and as const useful for?

**Priority:** start now. **Implementation:** Current source.

A literal union restricts a type to named alternatives, such as the four service names. as const preserves exact tuple values for deriving that union. These restrictions disappear at runtime: SERVICE arrives as environment text, so serviceName still checks membership. A cast inside includes does not validate the value; the includes result and thrown error perform that check.

**Project:** [backend/src/common/config.ts](evidence/node-backend-source-context.md#source-nr09) · symbol: `export const SERVICES =`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html).

<a id="nr10"></a>

### NR10 · Does a generic return type validate a response?

**Priority:** start now. **Implementation:** Current source.

No. Generics express relationships between types. The client api<T> helper tells TypeScript which result callers expect, then parses response JSON. It does not decode the fields against T. Runtime response schemas would be an explicit extension. Compare the backend Catalog lookup, which really parses the returned object with Zod before using ownerEmail.

**Project:** [frontend/src/services/http.ts](evidence/node-backend-source-context.md#source-nr10) · symbol: `export async function api<T>(`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/generics.html).

<a id="nr11"></a>

### NR11 · Why can Nest inject a class but not an erased interface by itself?

**Priority:** start now. **Implementation:** Current source.

A class can supply a runtime constructor value; an interface or object type disappears after compilation. Catalog’s constructor parameter uses Database as the dependency token Nest can resolve. Injecting an interface needs an explicit runtime token and matching provider registration. TypeScript private and readonly describe access and assignment checks; neither creates database permissions or an authorization boundary.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-nr11) · symbol: `constructor(private readonly db: Database) {}`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html) · [www.typescriptlang.org · reference 2](https://www.typescriptlang.org/tsconfig/emitDecoratorMetadata.html).

<a id="nr12"></a>

### NR12 · Why do these TypeScript files import local .js paths?

**Priority:** start now. **Implementation:** Current source.

The backend is an ECMAScript module (ESM) package: package.json sets type to module and TypeScript uses NodeNext. Its emitted files run as JavaScript, so ./config.js names the runtime file while TypeScript resolves the source .ts file during compilation. CommonJS uses require/module.exports and has different loading rules. Copying a require tutorial directly into this ESM package can fail at startup.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nr12) · symbol: `import { serviceName } from './config.js';`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/esm.html).

<a id="nr13"></a>

### NR13 · Why can decorator settings break dependency injection?

**Priority:** start now. **Implementation:** Current source.

This Nest setup uses decorator metadata emitted by TypeScript and loads reflect-metadata before bootstrap. The emitted constructor information helps resolve class dependencies. experimentalDecorators and emitDecoratorMetadata are part of that compiler/runtime agreement. Changing decorator mode requires checking compatibility. Declaration packages such as @types/pg add compile-time descriptions; installing them does not install pg’s runtime code or validate database results.

**Project:** [backend/tsconfig.json](evidence/node-backend-source-context.md#source-nr13) · symbol: `"emitDecoratorMetadata": true,`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/tsconfig/emitDecoratorMetadata.html).

<a id="nr14"></a>

### NR14 · Does await block every request or start a new thread?

**Priority:** start now. **Implementation:** Current source.

Neither. await suspends the current async function’s continuation until its promise settles, allowing other callbacks to run while external work waits. Identity can await PostgreSQL while another request progresses. Promises and async/await do not themselves execute JavaScript on extra processors. Two requests can interleave across awaits, so one main JavaScript thread does not remove database races.

**Project:** [backend/src/identity/identity.service.ts](evidence/node-backend-source-context.md#source-nr14) · symbol: `const result = await this.db.query(`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop).

<a id="nr15"></a>

### NR15 · How do callbacks, promises and async/await relate?

**Priority:** start now. **Implementation:** Current source.

A callback is a function another operation invokes. A promise represents a future result or rejection; async functions return promises and await consumes them. Password code uses promisify to adapt Node’s error-first scrypt callback, whose first argument reports failure. The wrapper keeps scrypt asynchronous; it does not create a new password algorithm. Callbacks remain appropriate for repeated events, while a promise settles once.

**Project:** [backend/src/identity/password.ts](evidence/node-backend-source-context.md#source-nr15) · symbol: `const scrypt = promisify(scryptCallback);`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/util.html) · [nodejs.org · reference 2](https://nodejs.org/api/crypto.html).

<a id="nr16"></a>

### NR16 · How is the native worker pool different from worker_threads?

**Priority:** start now. **Implementation:** Current source.

Asynchronous scrypt uses native worker-pool capacity, so the main event loop can serve other work. Heavy JavaScript still occupies its current thread, even inside an async function. worker_threads can run JavaScript in parallel on other threads; this application has no worker-thread job pool. Both designs consume finite processor and memory capacity, so unlimited parallel password work remains unsafe.

**Project:** [backend/src/identity/password.ts](evidence/node-backend-source-context.md#source-nr16) · symbol: `const hash = (await scrypt(password, salt, 64)) as Buffer;`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) · [nodejs.org · reference 2](https://nodejs.org/api/worker_threads.html).

<a id="nr17"></a>

### NR17 · Does Promise.all limit concurrency or cancel failed work?

**Priority:** start now. **Implementation:** Current source.

No. map starts each provider lookup; Promise.all aggregates the returned promises in input order and rejects when one rejects. Already started operations continue unless separately cancelled. The project caps comparisons at three, bounding that particular fan-out. For a large batch, queue work with a measured concurrency limit. Use allSettled when every success/failure outcome is needed, not when partial success should silently count as a complete result.

**Project:** [frontend/src/hooks/useMarketplace.ts](evidence/node-backend-source-context.md#source-nr17) · symbol: `Promise.all(compare.map((id) => providerService.get(id, controller.signal)))`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/control-abstraction-objects.html#sec-promise.all).

<a id="nr18"></a>

### NR18 · Are timers exact, and what does unref change?

**Priority:** start now. **Implementation:** Current source.

A timeout makes its callback eligible after a delay; busy JavaScript can postpone it. unref means that timer alone need not keep the process alive. It neither cancels the callback nor stops network work. The outbox worker uses an unreferenced pause for polling. A ref-count decision is about process lifetime, not a guarantee that a final retry or cleanup will execute.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-nr18) · symbol: `setTimeout(resolve, ms).unref();`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/timers.html).

<a id="nr19"></a>

### NR19 · What order do promises, nextTick, setTimeout and setImmediate run in?

**Priority:** next. **Implementation:** Current source.

Synchronous code finishes first; queued promise continuations run before the next timer turn. process.nextTick has a separate queue and recursive use can starve input/output (I/O). Do not promise one universal nextTick-versus-promise order across CommonJS and ESM entry points. Nor is top-level setTimeout(0) versus setImmediate order guaranteed. In an I/O callback, immediate runs before a timer scheduled there. State the execution context before predicting output.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-nr19) · symbol: `const pause = (ms: number) =>`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) · [nodejs.org · reference 2](https://nodejs.org/api/process.html).

<a id="nr20"></a>

### NR20 · Why is void backgroundWork() not an error handler?

**Priority:** start now. **Implementation:** Current source.

void discards an expression’s value; it does not catch promise rejection. The messaging bootstrap launches an ongoing loop with void this.run(); the loop owns retries, health status and cleanup. Awaiting that never-ending loop during bootstrap would prevent startup completing. Detached work needs a deliberate error owner and stop policy; merely prefixing an unsafe promise with void does not supply either.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-nr20) · symbol: `void this.run();`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/process.html).

<a id="nr21"></a>

### NR21 · What does backpressure mean beyond streams?

**Priority:** start now. **Implementation:** Current source.

Backpressure means slowing or limiting incoming work when a dependency cannot keep up. The database pool allows ten connections per process; additional work waits, with a five-second acquisition limit. That bounds connections, not all queued requests or query execution time. Measure waiting work and downstream latency before raising limits; four services and multiple replicas multiply the total connection budget.

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-nr21) · symbol: `max: 10,`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop).

<a id="nr22"></a>

### NR22 · Is EventEmitter.emit asynchronous?

**Priority:** start now. **Implementation:** Current source.

By default, emit calls registered listeners synchronously in registration order. A listener can schedule later work, but emit does not await a promise it returns. A plain EventEmitter error event without an error listener can terminate the process. Database registers a pool error listener for failures from idle clients. Local event listeners are not durable Kafka delivery and cannot replace the persisted outbox.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nr22) · symbol: `this.pool.on('error', (error: Error) =>`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/docs/latest-v22.x/api/events.html).

<a id="nr23"></a>

### NR23 · What does HTTP body parsing prove, and what does it not prove?

**Priority:** start now. **Implementation:** Current source.

HTTP (Hypertext Transfer Protocol) carries a method, path, headers and body bytes. Express’s JSON parser turns permitted input into a JavaScript value, subject to a 128-kilobyte limit. Valid JSON can still have the wrong fields, role or owner, so schema and business checks follow. Malformed syntax, excessive size and a rejected domain request fail at different boundaries; returning the same status does not make those causes identical.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-nr23) · symbol: `app.use(json({ limit: '128kb' }));`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/http.html).

<a id="nr24"></a>

### NR24 · Why is string length different from Buffer byte length?

**Priority:** start now. **Implementation:** Current source.

JavaScript string length counts UTF-16 code units; Buffer represents bytes. UTF-8 (Unicode Transformation Format, 8-bit) uses variable-width encoding: an emoji such as 😀 has string length 2 and byte length 4. The JSON Web Token secret (JWT_SECRET) is checked in bytes, while INTERNAL_API_KEY is checked in characters. Hex decoding in password verification and UTF-8 decoding in Kafka serve different purposes; choose the encoding explicitly.

**Project:** [backend/src/common/config.ts](evidence/node-backend-source-context.md#source-nr24) · symbol: `if (Buffer.byteLength(secret) < 32)`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/buffer.html).

<a id="nr25"></a>

### NR25 · When are readFile and readdir appropriate?

**Priority:** start now. **Implementation:** Current source.

readFile reads an entire file before resolving; readdir lists directory entries. That is reasonable for the small, trusted SQL (Structured Query Language) migration files loaded at startup. The migration runner filters service-prefixed numbered filenames and sorts them. A multi-gigabyte upload would need incremental processing and size limits instead. Async file reads avoid blocking the main loop on disk waits but still require memory for the returned contents.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nr25) · symbol: `const files = (await readdir(directory))`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/docs/latest-v22.x/api/fs.html).

<a id="nr26"></a>

### NR26 · How does process.cwd differ from the current module location?

**Priority:** start now. **Implementation:** Current source.

process.cwd() is the process’s working directory, which launchers can choose. import.meta.url identifies the current ESM module. Database locates migrations relative to cwd, so running node backend/dist/main.js from the repository root can look in the wrong migrations directory. Use the supplied backend start scripts and working directory. If deliberately redesigning paths, anchor them to a module URL and test the packaged layout.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nr26) · symbol: `const directory = join(process.cwd(), 'migrations');`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/process.html) · [nodejs.org · reference 2](https://nodejs.org/api/esm.html).

<a id="nr27"></a>

### NR27 · What is a stream, and why use pipeline for large data?

**Priority:** next. **Implementation:** Absent implementation.

A stream processes chunks instead of first building the whole result in memory. Readable produces chunks, Writable consumes them, Duplex does both, and Transform changes chunks. pipeline connects stages and propagates completion or errors. This app has no streaming-upload endpoint; its small migration-file read is only the contrast. A practice stream copy should prove identical destination bytes and exercise an error case.

**External worked example (not installed here):** Use the official pipeline example in a scratch directory. Connect createReadStream(source) to createWriteStream(destination) through await pipeline from node:stream/promises. Compare file sizes and SHA-256 (Secure Hash Algorithm, 256-bit) digests. Retry with a missing source and require the awaited operation to reject; do not add an upload route to rehearse streams. [Official example](https://nodejs.org/docs/latest-v22.x/api/stream.html#streampipelinesource-transforms-destination-options).

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nr27) · symbol: `const sql = await readFile(join(directory, file), 'utf8');`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/docs/latest-v22.x/api/stream.html).

<a id="nr28"></a>

### NR28 · What should a producer do when writable.write returns false?

**Priority:** next. **Implementation:** Absent implementation.

Pause production until the writable signals drain; false means the chunk was accepted but the internal buffer reached its threshold. Ignoring it keeps buffering and can exhaust memory. highWaterMark is a buffering threshold, not a universal memory ceiling. pipeline handles normal stream backpressure for you. The current application does not implement a custom stream producer; database pool limits teach a related resource-budget idea.

**External worked example (not installed here):** Adapt the official writable.write/drain producer example in a scratch file with a deliberately slow Writable. Stop sending after write returns false and resume on drain. Count produced and consumed chunks, then assert the counts match after finish. Compare memory while scaling input; do not assume one heap measurement proves a hard bound. [Official example](https://nodejs.org/docs/latest-v22.x/api/stream.html#writablewritechunk-encoding-callback).

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-nr28) · symbol: `max: 10,`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/docs/latest-v22.x/api/stream.html).

<a id="nr29"></a>

### NR29 · How are child processes, watch mode and compiled output related?

**Priority:** start now. **Implementation:** Current source.

spawn starts another operating-system process with its own memory and lifecycle. The backend developer launcher first compiles TypeScript, then runs a compiler watcher and Node’s watcher over emitted JavaScript. Saving source is not the same as successfully compiling or passing tests. By default a child inherits process.env. Supplying env replaces that environment unless the parent spreads its values into the new object. Ordinary JavaScript variables are not shared between processes.

**Project:** [backend/scripts/dev.mjs](evidence/node-backend-source-context.md#source-nr29) · symbol: `const build = spawn(process.execPath,`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/child_process.html).

<a id="nr30"></a>

### NR30 · Why choose spawn or execFile over a shell command string?

**Priority:** next. **Implementation:** Current source.

exec runs through a shell; untrusted metacharacters can become commands. spawn/execFile with a fixed executable, argument array and shell disabled avoid shell interpretation. They still need input rules because the called program can interpret dangerous options or paths. The backend launcher selects from four known service names and invokes process.execPath directly. Shell escaping is not replaced by JSON.stringify.

**Project:** [backend/scripts/dev.mjs](evidence/node-backend-source-context.md#source-nr30) · symbol: `const build = spawn(process.execPath,`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/child_process.html).

<a id="nr31"></a>

### NR31 · What should SIGTERM and shutdown hooks accomplish?

**Priority:** start now. **Implementation:** Current source.

SIGTERM asks a process to stop; Nest shutdown hooks let providers close resources. Database ends its pool and messaging workers disconnect. Normal shutdown should stop new work and allow bounded in-flight work to finish, but forced termination can bypass hooks. That is why durable transactions, outbox replay and consumer deduplication remain necessary. process.exitCode marks the eventual status without immediately terminating pending work.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-nr31) · symbol: `app.enableShutdownHooks();`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/process.html).

<a id="nr32"></a>

### NR32 · When would worker threads or cluster help, and are they implemented here?

**Priority:** extension. **Implementation:** Absent implementation.

Worker threads can run processor-heavy JavaScript in parallel and communicate through messages. Cluster starts separate Node processes that can share a listening port. Neither makes database transactions magically consistent, and cluster workers do not share ordinary in-memory state. The project runs one process per capability; it implements neither a worker-thread job pool nor Node cluster. Container replicas are another process-scaling choice.

**External worked example (not installed here):** Follow the official isMainThread/parentPort worker example in a scratch module. Send a calculation input through workerData, return the result with postMessage, and handle message, error and non-zero exit. Assert the answer and compare main-thread timer responsiveness while it runs. Use a bounded reusable pool for repeated jobs; the introductory example alone is not production pooling. [Official example](https://nodejs.org/api/worker_threads.html).

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-nr32) · symbol: `await app.listen(port,`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md) · [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/worker_threads.html) · [nodejs.org · reference 2](https://nodejs.org/api/cluster.html).

<a id="nr33"></a>

### NR33 · How do you keep a request ID across awaited operations?

**Priority:** extension. **Implementation:** Absent implementation.

AsyncLocalStorage can carry request-scoped data through supported asynchronous continuations without a mutable global currentRequest variable. That helps correlate logs while concurrent requests interleave. It does not authenticate a caller or persist an audit trail. The project’s current ErrorFilter logs errors without an AsyncLocalStorage request context; request-context middleware would be an explicit extension.

**External worked example (not installed here):** Adapt the official HTTP-server logging example: wrap each request in storage.run({ requestId }, handler), then read storage.getStore() after an await. Send two overlapping requests and assert each log retains its own ID. Supply a generated ID for untrusted or absent client IDs and avoid storing credentials in the context. [Official example](https://nodejs.org/api/async_context.html#class-asynclocalstorage).

**Project:** [backend/src/common/errors.ts](evidence/node-backend-source-context.md#source-nr33) · symbol: `private readonly logger = new Logger('HttpErrors');`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/async_context.html).

<a id="nr34"></a>

### NR34 · Does fetch reject an HTTP error response, and what does abort guarantee?

**Priority:** start now. **Implementation:** Current source.

fetch rejects for transport failure or an aborted operation, but a received HTTP 404 or 500 still needs an explicit status check. Inquiries checks response.status and response.ok and bounds Catalog lookup with AbortSignal.timeout(5000). Abort limits client waiting; it does not undo work the remote server may already have committed. Retry writes with their original idempotency key when the outcome is uncertain.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-nr34) · symbol: `signal: AbortSignal.timeout(5000),`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md) · [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/globals.html).

<a id="nr35"></a>

### NR35 · How would you investigate memory growth without assuming a leak?

**Priority:** extension. **Implementation:** Absent implementation.

Compare heap, external Buffer memory and whole-process memory under a repeatable workload. Live caches, retained closures, unfinished requests and excessive buffering can all grow usage. A garbage-collected language can still retain reachable objects forever. This project has no built-in heap-capture workflow; use controlled local diagnostic runs and treat snapshots as sensitive because they may contain tokens or request data.

**External worked example (not installed here):** Use the official process.memoryUsage example in a disposable local script. Record heapUsed, external and rss while running a bounded workload, release the workload, then compare repeated steady-state runs. A rising rss alone does not prove a JavaScript-object leak. Escalate to a local heap snapshot only with sanitized data and never expose the inspector publicly. [Official example](https://nodejs.org/api/process.html#processmemoryusage).

**Project:** [backend/src/common/errors.ts](evidence/node-backend-source-context.md#source-nr35) · symbol: `private readonly logger = new Logger('HttpErrors');`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/process.html).

<a id="nr36"></a>

### NR36 · What do JSON.parse and JSON.stringify preserve?

**Priority:** start now. **Implementation:** Current source.

JSON.parse decodes JSON syntax; it does not establish the expected object shape. JSON.stringify creates JSON text and can fail on circular references or BigInt values. Object properties with undefined are omitted, and a Date normally serializes through its ISO text representation. The catalog seed path parses trusted file contents, then validates each public document. Avoid using JSON round-trips as a universal deep-clone or input-validation technique.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-nr36) · symbol: `const providers: (Provider & { ownerEmail: string })[] = JSON.parse(`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md).

**Lesson relationship:** Prerequisite or related source; this card adds researched JSON/conversion/date/URL detail rather than claiming it is taught as a complete section in the numbered lessons.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/structured-data.html).

<a id="nr37"></a>

### NR37 · How should a backend use regular expressions and number conversion?

**Priority:** start now. **Implementation:** Current source.

A regular expression checks a text pattern, not business permission. The migration regex accepts numbered SQL (Structured Query Language) filenames after the service-prefix check; neither permits user-chosen arbitrary file paths. PORT is converted with Number and checked for integer range before listening. Number("") becomes zero and parseInt can accept a valid prefix followed by junk, so validate the whole external value. Avoid unbounded complex regexes on large untrusted input.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nr37) · symbol: `.filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** Prerequisite or related source; this card adds researched JSON/conversion/date/URL detail rather than claiming it is taught as a complete section in the numbered lessons.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/text-processing.html) · [tc39.es · reference 2](https://tc39.es/ecma262/multipage/numbers-and-dates.html).

<a id="nr38"></a>

### NR38 · Why serialize timestamps with toISOString?

**Priority:** start now. **Implementation:** Current source.

A Date represents a time value, while toISOString emits a standardized UTC (Coordinated Universal Time) timestamp ending in Z. Inquiries converts the stored creation timestamp before returning it. Local display time can differ by time zone. Validate external date input deliberately; an invalid Date makes toISOString throw. Use durations and monotonic clocks for elapsed-time measurement rather than assuming wall-clock dates never jump.

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-nr38) · symbol: `createdAt: new Date(row.created_at).toISOString(),`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** Prerequisite or related source; this card adds researched JSON/conversion/date/URL detail rather than claiming it is taught as a complete section in the numbered lessons.

**Official documentation:** [tc39.es · reference 1](https://tc39.es/ecma262/multipage/numbers-and-dates.html).

<a id="nr39"></a>

### NR39 · When should I use URL, URLSearchParams and encodeURIComponent?

**Priority:** start now. **Implementation:** Current source.

URL parses an address into named components; it does not by itself approve a host or protocol. Config separately permits only HTTP (Hypertext Transfer Protocol) or HTTPS (HTTP over Transport Layer Security) for Catalog. URLSearchParams encodes query names and values. encodeURIComponent protects a single path component, such as a provider ID; do not encode the entire URL as though it were one ID. The server must still validate decoded input and authorization.

**Project:** [backend/src/common/config.ts](evidence/node-backend-source-context.md#source-nr39) · symbol: `const catalog = new URL(required('CATALOG_URL'));`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** Prerequisite or related source; this card adds researched JSON/conversion/date/URL detail rather than claiming it is taught as a complete section in the numbered lessons.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/url.html).

<a id="nr40"></a>

### NR40 · What do Record, ReturnType and Omit change at runtime?

**Priority:** start now. **Implementation:** Current source.

Nothing by themselves. Record describes a key-to-value type, ReturnType derives a function’s return type, and Omit removes keys from a type description. main uses Record for service constructor lookup; the client uses Omit<Auth, token> for current-user responses and ReturnType for hook state. These helpers avoid duplicated type declarations, but never remove a sensitive property from a real object or check an incoming payload.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-nr40) · symbol: `const controllers: Record<string, Type> = {`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/utility-types.html).

<a id="nr41"></a>

### NR41 · Why use import type, and how is it different from a runtime import?

**Priority:** start now. **Implementation:** Current source.

import type tells TypeScript an import is needed only for checking types; it disappears from emitted JavaScript. The HTTP helper imports Auth this way because Auth is a type description. A class used by Nest dependency injection must remain available as a runtime value/token. Removing a required runtime import can break injection even though a similarly named type still appears in source.

**Project:** [frontend/src/services/http.ts](evidence/node-backend-source-context.md#source-nr41) · symbol: `import type { Auth }`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/modules.html).

<a id="nr42"></a>

### NR42 · Why do launchers use fileURLToPath, dirname, resolve and process groups?

**Priority:** next. **Implementation:** Current source.

An ECMAScript module (ESM) URL (Uniform Resource Locator) is not automatically an operating-system file path. fileURLToPath converts it safely, dirname gets its containing directory and resolve forms an absolute project path. The root developer launcher uses that anchor even when invoked elsewhere. On Unix it starts detached process groups and sends SIGTERM to the group, so nested compiler/server children can stop together; Windows has a different child-kill path.

**Project:** [scripts/dev.mjs](evidence/node-backend-source-context.md#source-nr42) · symbol: `const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** Prerequisite or related mechanism; this card adds a researched extension rather than claiming every detail is taught by the linked lesson.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/url.html) · [nodejs.org · reference 2](https://nodejs.org/api/path.html) · [nodejs.org · reference 3](https://nodejs.org/api/child_process.html).

<a id="nr43"></a>

### NR43 · How do arrow functions and class methods use this?

**Priority:** next. **Implementation:** Current source.

An arrow captures this from its surrounding scope; it does not get a new receiver when called as another object’s property. A normal method uses its call receiver, so passing an unbound method can lose the intended instance. Nest creates class instances and injects their constructor dependencies. Catalog’s local add arrow closes over per-call query values; moving request data onto a singleton field would change its sharing and lifetime.

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-nr43) · symbol: `const add =`.

**Lessons:** [01 · javascript language foundations](generated/01-javascript-language-foundations.md) · [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/functions.html#declaring-this-in-a-function).

<a id="nri01"></a>

### NRI01 · Compiled service reports ERR_MODULE_NOT_FOUND or require is not defined

**Priority:** start now. **Implementation:** Current source.

The service builds or passes editor checks but fails when Node loads emitted files.

**Symptom:** The service builds or passes editor checks but fails when Node loads emitted files.

**Checks:** Read the exact missing specifier and package type. Inspect backend/package.json, NodeNext settings and the emitted dist import. Compare the source .js suffix with the emitted file location. Run from backend and distinguish missing dependency from wrong module syntax.

**Repair:** Keep this package’s ECMAScript module (ESM) settings coherent. Repair the import/path or install the locked runtime dependency with npm ci from backend; rebuild. Use a deliberate compatibility boundary for a CommonJS library rather than converting the whole package to copy a tutorial.

**Recovery verification:** From backend, run npm run build and start the chosen service with its local configuration. Confirm the module loads, migrations complete and that service’s direct health endpoint responds. Run its relevant test; compilation alone is insufficient.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nri01) · symbol: `import { serviceName } from './config.js';`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/esm.html).

<a id="nri02"></a>

### NRI02 · Startup says ENOENT or No migrations found

**Priority:** start now. **Implementation:** Current source.

A compiled backend cannot find migrations or seed data.

**Symptom:** A compiled backend cannot find migrations or seed data.

**Checks:** Read the failed path and process working directory. Database joins process.cwd() with migrations; Catalog/Identity also read seeds relative to cwd. Check packaged migrations and seeds exist and match the selected SERVICE. Do not print .env or database credentials while diagnosing.

**Repair:** Launch through the supplied backend or Compose command with its expected working directory; repair missing packaged files if needed. Preserve applied migration files and their checksums; do not delete migration history to bypass startup.

**Recovery verification:** Restart the affected local service. Confirm migrations complete without checksum errors, the service’s direct /health/serve is healthy, and a relevant application programming interface (API) call reads durable data. Verify the packaged start command works from a clean copy.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-nri02) · symbol: `const directory = join(process.cwd(), 'migrations');`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/process.html) · [nodejs.org · reference 2](https://nodejs.org/api/esm.html).

<a id="nri03"></a>

### NRI03 · All requests pause during one expensive handler

**Priority:** start now. **Implementation:** Current source.

Latency rises across unrelated requests while processor use climbs.

**Symptom:** Latency rises across unrelated requests while processor use climbs.

**Checks:** Measure event-loop delay and per-request latency in a reproducible local run. Inspect synchronous loops, huge JSON parsing and synchronous file/crypto calls. Compare with a dependency-waiting workload; high latency with low processor use can instead indicate pool waits.

**Repair:** Bound payloads and computation. Move justified heavy JavaScript into a bounded worker/job design or partition work to yield between chunks; retain native async APIs for supported operations. Increasing promise count does not parallelize a busy JavaScript loop.

**Recovery verification:** Repeat the same mixed workload and compare tail latency, timer delay, processor use and correctness. Require unrelated health and application programming interface (API) requests to remain responsive and inspect errors/timeouts. Record measurements rather than declaring success because the handler became async.

**Project:** [backend/src/identity/password.ts](evidence/node-backend-source-context.md#source-nri03) · symbol: `const hash = (await scrypt(password, salt, 64)) as Buffer;`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) · [nodejs.org · reference 2](https://nodejs.org/api/worker_threads.html).

<a id="nri04"></a>

### NRI04 · A background rejection terminates or silently stops work

**Priority:** start now. **Implementation:** Current source.

After a worker failure the process exits, logs an unhandled rejection, or stops making progress.

**Symptom:** After a worker failure the process exits, logs an unhandled rejection, or stops making progress.

**Checks:** Find the originating promise and its error owner. Inspect bootstrap’s catch and the messaging run loop’s retry/finally path. Check health readiness and the durable backlog, distinguishing HTTP (Hypertext Transfer Protocol) serving health from worker readiness. void does not handle rejection.

**Repair:** Catch expected failures at the loop boundary, report them and retry with bounded pacing; close partial connections in finally. Unexpected fatal failures need controlled termination and supervision, not an empty global rejection handler that pretends processing succeeded.

**Recovery verification:** Inject the original dependency failure locally, observe a visible unhealthy worker state and preserved durable records, then restore the dependency. Require worker readiness and backlog drain to recover, with deduplicated effects and no unhandled rejection.

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-nri04) · symbol: `void this.run();`.

**Lessons:** [03 · node runtime and async](generated/03-node-runtime-and-async.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/process.html).

<a id="nri05"></a>

### NRI05 · A source edit never reaches the running service

**Priority:** start now. **Implementation:** Current source.

The browser keeps seeing old behavior after a TypeScript edit.

**Symptom:** The browser keeps seeing old behavior after a TypeScript edit.

**Checks:** Read the compiler watcher output and Node watcher output separately. Confirm the selected SERVICE, dist-dev directory, working directory and listening port. Check for another Compose or host process serving the same route. A saved .ts file is not proof that a .js file was emitted.

**Repair:** Repair the actual compile error or wrong launcher target and restart the affected local watcher. Use npm run down before switching from the full Compose stack to host hot reload, following local setup; do not kill unrelated processes blindly.

**Recovery verification:** Make a harmless observable local change, confirm successful emit/restart, call the intended service port and routed endpoint, then revert the probe. Run the relevant behavior test and verify no duplicate listener remains.

**Project:** [backend/scripts/dev.mjs](evidence/node-backend-source-context.md#source-nri05) · symbol: `const build = spawn(process.execPath,`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/child_process.html).

<a id="nri06"></a>

### NRI06 · The service hangs on shutdown or restarts mid-delivery

**Priority:** start now. **Implementation:** Current source.

A local process does not exit after the SIGTERM termination signal, or an interrupted worker later repeats an event.

**Symptom:** A local process does not exit after SIGTERM, or an interrupted worker later repeats an event.

**Checks:** Inspect shutdown hooks, pool.end, worker stopping flags and disconnect calls. Check open sockets/timers and whether an external call can wait indefinitely. Determine whether an event was acknowledged before its database bookkeeping; repeated delivery can be a legitimate crash window.

**Repair:** Close owned resources with a bounded drain policy and let the supervisor enforce its stop deadline. Repair deduplication or restart/replay behavior if repeated delivery changes business results. Do not use immediate process.exit as a substitute for durable delivery safety.

**Recovery verification:** Send the SIGTERM termination signal in a local rehearsal, require exit within the stated deadline, then restart. Verify the service becomes healthy and pending events complete with one durable notification per event identity. Also test a forced termination, because graceful shutdown alone does not cover crashes.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-nri06) · symbol: `app.enableShutdownHooks();`.

**Lessons:** [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/api/process.html).

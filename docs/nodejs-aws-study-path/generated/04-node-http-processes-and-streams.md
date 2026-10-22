---
title: "Node APIs: HTTP, Buffer, files, paths and processes"
topic: "Node APIs: HTTP, Buffer, files, paths and processes"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Node APIs: HTTP, Buffer, files, paths and processes

Prerequisite: lesson 03. Learn the standard APIs beneath NestJS.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## HTTP parsing versus application validation

**What:** HTTP transports bytes, method, path and headers. Express parses a JSON body into a JavaScript value.

**How:** The parser limit controls memory exposure. A valid JSON number is still not a valid login object; Zod and business rules run after parsing.

**Real code:** [backend/src/main.ts · lines 46–47](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L46-L47).

```ts
app.use(json({ limit: '128kb' }));
app.useGlobalFilters(new ErrorFilter());
```

**Watch for:** Parser errors and schema errors can both be 400, but occur at different boundaries.

### Does successful JSON parsing establish a valid request?

No. It only establishes JSON syntax and decoding, not the domain contract.

## Buffer measures bytes

**What:** Buffer is Node’s binary-data representation. Text needs an encoding to become bytes or to be decoded from them.

**How:** Config checks UTF-8 secret byte length; password code decodes hex; Kafka code decodes UTF-8. Each conversion has a different purpose.

**Real code:** [backend/src/common/config.ts · lines 17–18](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/config.ts#L17-L18).

```ts
if (Buffer.byteLength(secret) < 32) throw new Error('JWT_SECRET requires at least 32 bytes');
const url = new URL(required('DB_URL'));
```

**Watch for:** JavaScript string length and UTF-8 byte length can differ for non-ASCII text.

### Why can an emoji need more bytes than its visible character count?

Unicode characters can occupy multiple bytes in UTF-8.

## fs/promises and bounded file reads

**What:** `readFile` resolves after reading a complete file. `readdir` lists entries; neither is an SQL or HTTP operation.

**How:** The migration runner reads small SQL files and filters by service prefix. Reading an unbounded upload into one Buffer would have different memory consequences.

**Real code:** [backend/src/common/database.ts · lines 31–35](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L31-L35).

```ts
const directory = join(process.cwd(), 'migrations');
const files = (await readdir(directory))
  .filter((file) => file.startsWith(`${name}.`) && /^.+\.\d{3}\.sql$/.test(file))
  .sort((a, b) => a.localeCompare(b, 'en'));
if (!files.length) throw new Error(`No migrations found for ${name}`);
```

**Watch for:** Streams are an extension for large data; the app does not already contain a streaming upload feature.

### When prefer a stream?

When data should be processed incrementally while respecting downstream capacity.

## cwd versus module location

**What:** `process.cwd()` is the directory from which the process runs. It need not be the directory containing the current module.

**How:** Database migrations are located relative to cwd. The supplied scripts set the expected execution context; launching dist/main.js elsewhere can break those file paths.

**Real code:** [backend/src/common/database.ts · lines 31–31](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L31-L31).

```ts
const directory = join(process.cwd(), 'migrations');
```

**Watch for:** A correct compiled file can still fail because its runtime working directory is wrong.

### What would import.meta.url describe instead?

The current module’s location, which can anchor paths independently of the launch directory.

## Child processes and watch mode

**What:** `spawn` starts another operating-system process with its own memory and lifetime. Watch mode restarts or recompiles on changes.

**How:** The development launcher first compiles TypeScript, then runs compiler watch and Node watch. Compilation and executing emitted JavaScript are separate jobs.

**Real code:** [backend/scripts/dev.mjs · lines 1–6](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/scripts/dev.mjs#L1-L6).

```js
import { spawn } from 'node:child_process';
const service = process.argv[2];
if (!['identity', 'catalog', 'inquiries', 'notifications'].includes(service)) {
  throw new Error('Expected service name');
}
const outDir = `dist-dev/${service}`;
```

**Watch for:** A source watcher does not validate every behavioral consequence of a change.

### Does one child process share variables with its parent?

No. Use explicit IPC, environment, files or network communication when coordination is needed.

## Signals and graceful resource cleanup

**What:** A signal tells a process about an event such as termination. Nest shutdown hooks allow registered cleanup methods to run.

**How:** Database closes its pool; workers disconnect. Crash-safe persistence is still needed because a forced kill or host loss may bypass graceful cleanup.

**Real code:** [backend/src/main.ts · lines 48–52](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L48-L52).

```ts
app.enableShutdownHooks();
const port = Number(process.env.PORT ?? 8181 + SERVICES.indexOf(service));
if (!Number.isInteger(port) || port < 1 || port > 65535)
  throw new Error('PORT must be a valid TCP port');
await app.listen(port, '0.0.0.0');
```

**Watch for:** process.exitCode allows pending work to finish; it does not forcibly close every leaked handle.

### Why keep the outbox if shutdown is graceful?

A crash can occur between external effects and local bookkeeping despite normal shutdown hooks.

## Practice and mastery

- In `work/bytes.mjs`, print `'😀'.length` and `Buffer.byteLength('😀')`. Expected: 2 UTF-16 units and 4 UTF-8 bytes.
- Read `Database.onModuleInit` and identify each filesystem operation, path operation and cryptographic operation.
- For a practice-only stream copy, use `pipeline` from `node:stream/promises` with file read/write streams. Compare byte counts afterward; keep it separate from application behavior.
- Use the project’s loopback inspector configuration to break on a handler. Do not expose the inspector publicly.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Node Buffer](https://nodejs.org/api/buffer.html)
- [Node streams](https://nodejs.org/api/stream.html)
- [Node child processes](https://nodejs.org/api/child_process.html)
- [Project example: HTTP parsing versus application validation](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L46-L47)
- [Project example: Buffer measures bytes](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/config.ts#L17-L18)
- [Project example: fs/promises and bounded file reads](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L31-L35)
- [Project example: cwd versus module location](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L31-L31)
- [Project example: Child processes and watch mode](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/scripts/dev.mjs#L1-L6)
- [Project example: Signals and graceful resource cleanup](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/main.ts#L48-L52)

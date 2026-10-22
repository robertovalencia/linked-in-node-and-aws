---
title: Node HTTP, buffers, files, processes and debugging
topic: Node runtime
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# The server beneath the framework

Prerequisite: 03. A process has its own memory, environment, sockets and lifetime. HTTP sends a method, URL, headers and optional body; the server produces a status, headers and optional body. JSON is an application convention on top of bytes. Nest/Express organize the same mechanics rather than replacing them.

## Runnable HTTP checkpoint

Save work/http.mjs and run node work/http.mjs in one terminal.

~~~js
import { createServer } from 'node:http';
const server = createServer((req, res) => {
  if (req.url !== '/health') {
    res.writeHead(404, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ detail: 'Unknown path' }));
  }
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ status: 'UP' }));
});
server.listen(8288, '127.0.0.1');
process.on('SIGTERM', () => server.close());
~~~

In another terminal run curl -i http://127.0.0.1:8288/health and curl -i http://127.0.0.1:8288/missing. Expect 200 JSON and 404 JSON. Stop with Ctrl-C. This server is only a teaching example; it is not the repository's entry point and is not a production template.

## Bytes, files and streams

A Buffer represents bytes; UTF-8 characters may take multiple bytes. Buffer.byteLength(secret) and secret.length answer different questions. Password comparison converts hex back to bytes, checks expected lengths and uses timingSafeEqual. Kafka message.value is a Buffer, so the consumer decodes UTF-8 before JSON parsing.

readFile reads an entire file into memory; this is reasonable for small migration and seed files. A large export should use streams. A readable produces chunks, a writable consumes them, and backpressure keeps the faster side from growing memory indefinitely. A scratch extension can copy a file with await pipeline(createReadStream(source), createWriteStream(destination)); import pipeline from node:stream/promises and the file streams from node:fs. This application does not currently implement file-upload or export streams.

Paths from process.cwd() depend on where the process starts, whereas import.meta.url identifies the module location. Database migrations are loaded from the backend working directory. Starting dist/main.js from the wrong folder can produce missing-migration errors even when the file exists elsewhere.

## Read the application

backend/src/main.ts disables the default parser, installs helmet and a 128kb JSON limit, registers ErrorFilter, enables shutdown hooks and listens on 0.0.0.0. In a container that permits its mapped network interface; Compose binds published local ports to loopback. backend/src/common/config.ts validates environment variables. backend/scripts/dev.mjs and scripts/dev.mjs coordinate subprocesses; inspect process spawning, output forwarding and termination rather than assuming one process starts all four capabilities internally.

## Debugging lab

Run node --inspect=127.0.0.1:9229 work/http.mjs and attach a local debugger; never expose the inspector publicly. Break in the handler, send curl again, and inspect req.url and res.statusCode. Then intentionally reuse port 8288 and explain EADDRINUSE. Change the unused scratch server port rather than killing unknown processes. Finally test a small file copy stream and compare the byte length of the input and output using node:fs/promises stat.

## Senior tradeoffs and interview answers

Graceful shutdown means stop accepting traffic, finish or bound in-flight work, stop workers, and release connections. The repository installs lifecycle hooks and disconnects resources, but that is not proof of fully coordinated draining under every signal/race. Review and test that behavior before promising it. process.exitCode allows the runtime to finish pending work; immediate process.exit can truncate output or work.



### Why a request size limit?

To bound parsing/memory exposure.

### Does Buffer length equal character count?

Not for general UTF-8 text.

### When use streams?

When processing incremental or large data while preserving backpressure.

- [ ] Produce and explain 200/404 HTTP responses.
- [ ] Show byte versus character length with an emoji.
- [ ] Diagnose EADDRINUSE and a wrong working directory safely.
- [ ] Explain why a stream example is an extension rather than existing application behavior.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Node streams](https://nodejs.org/api/stream.html) — accessed 2026-10-22.
- [HTTP](https://nodejs.org/api/http.html) — accessed 2026-10-22.
- [Project source: backend/src/main.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/main.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/config.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/config.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/scripts/dev.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/scripts/dev.mjs) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: scripts/dev.mjs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/scripts/dev.mjs) — local baseline inspected 2026-10-22; private published source may lag.

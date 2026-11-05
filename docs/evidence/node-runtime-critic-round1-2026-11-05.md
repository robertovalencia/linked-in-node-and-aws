# Independent Node runtime critic · 5 November 2026

Reviewer: separate runtime critic agent, not the builder. Scope: NR01–NR42 and NRI01–NRI06 in `docs/nodejs-aws-study-path/node-runtime-items.json`, the credential-free runtime lab, current application source, and the relationship to existing lessons 01–04/19. This is a section review; it is not the final integrated anonymous comparison or a production verification.

I read AGENTS.md, README.md, CONTRACT.md, requirements and architecture before reviewing. I opened [Devinterview's Node interview reference](https://github.com/Devinterview-io/node-interview-questions) before the review. Its breadth is useful, but its statement that ordinary EventEmitter listeners execute asynchronously is incorrect. I checked disputed behavior against primary Node documentation rather than copying that answer.

## Initial decision and largest gap

**Repair required.** The initial lab passed its normal run but did not correctly own both worker-event promises on failure. It created `once(worker, 'message')` and `once(worker, 'exit')`, then awaited them sequentially. A worker error rejects both; the exit promise could become an unhandled rejection while the first rejection unwound cleanup. This directly weakened the lab's teaching about error ownership.

I confirmed the gap in a disposable `/tmp` copy by replacing the worker's `postMessage` with `throw new Error('injected-worker-failure')`. Under `node --unhandled-rejections=warn`, the corrected fault probe exited 1 and printed both `UnhandledPromiseRejectionWarning` and the propagated worker error. The builder source was not modified by the critic. An earlier probe had an incorrectly quoted replacement and failed with a syntax error; that result was discarded as a probe-construction failure, not evidence about the lab.

Concrete repair requested: observe both promises immediately using `Promise.all`, include an expected failed-worker case, assert the worker exit status, and await worker completion before temporary files are removed. The builder implemented the shared rejection ownership and expected throw case; subsequent independent normal execution passed. Final exit-status verification is recorded below after reinspection.

## Other findings and repairs

1. **NR29 environment inheritance was inaccurate.** The original answer said a child inherits only explicitly supplied environment/options. `spawn` defaults to `process.env`, and the actual build/compiler watcher supplies no `env`. Requested repair: state default inheritance, explain replacement when `env` is supplied and the need to spread preserved values. The builder corrected the answer. [Node child-process defaults](https://nodejs.org/docs/latest-v22.x/api/child_process.html#child_processspawncommand-args-options).
2. **Pipeline failure proved rejection but not resource closure.** Requested explicit stream references and destroyed/closed assertions after the missing-input rejection. The builder added these assertions; independent rerun passed. The source still uses a bounded 200,000-byte file; digest comparison is a correctness check, not a claimed constant-memory benchmark. [Node pipeline error destruction](https://nodejs.org/docs/latest-v22.x/api/stream.html#streampipelinesource-transforms-destination-callback).
3. **Existing lesson links needed honest scope.** Original lessons 03/04/19 do not teach all newly researched scheduling, EventEmitter, stream, context and memory material. This task is a supplementary questionnaire, so rewriting/renumbering existing lessons is unnecessary. The builder added prerequisite/related-mechanism labels for extensions. Historical pinned excerpts can differ from current source; questionnaire current-source metadata was checked independently. JSON, numeric conversion, Date and URL additions should receive the same relationship disclosure when their prerequisite lessons lack a taught section.

## Actual checks

- Executed `node docs/nodejs-aws-study-path/labs/node-runtime/run.mjs` independently before repair: Node **v22.14.0**, exit **0**, **10** named groups passed.
- Executed the same command after shared-promise/pipeline repairs: Node **v22.14.0**, exit **0**, **10** groups passed. Groups included synchronous EventEmitter ordering/error, distinct CJS/ESM scheduling, closure/copy/UTF lengths, equal stream bytes and failure closure, 100 consumed backpressured chunks, isolated asynchronous contexts, worker result/exit and failed-worker rejection, literal shell metacharacters/nonzero child rejection, timeout abortion and conversion/query edge cases.
- Independently loaded all **48** metadata entries, checked that each source path exists, each literal source symbol and full excerpt occurs in that file, each SHA-256 matches actual source bytes, and every mapped lesson exists. **Zero discrepancies** at the inspected revision. This is local source validation, not verification of private GitHub publication.
- Read actual `password.ts`, `messaging.ts`, database/connections/config/errors, launchers, `main.ts` and compiler/package settings. Native async scrypt uses libuv worker capacity; it is not a JavaScript worker-thread job pool. No streaming upload, custom worker pool, AsyncLocalStorage request middleware or heap-capture workflow is claimed as implemented. Five absent-feature entries have official worked-example URLs and specific useful practice instructions.
- All six incidents contain symptom, checks, repair and recovery. They are diagnostic scenarios, not claims that those failures were reproduced in the four-service application during this review. Recovery instructions preserve migration history, durable outbox/deduplication and local/cloud isolation.
- No AWS, external publication, secret file read, application mutation or Java-project edit was performed. Application-wide npm check/test/build/acceptance are the integrating agent's separate responsibility; this section critic ran the relevant runtime lab and independent metadata checks.

## Technical source checks

- [Node EventEmitter](https://nodejs.org/docs/latest-v22.x/api/events.html#asynchronous-vs-synchronous) confirms synchronous registration-order listeners; error events and returned promises need explicit ownership. NR22 and the runnable example correctly avoid the reference's asynchronous-listener mistake.
- [Node process scheduling](https://nodejs.org/docs/latest-v22.x/api/process.html#when-to-use-queuemicrotask-vs-processnexttick) distinguishes CJS from ESM microtask context. The lab compares two explicit entry points and does not claim universal callback ordering. [Event-loop guide](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick) supports the context-qualified immediate/timer explanation.
- [Node crypto](https://nodejs.org/docs/latest-v22.x/api/crypto.html#cryptoscryptpassword-salt-keylen-options-callback), [worker threads](https://nodejs.org/docs/latest-v22.x/api/worker_threads.html) and [do not block guide](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) support the distinction between native pool work and JavaScript computation.
- [Node stream buffering](https://nodejs.org/docs/latest-v22.x/api/stream.html#buffering) supports false-as-backpressure and highWaterMark-as-threshold. The small slow Writable checks actual drain waits and counts, without manufacturing memory limits.
- [Node child processes](https://nodejs.org/docs/latest-v22.x/api/child_process.html) supports no-shell argument arrays, inherited environment and separate process memory. The lab executes a fixed Node binary; the supplied metacharacter payload remains literal. It makes no claim that argument arrays remove called-program option/path validation.

The official `latest-v22.x` pages inspected identify themselves as v22.23.4; the installed runtime used for execution is v22.14.0. Unversioned official links can show newer APIs; the examples reviewed use APIs available in the installed Node 22 baseline.

## Independent repair re-review and section decision

**Runtime section accepted after repair.** I inspected the final worker code: both event promises are joined before either is awaited; the failing worker has a separate exit observer installed before execution, its rejection is asserted, and the observed nonzero exit is awaited before temporary-directory cleanup. I independently executed the final lab using `node --unhandled-rejections=warn docs/nodejs-aws-study-path/labs/node-runtime/run.mjs`: exit **0**, all **10** groups passed, and no warning appeared. I reran the full 48-item literal-source/excerpt/hash/lesson-path check: zero discrepancies. NR36–NR39 also now explicitly disclose the prerequisite/related-source lesson relationship.

The reviewed artifact SHA-256 values were:

- `node-runtime-items.json`: `18ad346e8eace4e965959f9a8be226883bb2bf5d153d996d855a8b5b6ce3e794`
- `labs/node-runtime/run.mjs`: `9a83d71ecf201d39c37664990431520efdc74ee4673ef8dca07651074b45ee33`

For this repository-specific runtime learning section, I prefer the repaired candidate to the fetched reference: it gives correct synchronous EventEmitter behavior, context-qualified scheduling, runnable expected failures, precise current-source anchors and explicit absent-feature boundaries. This was an identified-source technical comparison, **not** the requested final integrated anonymous comparison. It does not establish production shutdown deadlines, workload memory bounds, CPU throughput, cloud deployment or service-outage recovery; those remain explanations or separately scoped application tests, not achievements claimed by this lab. No blocking runtime-content defect remains in the reviewed artifacts.

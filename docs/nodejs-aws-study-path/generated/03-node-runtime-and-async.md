---
title: Node event loop, promises and resource limits
topic: Node runtime
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Node concurrency without the myths

Prerequisites: 01–02. One Node process commonly runs application JavaScript on one main thread. Network operations can progress while a handler awaits their results. Some operations, including asynchronous password derivation, use native worker-pool resources. “Single-threaded” does not mean one request at a time and does not protect database invariants.

## A runnable scheduling experiment

Save as work/scheduling.mjs and run node work/scheduling.mjs.

~~~js
console.log('start');
setTimeout(() => console.log('timer'), 0);
Promise.resolve().then(() => console.log('promise'));
await Promise.resolve();
console.log('after await');
~~~

Expected order in this self-contained ESM example: start, promise, after await, timer. Synchronous code runs first, promise continuations run before the later timer callback here, and a zero delay is not an immediate execution promise. Do not memorize one ordering diagram as proof for all combinations of timers, I/O and process.nextTick across module contexts. Make the scheduling context explicit.

An async function always returns a promise. await pauses that function's continuation, leaving the runtime free to do other work; it does not create a thread. Promise.all aggregates promises and rejects if any rejects. Calls used to construct those promises start the operations before or during argument evaluation; Promise.all does not invoke an array of function values. Promise.allSettled reports every outcome. Neither automatically limits concurrency or cancels other operations. A list of 100,000 started requests aggregated with Promise.all can exhaust sockets or a database pool.

## Where this matters in the project

backend/src/identity/password.ts promisifies scrypt rather than hashing synchronously in the request path. backend/src/common/database.ts limits each pool to ten clients; with four processes the configured maxima add up to forty, not ten globally. backend/src/common/messaging.ts runs background loops and uses unref timers. unref lets a timer stop keeping the process alive on its own; it is not cancellation. frontend/src/hooks/useMarketplace.ts uses Promise.all for at most three comparison profiles, which is a deliberately bounded set.

The inquiry handler holds a database connection and a transaction while awaiting an internal catalog lookup. That means a slow external dependency consumes scarce connection capacity and prolongs the idempotency lock. The five-second timeout bounds that specific wait. Moving the lookup outside the transaction could reduce lock time, but changes duplicate-replay and consistency behavior; validate those tradeoffs first.

## Lab: show starvation and repair the design

In a scratch Node script start a 20 ms interval, then run a CPU loop for about 300 ms using performance.now(). Record the observed gap in interval output. Replace the busy loop with an awaited 300 ms timer and compare. The timer version allows ticks while waiting; adding async before a CPU-heavy function alone does not repair starvation. Proposed extensions for actual heavy CPU work include worker_threads or an external job worker with bounded concurrency; neither is implemented here.

Then implement runLimited(tasks, limit) for ten synthetic promises with a maximum of two active tasks. Log active counts and assert the maximum never exceeds two even if a task rejects. Explain how you would stop accepting new work and await in-flight tasks during shutdown. This is more useful than knowing the names of all event loop phases.

## Debugging and senior tradeoffs

When latency rises, distinguish event-loop blocking, worker-pool contention, pool exhaustion, network waiting and downstream failure. Use timestamps, CPU profiles, pending connection counts and request traces; an increase in CPU does not automatically mean the database needs an index. async loops still need backoff, cancellation and an error policy. Catching an error and continuing forever can conceal a broken dependency.

Interview:

### Does await prevent duplicate inquiries?

No. Separate handlers and replicas interleave; the PostgreSQL advisory lock plus uniqueness constraint protects the invariant.

### Why not Promise.all every SQL query?

Related transaction operations require one connection and ordered semantics; unrelated work may still need concurrency bounds.

- [ ] Predict and verify scheduling output.
- [ ] Demonstrate blocking with measured timer delay.
- [ ] Explain why async scrypt can still contend for limited native resources.
- [ ] Calculate aggregate pool demand and identify the network-in-transaction tradeoff.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Node event loop and worker-pool guidance](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) — accessed 2026-10-22.
- [Project source: backend/src/identity/password.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/identity/password.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/database.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/database.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/messaging.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/messaging.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/inquiries/inquiries.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/inquiries/inquiries.service.ts) — local baseline inspected 2026-10-22; private published source may lag.

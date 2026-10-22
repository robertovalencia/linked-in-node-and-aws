---
title: "Node runtime: event loop, promises and resource limits"
topic: "Node runtime: event loop, promises and resource limits"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Node runtime: event loop, promises and resource limits

Prerequisites: lessons 01–02. The examples come from the services and their supporting React client.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## await suspends one continuation

**What:** The event loop lets Node run JavaScript callbacks while network operations wait. Await pauses the current async function until its promise settles.

**How:** Other handlers can progress while a database request waits. That is why two requests can race even when application JavaScript usually executes on one main thread.

**Real code:** [backend/src/identity/identity.service.ts · lines 47–50](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L47-L50).

```ts
const result = await this.db.query(
  'SELECT email,name,role,password_hash FROM accounts WHERE email=$1',
  [email.toLowerCase()],
);
```

**Watch for:** Single-threaded JavaScript is not a database lock.

### Does await block every HTTP request?

No. It pauses the awaiting function’s continuation, not all request processing.

## Worker pool versus JavaScript CPU work

**What:** Some native async APIs use worker-pool resources; scrypt is one example. CPU-heavy JavaScript still occupies the main thread unless explicitly moved elsewhere.

**How:** Async password derivation lets the main loop handle other I/O. Capacity remains finite; parallel derivations can contend for CPU, memory and worker threads.

**Real code:** [backend/src/identity/password.ts · lines 6–7](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L6-L7).

```ts
const hash = (await scrypt(password, salt, 64)) as Buffer;
return `scrypt:${salt}:${hash.toString('hex')}`;
```

**Watch for:** An async keyword does not offload a long JavaScript loop.

### Why does CPU work still affect latency?

Finite CPU and worker capacity must serve all active work, even when a particular API is asynchronous.

## Promise aggregation is not a concurrency limiter

**What:** `Promise.all` aggregates promises and rejects when one rejects. It does not call function values or cancel other work automatically.

**How:** The map invokes providerService.get for each compared ID before the aggregate settles. This application caps comparisons at three, which bounds that particular fan-out.

**Real code:** [frontend/src/hooks/useMarketplace.ts · lines 123–127](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L123-L127).

```ts
Promise.all(compare.map((id) => providerService.get(id, controller.signal)))
  .then((items) => {
    if (!controller.signal.aborted) setCompareProviders(items);
  })
  .catch((error) => {
```

**Watch for:** Building 100,000 fetch promises can start 100,000 operations; Promise.all does not queue them safely.

### Where does the concurrent work start here?

In each providerService.get call made by map, not in a later magical scheduler inside Promise.all.

## Timers, delays and unref

**What:** `setTimeout` makes a callback eligible after a delay; it does not promise an exact execution time.

**How:** The worker wraps a timer in a promise for retry pacing. unref means this timer alone need not keep the Node process alive.

**Real code:** [backend/src/common/messaging.ts · lines 8–12](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L8-L12).

```ts
const pause = (ms: number) =>
  new Promise<void>((resolve) => {
    setTimeout(resolve, ms).unref();
  });

```

**Watch for:** unref does not cancel the timer or stop network calls.

### Can a 500ms timer run late?

Yes. Busy JavaScript or other runtime scheduling can delay the callback.

## Detached promises need their own error policy

**What:** Calling an async function starts it and returns a promise. `void` discards the result expression; it does not suppress a rejection.

**How:** The messaging bootstrap launches a loop. That loop catches expected failures and retries; a blocking bootstrap await of the entire infinite loop would prevent normal startup completion.

**Real code:** [backend/src/common/messaging.ts · lines 22–24](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L22-L24).

```ts
onApplicationBootstrap(): void {
  void this.run();
}
```

**Watch for:** Ignoring a rejected promise can create an unhandled rejection rather than a safe background task.

### What does void this.run actually guarantee?

Only that the returned promise is intentionally unused at that call site.

## Connection budgets create backpressure

**What:** Backpressure prevents producers from creating more work than a consumer can handle. A bounded pool is one resource limit.

**How:** With max=10, additional database work waits for a connection. A slow Catalog fetch inside an inquiry transaction occupies one of those connections while waiting on another service.

**Real code:** [backend/src/common/database.ts · lines 12–13](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L12-L13).

```ts
max: 10,
connectionTimeoutMillis: 5000,
```

**Watch for:** A pool limit does not by itself define a complete HTTP overload or timeout policy.

### Why can an idle-CPU API still be slow?

It may be waiting for connections or downstream I/O rather than computing.

## Practice and mastery

Save as `work/scheduling.mjs`, then run `node work/scheduling.mjs`:

```js
console.log('start');
setTimeout(() => console.log('timer'), 0);
Promise.resolve().then(() => console.log('promise'));
await Promise.resolve();
console.log('after await');
```

Expected for this self-contained ES module: `start`, `promise`, `after await`, `timer`.

- Start a 20ms interval and compare a 300ms busy loop with an awaited 300ms timer. Measure the gap; do not assume exact timing.
- Implement a two-at-a-time runner for ten synthetic tasks, including a rejection. Assert its active count never exceeds two.
- Worker threads or external CPU jobs are possible extensions; the current services do not implement them.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Node event loop and worker pool](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop)
- [Project example: await suspends one continuation](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/identity.service.ts#L47-L50)
- [Project example: Worker pool versus JavaScript CPU work](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/identity/password.ts#L6-L7)
- [Project example: Promise aggregation is not a concurrency limiter](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/frontend/src/hooks/useMarketplace.ts#L123-L127)
- [Project example: Timers, delays and unref](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L8-L12)
- [Project example: Detached promises need their own error policy](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/messaging.ts#L22-L24)
- [Project example: Connection budgets create backpressure](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/backend/src/common/database.ts#L12-L13)

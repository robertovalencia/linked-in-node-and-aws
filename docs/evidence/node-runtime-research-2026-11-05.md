# Runtime/language builder research · November 5, 2026

Scope: builder research and local example execution for the Node.js/backend questionnaire. This is not an independent approval or a claim of application, cloud, GitHub or reader publication. Read both projects’ applicable AGENTS.md instructions, marketplace README/contract/requirements/architecture, both copies of lessons 01–04, lesson 19’s finer source-concept table and actual current source before authoring. Numbered lessons and personal files were not changed.

## Coverage decision

The two lesson profiles teach the same 24 substantive headings in lessons 01–04. The output has 42 questions and six incident cards: one question per heading where useful, separate questions for high-risk mechanisms, and added source-table/interview gaps. Counts follow coverage, not the reference’s title. Additional coverage includes EventEmitter synchronous order/error handling; callback/promisify relationships; timer context; worker threads/cluster; stream types/pipeline/drain; request context; memory investigation; JSON/regular expressions/Date/URL; utility and type-only imports; process path anchoring/groups; and safe shell-free spawning. It links current real source with exact literal excerpts and SHA-256-at-inspection values. Absent streaming upload, worker/cluster job infrastructure, AsyncLocalStorage context and built-in memory diagnosis are explicitly labeled absent; nearby source is a contrast, not evidence those features exist.

## Reference inspected before writing

Fetched and inspected [Devinterview Node questions](https://github.com/Devinterview-io/node-interview-questions) through the browser research tool, then located its event-driven and nonblocking sections. The reference says EventEmitter callbacks are asynchronous by default and attributes parallelism to callbacks/promises/async-await. Official Node events documentation establishes synchronous listener calls in registration order; worker documentation distinguishes parallel JavaScript from asynchronous waiting. Those are consequential beginner misconceptions, not stylistic preferences. Our answers explain the request consequence and use this project’s database pool error handler, async scrypt, outbox loop and ESM module setup.

## Primary-source verification

Opened all URLs below with the web research tool on November 5. For JavaScript language mechanisms, ECMA-262 is the normative language specification; MDN’s maintained JavaScript documentation was also opened for accessible closure and Promise.all explanations. Node’s unversioned API pages currently resolve to v26.13.0, newer than this project’s >=22 <25 engine range. Answers use established APIs already available in Node 22 and were locally exercised on v22.14.0; they do not imply Node 26 support. Opened version-22 events, streams, process, filesystem and crypto pages successfully. Attempts at several other latest-v22 API pages returned research-tool accessibility errors; their successfully opened unversioned official counterparts support the stable behavior, without claiming the failed requests succeeded.

- [developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Closures)
- [developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)
- [nodejs.org/api/async_context.html](https://nodejs.org/api/async_context.html)
- [nodejs.org/api/buffer.html](https://nodejs.org/api/buffer.html)
- [nodejs.org/api/child_process.html](https://nodejs.org/api/child_process.html)
- [nodejs.org/api/cluster.html](https://nodejs.org/api/cluster.html)
- [nodejs.org/api/crypto.html](https://nodejs.org/api/crypto.html)
- [nodejs.org/api/esm.html](https://nodejs.org/api/esm.html)
- [nodejs.org/api/globals.html](https://nodejs.org/api/globals.html)
- [nodejs.org/api/http.html](https://nodejs.org/api/http.html)
- [nodejs.org/api/path.html](https://nodejs.org/api/path.html)
- [nodejs.org/api/process.html](https://nodejs.org/api/process.html)
- [nodejs.org/api/timers.html](https://nodejs.org/api/timers.html)
- [nodejs.org/api/url.html](https://nodejs.org/api/url.html)
- [nodejs.org/api/util.html](https://nodejs.org/api/util.html)
- [nodejs.org/api/worker_threads.html](https://nodejs.org/api/worker_threads.html)
- [nodejs.org/docs/latest-v22.x/api/events.html](https://nodejs.org/docs/latest-v22.x/api/events.html)
- [nodejs.org/docs/latest-v22.x/api/fs.html](https://nodejs.org/docs/latest-v22.x/api/fs.html)
- [nodejs.org/docs/latest-v22.x/api/stream.html](https://nodejs.org/docs/latest-v22.x/api/stream.html)
- [nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop)
- [nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick](https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick)
- [nodejs.org/en/learn/getting-started/introduction-to-nodejs](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs)
- [tc39.es/ecma262/multipage/ecmascript-language-expressions.html](https://tc39.es/ecma262/multipage/ecmascript-language-expressions.html)
- [tc39.es/ecma262/multipage/ecmascript-language-statements-and-declarations.html](https://tc39.es/ecma262/multipage/ecmascript-language-statements-and-declarations.html)
- [tc39.es/ecma262/multipage/indexed-collections.html](https://tc39.es/ecma262/multipage/indexed-collections.html)
- [tc39.es/ecma262/multipage/keyed-collections.html](https://tc39.es/ecma262/multipage/keyed-collections.html)
- [tc39.es/ecma262/multipage/numbers-and-dates.html](https://tc39.es/ecma262/multipage/numbers-and-dates.html)
- [tc39.es/ecma262/multipage/structured-data.html](https://tc39.es/ecma262/multipage/structured-data.html)
- [tc39.es/ecma262/multipage/text-processing.html](https://tc39.es/ecma262/multipage/text-processing.html)
- [www.typescriptlang.org/docs/handbook/2/everyday-types.html](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)
- [www.typescriptlang.org/docs/handbook/2/generics.html](https://www.typescriptlang.org/docs/handbook/2/generics.html)
- [www.typescriptlang.org/docs/handbook/2/modules.html](https://www.typescriptlang.org/docs/handbook/2/modules.html)
- [www.typescriptlang.org/docs/handbook/2/narrowing.html](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)
- [www.typescriptlang.org/docs/handbook/utility-types.html](https://www.typescriptlang.org/docs/handbook/utility-types.html)
- [www.typescriptlang.org/tsconfig/emitDecoratorMetadata.html](https://www.typescriptlang.org/tsconfig/emitDecoratorMetadata.html)

## Actual local examples executed

Ran one isolated `node --input-type=module` program on **v22.14.0**, using `node:assert/strict`, a disposable temporary directory and no application processes. Exit code **0**. Ten assertion groups passed:

1. EventEmitter order was before → listener → after.
2. The self-contained ESM scheduling example produced start → promise → after await → timer; no universal top-level immediate/timer or nextTick/ESM ordering claim was tested.
3. Emoji string length was two UTF-16 code units and UTF-8 Buffer byte length was four.
4. Closure counter returned 1,2 and a shallow nested-array copy changed the original.
5. `pipeline` copied 200,000 bytes exactly; missing source rejected.
6. Slow Writable with 16-byte highWaterMark produced 100 chunks, observed 100 drain waits and consumed all 100. This is an observed run, not a general peak-memory benchmark.
7. Two overlapping AsyncLocalStorage runs retained separate request IDs.
8. A disposable worker module returned 144 for input 12 and exited.
9. `promisify(execFile)` invoked the fixed Node executable with an argument array and returned the expected version.
10. URLSearchParams round-tripped an ampersand-containing value; Number("") returned 0 and parseInt("12oops",10) returned 12.

The temporary files were removed in finally. The current JSON source map was also checked programmatically: every literal source symbol occurs in its excerpt and every excerpt is present in its real source file. No fresh HTTP acceptance, full npm suite, worker production deployment or live memory profile is claimed by these small examples. The parent integration adds repeatable validation and independent criticism.

## Builder’s largest gap and repair

The first pass covered lesson headings but missed finer source-table concepts: JSON, regular expressions, Date, URL/URLSearchParams, Record/ReturnType/Omit, type-only imports and process-location/process-group behavior. The inventory critic independently pointed out that gap. Added NR36–NR42 with exact current source and verified primary references, preserving the original questions rather than reducing the coverage bar.

## Packaged runnable lab added after integration request

Executed `node docs/nodejs-aws-study-path/labs/node-runtime/run.mjs` from the repository root. Exit **0**, Node **v22.14.0**, JSON output `passed: 10`. The packaged lab is the repeatable replacement for the initial scratch experiment. It adds isolated CommonJS/ESM entry-point scheduling comparisons, an unhandled EventEmitter error assertion, literal shell-metacharacter child arguments and nonzero child failure, and a timeout-abort assertion. It also preserves the pipeline output/error, slow-writable drain, worker result, context-isolation, language-value and input-conversion assertions. Temporary files are removed in `finally`; no cloud credentials, application database, broker or public listener is used.

Run the same command from a clean checkout, or run `node labs/node-runtime/run.mjs` from the extracted `NodeJs-AWS` study pack. Expected: exit zero and ten named checks in the JSON result; the reported Node patch version is the runtime actually used. Scheduling assertions are scoped to the two isolated entry points, not to arbitrary request callbacks. Timing-dependent assertions only require a supported operation to be aborted; they do not demand exact wall-clock completion.

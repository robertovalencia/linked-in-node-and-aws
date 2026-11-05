# Node/backend lesson inventory and initial critic · November 5, 2026

This is an independent inventory and initial coverage critique, not approval of a questionnaire that had not yet been completed. The inventory agent did not build questionnaire answers. No application, cloud, publication or external-reader operation occurred.

Both applicable agreements were read before work: this repository's `AGENTS.md` and `/Users/robertovalencia/Documents/Business/Interview process/AGENTS.md`. The external profile has no additional `AGENTS.md`. README, contract, requirements and architecture were read. The external project was read only; its personal note contents were excluded.

## Actual inventory

[Machine-readable inventory](../nodejs-aws-study-path/node-backend-lesson-inventory.json) records exact paths, SHA-256 file hashes, every Markdown heading outside code fences, table first-column indexes, scope/reason, backend concept lists and existing AWS questionnaire card mappings. The extractor read complete lesson texts; manual deeper review covered core/toolchain/reliability lessons, backend concept tables, service handbooks, setup/application walkthroughs and the cloud lessons' backend overlaps.

| Set | Observed content |
|---|---|
| Marketplace study path | All 84 numbered lessons, IDs00–83 |
| Interview-process NodeJs/AWS profile | All corresponding 84 numbered lessons plus README; personal progress excluded |
| Marketplace supplementary material | 10 handbook guides including its index;12 walkthrough guides including its index |
| Navigation | Both study-path READMEs inventoried separately |

Only17 paired lessons are byte-identical:01–14 and16–18. The other67 differ exclusively in Markdown link destinations. Replacing only Markdown link destinations yields exact complete-text equality for all84 pairs. The external reader uses `/guide/nodejs-aws--...` destinations and some pinned supplementary links; it is not a separate teaching syllabus. This check does not equate byte identity with conceptual coverage. No lesson ID or original content was changed.

Deterministic checks executed successfully: unique IDs exactly00–83; all84 external counterparts exist; all84 complete normalized texts match;22 unique supplementary paths; every lesson/guide has headings and a scope reason. No personal-file extraction was performed. The temporary extractor was `/tmp/node-lesson-inventory.py`; the retained JSON contains its results and check descriptions.

## Required coverage beyond the obvious service chapters

The largest initial risk is counting questions rather than mapping the whole syllabus. Lessons01–10 are necessary but insufficient. The JSON's `node_backend_concepts` list is the checklist for mixed lessons; blank cloud-only lists mean infrastructure scope, not uninspected files.

- Lesson12 teaches HTTP-status rejection versus network failure, cancellation versus uncertain server writes, stale read responses and preserving the original idempotency key/payload. React portals/focus/effect ownership remain frontend topics, while server validation and API-owned data matter to this guide.
- Lessons13–14 add mocks versus integration evidence, deterministic race tests, ESM test transforms, lint/type/format distinctions, browser proof, separate npm scopes, reproducible installation, build versus startup, migration packaging, process supervision, host/container DNS and listener context.
- Lessons15/17 and walkthroughs01–02 add setup tools, `.env` versus existing database-volume credentials, modes/ports, contract-first request tracing, quality gates, dependency review and exact source/image release identity. OIDC means OpenID Connect; configuration is not verified integration execution.
- Lesson16 adds complete request budgets versus one operation timeout, health boundaries, shared failure domains, optimistic conflict detection versus row locks and rollback versus data restore. The Catalog currently lacks version/ETag conflict checking.
- Lessons26–29/31/40–41 and50–56 add immutable images, secrets, access patterns, observability, TLS/proxy health, cache freshness, process scaling and schema-compatible release rollback. Preserve infrastructure details in the AWS companion while explaining backend consequences.
- Lessons57–63 add pool reconnection/failover, recovery objectives, cache-aside/TTL/invalidation/stampedes, DynamoDB query/key/hot-key/conditional-write semantics, partitions/replicas/acknowledgments, messaging alternatives, visibility/delete crash windows, FIFO group order, dead-letter queues, partial-batch failures, workflow compensation, serverless invocation-specific retry/concurrency, storage lifetime and secret rotation.
- Lessons65–68/79–80/83 add log/metric/trace/audit distinctions, bounded labels/privacy/sampling, trace context versus event identity, service indicators/objectives/error budgets, hypothesis-led incidents, restore verification, trust boundaries and requirements-to-release evidence.
- Lesson19's tables enumerate individual dependencies and APIs. Inspect those rows rather than treating the lesson's broad title as sufficient. Installed RxJS does not establish an application Observable pipeline; installed type declarations do not validate runtime input. The guide must clearly label absent ORM, Passport, Swagger, Nest ConfigModule, WebSocket/SSE, dead-letter handling, workers, tracing, cache and serverless examples.

## Initial reference and technical critique

The requested [Devinterview reference](https://github.com/Devinterview-io/node-interview-questions) was fetched through web browsing before this report. Its event-driven and nonblocking explanations are suitable equivalent topics for a later anonymous comparison, but two claims require correction: EventEmitter listeners are synchronous by default, and callbacks/Promises do not create parallel JavaScript execution. Node's [events documentation](https://nodejs.org/api/events.html#asynchronous-vs-synchronous) establishes listener order and scheduling. The [event-loop and worker-pool guide](https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop) explains the distinct execution resources and why either can be saturated. Both were opened on November5.

The new guide should show tiny runnable observations for those distinctions, then connect them to a concrete project mechanism such as asynchronous password work or outbox polling. Exact timer order needs an explicit CommonJS/ES-module and I/O context. Increasing thread or connection counts is not a substitute for identifying the constrained resource.

[Official Nest lifecycle guidance](https://docs.nestjs.com/fundamentals/lifecycle-events) and [Node stream pipeline documentation](https://nodejs.org/api/stream.html#streampipelinesource-transforms-destination-callback) were also opened. Nest shutdown hooks require enabling; actual `main.ts` does this. Streams need bounded producer/consumer flow and failure cleanup; no custom streaming endpoint should be invented from an installed Express adapter.

Actual source inspection included `main.ts`, config, health, messaging and inquiry creation. `/health/serve` currently checks PostgreSQL while allowing durable inquiry writes during Kafka retry; `/health/ready` additionally checks worker state. Broker acknowledgments and SQL commits remain separate, and notification deduplication is event-based. The old handbooks contain EC2-only deployment statements from their historical checkpoint. Preserve those lessons, but label historical context in the new guide and anchor current behavior to actual source and dated records.

## Largest gap and required repair

**Largest gap:** a polished core-only questionnaire could omit the cloud lessons' backend concepts and treat a lesson number as proof. **Repair required:** link every retained backend concept to a stable question/incident ID with an actual explanation; route infrastructure-only topics to exact existing AWS cards/lessons. Add researched gaps explicitly, label absent implementations, and test portable source excerpts and archive contents. A later separate critic must assess the final answers, failure paths, actual output and anonymous comparison; this inventory makes no winner selection.

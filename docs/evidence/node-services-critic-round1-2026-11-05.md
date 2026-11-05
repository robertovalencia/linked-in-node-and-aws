# Node service learning companion: independent critic, round 1

Date: November 5, 2026. Reviewer: the independent service critic agent; this agent did not build the questionnaire. Scope: `node-services-items.json`, current backend implementation, lessons 05–10/16, and the beginner service handbooks/walkthroughs. This is a section review, not approval of the integrated reader, ZIP, publication, or cloud runtime.

**Verdict: repair required.** The largest gap is recovery guidance that can leave a live Notifications process permanently idle after a handler failure. Correct source excerpts and green unit tests do not close that operational gap.

## Inspected artifact and actual checks

The initial draft contained 49 questions and 9 incidents. The builder added NS50–NS54 during this review. The subsequently inspected 63-item JSON has SHA-256 `1b3b2686d7c6e7be6063fc36d926018fc0625cc1f9cb97a8a626b9368825ca27`.

- An independent Python read checked every item's source-file SHA-256, literal symbol and full excerpt against disk: 63 items, 17 distinct source files, zero mismatches. All listed lesson files exist. IDs are unique. This verifies provenance, not semantic completeness or rendered links.
- Read the Nest registration, database wrapper/options, JWT/guard/password code, all four service paths, worker loops and health handlers. Compared the explanations with the API/event contract and existing source-linked lessons.
- Executed `npm --prefix backend test -- --runTestsByPath test/security.spec.ts test/workflows.spec.ts`: 2 suites passed, 33 tests passed. These tests exercise validation, token/role boundaries, service workflows and duplicate effects; they do not prove real broker crash/recovery behavior.
- Inspected installed KafkaJS 2.2.4 consumer implementation and fetched its official configuration/consumption documentation. No application runtime, Docker state, AWS account, secret file or external repository was changed by this review. No acceptance/browser/ZIP execution is claimed here.

## Findings and required repairs

### 1. High: dependency restoration alone does not restart every consumer failure

Affected: NSI06 repair, NSI07 symptom/repair/recovery, and the qualification in NS41/NS42.

NSI06 says to repair the consumer dependency and allow existing durable retries. NSI07 frames poison data as repeated failures on one record. That misses a concrete failure path. In `backend/src/common/messaging.ts`, `consumer.run()` starts processing in the background; execution then enters the pause loop at line 116. A later CRASH listener only sets health false and logs. It does not leave that loop or recreate the consumer.

KafkaJS's installed `src/consumer/index.js` lines 267–300 tests whether an error is retriable before scheduling restart. A plain parsing, schema or database-handler error need not have `retriable: true`. Its consumer can therefore stop while the marketplace process continues to serve HTTP and wait. The [official restart policy](https://kafka.js.org/docs/configuration#restartonfailure) explicitly limits automatic restart to retriable failures; the [official versioned consumer implementation](https://github.com/tulios/kafkajs/blob/v2.2.4/src/consumer/index.js) supplies the code boundary. This conclusion is a source-based failure-path inference, not a fresh live-broker reproduction.

Required repair: explicitly separate publisher retries, KafkaJS retriable restart, and stopped consumer recovery. Check crash classification/restart status and actual consumer-group progress after dependency repair. Preserve logs and offsets; in the isolated local environment, restart the Notifications process when it remains stopped, retaining its group and original event identity. The existing beginner lab at `docs/nodejs-beginner/04-debugging-and-practice.md` already gives `docker compose restart notifications` after checking non-recovery. A poison record will still fail after restart: repair compatibility or design the explicitly absent durable quarantine/replay policy before any skip. Recovery must show group progress, the intended inbox effect, unchanged event identity and harmless replay; process health alone is insufficient. Do not claim the current source has a quarantine flow or universal automatic recovery.

### 2. Medium: extension lesson mappings imply teaching that those lessons do not contain

Affected: NS46 and NS47, and the meaning of the rendered lesson links.

NS46 links lessons 08/16, which do not contain a CORS/CSRF lesson section. NS47 links lesson 08, which teaches JWT signing/verification but not an OAuth/OpenID Connect or server-session flow. Those links are useful prerequisites, but a beginner following them cannot find the promised mechanism there. The answers correctly label these features absent; the navigation should be equally honest.

Required repair: label those existing links as prerequisites, explain the coverage boundary beside them, and provide a direct official worked-example link for the absent mechanism. Alternatively add a clearly labeled small extension section without changing existing lesson IDs. Do not pass a file-existence assertion as proof of exact topic mapping. For NS46, the CORS example alone does not demonstrate cookie-session CSRF defense; identify that boundary. For NS47, PKCE demonstrates authorization-code binding, not a complete OpenID Connect login, session or revocation system.

### 3. Low: wrong row name in the inquiry transition answer

Affected: NS34.

The answer says the provider's row is locked. `InquiriesService.respond()` locks `SELECT * FROM inquiries WHERE id=$1 FOR UPDATE`. Required repair: say **inquiry row**, then explain that its stored `provider_email` is compared with the actor before changing its status. This matters because service-owned database boundaries must remain understandable.

### 4. Medium learning usability: complete the acronym bridge in the integrated output

Most specialist terms have useful explanations, including JWT, SQL, SHA-256, TLS, CA and UUID. The section still uses API, IP, UTF-8 and SCRAM without an expansion adjacent to the relevant beginner explanation. Required repair: provide a visible linked glossary or expand at first use: Application Programming Interface, Internet Protocol, Unicode Transformation Format (8-bit), and Salted Challenge Response Authentication Mechanism. Keep protocol identifiers such as `HS256`/`SCRAM-SHA-512` recognizable and explain their role rather than merely expanding the letters. This can be solved centrally in the integrated companion; do not repeat long definitions in every card.

## Security, contract and failure-path assessment

The draft correctly distinguishes authentication, role and row ownership; shared-HMAC verifier compromise; readable token claims; current lack of revocation/federation; strict input versus erased TypeScript types; parameter values versus SQL identifiers; and TLS peer verification versus encryption alone. It does not suggest disabling verification or printing credentials. The throttle guidance correctly identifies process-local counters and proxy trust.

It correctly separates client retry keys, payload fingerprints, inquiry IDs, event IDs and offsets. The atomic inquiry/outbox commit and the two replay windows are explained without an exactly-once claim. The publisher's held transaction/client and bounded batch are acknowledged. Stale profile edits are correctly identified as absent optimistic concurrency. The uncertain-write incident preserves the original key/payload and includes changed-payload and cross-actor rejection checks.

The nine incidents include symptom, checks, repair and recovery fields. The consumer recovery branch above is the material exception to otherwise sensible diagnostic sequences. Existing tests and source invariants support many individual claims, but the report deliberately does not promote mock results to real PostgreSQL lock, broker recovery or cloud execution evidence.

## External example and reference-bar inspection

Fetched [Devinterview's Node interview repository](https://github.com/Devinterview-io/node-interview-questions) on the review date. Its question-led organization and short explanations provide the comparison bar; its broad runtime surface is not evidence about this marketplace. The service companion's strongest addition is concrete ownership, transaction and failure-window detail. The critic did not copy its answers or use it as a technical authority.

Verified current primary references for disputed or absent mechanisms:

- [KafkaJS consumption](https://kafka.js.org/docs/consuming) supports handler/offset separation; [retry configuration](https://kafka.js.org/docs/configuration#restartonfailure) establishes the limited restart policy.
- [Node-postgres transactions](https://node-postgres.com/features/transactions) requires one client for the transaction; this matches the current wrapper.
- [Nest outbox tutorial](https://docs.nestjs.com/reliability/outbox#retries-and-the-dead-letter-queue) actually includes persistent dead letters/admin requeue. NSI07 appropriately describes it as an external design with its own storage/version requirements, not installed marketplace behavior.
- [RxJS Observable guide](https://github.com/ReactiveX/rxjs/blob/master/apps/rxjs.dev/content/guide/observable.md) contains the 1/2/3 synchronous, delayed 4, completion example described in NS07.
- [RFC 9110 If-Match](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match) supports conditional updates and failed-precondition behavior. NS45's separate-server exercise remains a proposed practice design, not an executed marketplace test.
- [Nest CORS](https://docs.nestjs.com/security/cors) contains `enableCors` and configuration examples. [RFC 7636 Appendix B](https://www.rfc-editor.org/rfc/rfc7636.html#appendix-B) supplies the PKCE challenge vector used by NS47. Neither establishes a project identity-provider integration.

NS50–NS54 were read after their addition: they distinguish direct Zod/env/pg/JWT/contracts from absent pipes/interceptors, ConfigModule, ORM, Passport and Swagger/OpenAPI, with isolated external exercises. Their source excerpts also passed the independent provenance check. Full live link/fragment and rendered-example validation remains an integration check.

## Re-review gate

The builder should repair findings 1–4, record the largest gap and repair in `docs/reviews.md`, regenerate the integrated artifact, and preserve this round's failed finding. A separate critic should inspect the repaired actual output and managed ZIP. This report supplies no self-approval by a builder and no cloud/deployment verification.

## Independent service-section re-review — November 5, 2026

**Current verdict: accepted for the service learning section.** The independent critic reviewed the repaired JSON and actual generated `node-backend-services.md`, rather than accepting the builder's description. The original failed findings above remain preserved.

All four repairs are present:

1. NSI06/NSI07 now separate durable publisher retry from KafkaJS crash/restart behavior, identify a consumer left stopped while the outer loop sleeps, and require checking actual offset/insert progress. They specify controlled **local** process restart after cause repair with the same group, offsets and event identity. They explicitly preserve the poison-record/quarantine boundary and require recording manual recovery. NS41/NS42 now repeat the limitation where startup and instrumentation are explained. This resolves the largest gap without claiming a runtime repair or a newly executed broker drill.
2. NS46/NS47 visibly render `lesson_relation` explanations identifying existing lessons as prerequisites and the absent mechanisms as researched extensions. The external CORS exercise explicitly concerns CORS preflight/authorization behavior; the distinct CSRF reference remains available, and the text claims no implemented cookie-session defense. The PKCE example explicitly says it demonstrates code binding, not an identity provider.
3. NS34 correctly says **inquiry row**, matching `InquiriesService.respond()`.
4. The questionnaire's visible acronym table supplies API, IP, ID, UTF-8 and SCRAM alongside the existing security/protocol definitions. The service section links directly back to that questionnaire.

Repeated independent provenance checks: 63 items; current source-file hashes, literal symbols and excerpts all match; listed lesson files exist; zero failures. An additional parity check required every service item anchor, answer, incident field, worked example and explicit lesson-relation text to appear in the generated service Markdown, and every literal source excerpt to appear in the generated source-context artifact: zero failures. The 33 targeted tests recorded earlier remain the actual executed test result; they were not relabeled as integration recovery evidence or rerun without a runtime change.

Exact artifacts inspected for this re-review:

| Artifact under `docs/nodejs-aws-study-path/` | SHA-256 |
|---|---|
| `node-services-items.json` | `823f9ececb8c612f7467ec36dfcb8d14db6709c3771b9e2467b31b520c030d11` |
| `node-backend-services.md` | `f4754579d58ef50b0ec949c28c61a00c399c7547c304cf96d882bcfcc3956709` |
| `node-backend-questionnaire.md` | `41d789f669a6b2424e2c53a5f4f7888eb528f70564af11134e15269c94fcfb66` |
| `evidence/node-backend-source-context.md` | `4cdddc5d3769415b70e18aa121737b305d0b8b15a756c91638ae6d7c4c4cedf7` |

This verdict is limited to the repaired service section and its source/lesson/example explanations. The integrated artifact, link/fragment suite, package bytes/exclusions and publication state remain the separate integrated critic's responsibility. The critic changed only this evidence record, not builder content or application behavior.

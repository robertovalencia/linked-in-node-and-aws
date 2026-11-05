# Setup, testing, client boundaries, delivery and extensions

[Questionnaire and routes](node-backend-questionnaire.md) · [Acronym glossary](node-backend-questionnaire.md#acronyms-at-a-glance) · [Source excerpts](evidence/node-backend-source-context.md) · [Runtime lab](labs/node-runtime/README.md)

<a id="no01"></a>

### NO01 · Which Node version should I install for this project?

**Priority:** start now. **Implementation:** Current source.

Start with `node --version` and the package engines, rather than installing whichever version is newest. This backend declares `>=22 <25`; its Dockerfile pins a Node 22 image by digest. Use a patched, supported release inside that range and rerun checks when upgrading. Long-term support (LTS) describes maintenance policy, not proof that every dependency supports that version.

**Project:** [backend/package.json](evidence/node-backend-source-context.md#source-no01) · symbol: `"node":`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.npmjs.com · reference 1](https://docs.npmjs.com/cli/v11/configuring-npm/package-json) · [nodejs.org · reference 2](https://nodejs.org/en/about/previous-releases).

<a id="no02"></a>

### NO02 · What do package.json, a lockfile and npm ci each do?

**Priority:** start now. **Implementation:** Current source.

`package.json` declares scripts and version ranges; `package-lock.json` records the resolved dependency tree. `npm ci` installs from that agreement and fails on a manifest/lock mismatch instead of updating the lock. Root, backend and frontend are separate package scopes here: run `npm ci`, `npm --prefix backend ci`, and `npm --prefix frontend ci` from the repository root when all tools are needed.

**Project:** [package.json](evidence/node-backend-source-context.md#source-no02) · symbol: `"check":`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.npmjs.com · reference 1](https://docs.npmjs.com/cli/v11/commands/npm-ci) · [docs.npmjs.com · reference 2](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json).

<a id="no03"></a>

### NO03 · How do I start all four services locally?

**Priority:** start now. **Implementation:** Current source.

Install the declared Node version and Docker Desktop with Compose v2. From the repository root run `npm run setup`, then `npm run up`; open `http://localhost:8180`. Setup creates independent local credentials only if `.env` is absent. Compose starts PostgreSQL, Kafka, four service processes and nginx. `docker compose ps` should show their health; a successful image build alone does not establish readiness.

**Project:** [scripts/local.sh](evidence/node-backend-source-context.md#source-no03) · symbol: `up) docker compose`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/compose/how-tos/startup-order/).

<a id="no04"></a>

### NO04 · How can I run with hot reload and a debugger?

**Priority:** start now. **Implementation:** Current source.

Use `npm run down` before switching away from container APIs. Run `bash scripts/local.sh deps`, install backend/frontend dependencies, then `npm run dev`; open port 5183. The supervisor starts four APIs on 8181–8184 and Vite. Each service has its own compiled output and loopback inspector port (9229–9232). A debugger attaches to an inspector, while clients send requests to an HTTP port.

**Project:** [backend/scripts/dev.mjs](evidence/node-backend-source-context.md#source-no04) · symbol: `const outDir =`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [13 · testing and debugging](generated/13-testing-and-debugging.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/docs/latest-v22.x/api/inspector.html).

<a id="no05"></a>

### NO05 · Why can localhost work on my laptop but fail in a container?

**Priority:** start now. **Implementation:** Current source.

`localhost` means the process’s own network environment. A host process reaches PostgreSQL through `127.0.0.1:55432`; a Compose backend uses `postgres:5432`. Kafka bootstrap and advertised addresses must both match the client’s network. Local names and ports belong to Compose project `linked-in-node-local`; they are independent of AWS addresses, credentials and data.

**Project:** [compose.yaml](evidence/node-backend-source-context.md#source-no05) · symbol: `name: linked-in-node-local`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [04 · node http processes and streams](generated/04-node-http-processes-and-streams.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/compose/how-tos/networking/).

<a id="no06"></a>

### NO06 · What must configuration validation establish before listening?

**Priority:** start now. **Implementation:** Current source.

Reject missing or malformed settings at startup so requests never reach a half-configured service. `validateConfig` checks the service name, database settings, shared signing secret and capability-specific dependencies. Inquiries also requires a catalog URL. Check variable names and validation messages without printing `.env` or connection strings. Configuration being syntactically valid still does not prove a remote dependency is reachable.

**Project:** [backend/src/common/config.ts](evidence/node-backend-source-context.md#source-no06) · symbol: `export function validateConfig`.

**Lessons:** [05 · nestjs service wiring](generated/05-nestjs-service-wiring.md) · [14 · local runtime and containers](generated/14-local-runtime-and-containers.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.nestjs.com · reference 1](https://docs.nestjs.com/techniques/configuration).

<a id="no07"></a>

### NO07 · Why compile TypeScript before starting Node?

**Priority:** start now. **Implementation:** Current source.

`tsc` checks types and emits JavaScript; `node dist/main.js` executes that output. This project uses strict TypeScript and ECMAScript modules (ESM), with NodeNext resolution. The container copies migrations, seeds and certificates as runtime assets too. Passing compilation cannot prove those files were packaged or that environment settings are correct; test startup from the actual image.

**Project:** [backend/Dockerfile](evidence/node-backend-source-context.md#source-no07) · symbol: `COPY --chown=node:node migrations`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md) · [14 · local runtime and containers](generated/14-local-runtime-and-containers.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) · [docs.docker.com · reference 2](https://docs.docker.com/build/building/multi-stage/).

<a id="no08"></a>

### NO08 · What is shared when four services use the same Docker image?

**Priority:** start now. **Implementation:** Current source.

They share packaged code and dependencies, not one JavaScript heap or domain database. Each container selects one capability with `SERVICE` and receives its own database login. A shared PostgreSQL server or broker remains a shared failure risk. Container memory and CPU limits constrain resources; they do not make workloads highly available.

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-no08) · symbol: `const providers:`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).

<a id="no09"></a>

### NO09 · What does a mock prove compared with a real integration test?

**Priority:** start now. **Implementation:** Current source.

A mock supplies controlled dependency behavior; a spy records calls. A Jest test can prove that a denial branch avoids an insert against a fake database. It cannot prove PostgreSQL actually blocks a concurrent write or Kafka recovers after restart. Pair those tests with real dependency scenarios for durability, locking and replay. Choose tests by the failure they could catch.

**Project:** [backend/test/workflows.spec.ts](evidence/node-backend-source-context.md#source-no09) · symbol: `function database(`.

**Lessons:** [13 · testing and debugging](generated/13-testing-and-debugging.md) · [18 · interview drills and capstone](generated/18-interview-drills-and-capstone.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [jestjs.io · reference 1](https://jestjs.io/docs/mock-functions).

<a id="no10"></a>

### NO10 · How do I test a race without hoping it happens?

**Priority:** next. **Implementation:** Current source.

Control the schedule. In the stale-search test, keep the first promise unresolved, issue another search, resolve the newer response, then resolve the older response last. Assert the latest results stay visible. Vitest runs that hook test; a simulated browser document is useful for state behavior but does not reproduce real browser layout. Avoid arbitrary sleeps when explicit promise control can reproduce the failure.

**Project:** [frontend/src/hooks/useMarketplace.test.tsx](evidence/node-backend-source-context.md#source-no10) · symbol: `let resolveFirst`.

**Lessons:** [12 · react effects http and accessibility](generated/12-react-effects-http-and-accessibility.md) · [13 · testing and debugging](generated/13-testing-and-debugging.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [vitest.dev · reference 1](https://vitest.dev/guide/mocking.html) · [react.dev · reference 2](https://react.dev/reference/react/useEffect).

<a id="no11"></a>

### NO11 · What do type checking, linting, unit tests, build and acceptance each establish?

**Priority:** start now. **Implementation:** Current source.

Type checking rejects inconsistent static types; linting checks source rules; unit tests exercise selected behavior; a build proves artifacts can be emitted. Acceptance sends real application programming interface (API) requests through nginx to services and dependencies. None substitutes for the others. Run the root check/test/build scripts, then local acceptance against port 8180 when the stack is running; inspect failed cases rather than changing expected results to force green.

**Project:** [package.json](evidence/node-backend-source-context.md#source-no11) · symbol: `"acceptance":`.

**Lessons:** [13 · testing and debugging](generated/13-testing-and-debugging.md) · [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.typescriptlang.org · reference 1](https://www.typescriptlang.org/docs/handbook/2/basic-types.html) · [jestjs.io · reference 2](https://jestjs.io/docs/asynchronous).

<a id="no12"></a>

### NO12 · Why keep a real browser test after API tests pass?

**Priority:** next. **Implementation:** Current source.

An API response does not prove that a person can open a modal, use a keyboard or recover from an error. The browser smoke uses Playwright against the actual site; component tests provide faster focused feedback. Browser checks and screenshots cover selected journeys, not complete accessibility or all supported browsers. Record the tested URL, source revision and actual assertions.

**Project:** [scripts/browser-smoke.mjs](evidence/node-backend-source-context.md#source-no12) · symbol: `chromium`.

**Lessons:** [11 · react foundations and state](generated/11-react-foundations-and-state.md) · [12 · react effects http and accessibility](generated/12-react-effects-http-and-accessibility.md) · [13 · testing and debugging](generated/13-testing-and-debugging.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [playwright.dev · reference 1](https://playwright.dev/docs/library) · [playwright.dev · reference 2](https://playwright.dev/docs/test-assertions).

<a id="no13"></a>

### NO13 · Why does fetch need both catch and a response-status check?

**Priority:** start now. **Implementation:** Current source.

A fetch promise may fulfill for a server error such as 404 or 500; those are HTTP responses, not network failures. Check `res.ok` and translate error bodies safely. This API helper separately handles 204 so it does not parse an empty body as JavaScript Object Notation (JSON). A TypeScript return type cannot validate a server’s JSON at runtime.

**Project:** [frontend/src/services/http.ts](evidence/node-backend-source-context.md#source-no13) · symbol: `if (!res.ok)`.

**Lessons:** [12 · react effects http and accessibility](generated/12-react-effects-http-and-accessibility.md) · [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [fetch.spec.whatwg.org · reference 1](https://fetch.spec.whatwg.org/#dom-response-ok).

<a id="no14"></a>

### NO14 · Why use abort plus a stale-response guard?

**Priority:** next. **Implementation:** Current source.

When a search changes, abort the old request and prevent old continuations from updating current state. The hook checks the aborted signal before applying results, errors and loading state. Cleanup also aborts on unmount. Cancellation reduces wasted work; it does not reverse a server transaction that already committed. Retry uncertain writes with the original idempotency identity.

**Project:** [frontend/src/hooks/useMarketplace.ts](evidence/node-backend-source-context.md#source-no14) · symbol: `if (controller.signal.aborted) return;`.

**Lessons:** [12 · react effects http and accessibility](generated/12-react-effects-http-and-accessibility.md) · [18 · interview drills and capstone](generated/18-interview-drills-and-capstone.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [react.dev · reference 1](https://react.dev/reference/react/useEffect#fetching-data-with-effects).

<a id="no15"></a>

### NO15 · Which state belongs in React and which belongs in the backend?

**Priority:** next. **Implementation:** Current source.

Props pass data to a component; state triggers renders; a ref holds mutable coordination without triggering a render. Context shares authentication and hooks reuse effects; route components compose pages while services call APIs. Browser storage here remembers a token, comparison IDs and uncertain-write intent. Committed profiles, inquiries and notifications remain authoritative in service-owned databases; browser storage cannot replace them.

**Project:** [frontend/src/hooks/useInquiryAttempt.ts](evidence/node-backend-source-context.md#source-no15) · symbol: `const inFlight = useRef(false);`.

**Lessons:** [11 · react foundations and state](generated/11-react-foundations-and-state.md) · [12 · react effects http and accessibility](generated/12-react-effects-http-and-accessibility.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [react.dev · reference 1](https://react.dev/reference/react/useRef) · [react.dev · reference 2](https://react.dev/learn/sharing-state-between-components).

<a id="no16"></a>

### NO16 · Why preserve the original inquiry key after a network failure?

**Priority:** start now. **Implementation:** Current source.

A network failure may hide a successful commit. This hook saves the key and canonical payload in session storage before sending. Reuse that pair to reconcile or retry; a new key could create a second inquiry. The saved attempt is intent, not evidence of a committed record. A successful API response or durable read establishes the business result.

**Project:** [frontend/src/hooks/useInquiryAttempt.ts](evidence/node-backend-source-context.md#source-no16) · symbol: `sessionStorage.setItem(key, JSON.stringify(canonical));`.

**Lessons:** [12 · react effects http and accessibility](generated/12-react-effects-http-and-accessibility.md) · [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [fetch.spec.whatwg.org · reference 1](https://fetch.spec.whatwg.org/#concept-network-error).

<a id="no17"></a>

### NO17 · How do I explain a CI workflow without claiming deployment happened?

**Priority:** next. **Implementation:** Current source.

Continuous integration (CI) runs configured jobs on specific source. Here source, integration and Terraform jobs provide different evidence; deployment is separate. A workflow file describes intended execution, while an actual run and its artifacts establish results. Job dependencies determine ordering; steps inside a job run sequentially. Quote the observed run and commit before describing an external integration as verified.

**Project:** [.github/workflows/verify.yml](evidence/node-backend-source-context.md#source-no17) · symbol: `jobs:`.

**Lessons:** [15 · aws terraform and delivery](generated/15-aws-terraform-and-delivery.md) · [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.github.com · reference 1](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).

<a id="no18"></a>

### NO18 · What does a Sonar quality gate add, and what are its limits?

**Priority:** next. **Implementation:** Current source.

A quality gate applies configured conditions to submitted analysis, including the chosen coverage scope. Editor feedback is a different stage. The local Sonar helper waits for a real gate result; its existence is not a successful hosted scan. Review exclusions and missing reports. A passing gate still needs meaningful authorization and failure-path tests; no measured generated-code percentage follows from it.

**Project:** [scripts/sonar-ci.mjs](evidence/node-backend-source-context.md#source-no18) · symbol: `qualitygate`.

**Lessons:** [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.sonarsource.com · reference 1](https://docs.sonarsource.com/sonarqube-server/quality-standards-administration/managing-quality-gates/introduction-to-quality-gates).

<a id="no19"></a>

### NO19 · How should I review a dependency update or security advisory?

**Priority:** next. **Implementation:** Current source.

Inspect direct and transitive changes, the advisory’s affected path and the runtime/build distinction. This project audits production dependencies and has scoped overrides; an override needs compatibility tests and an exit condition. Dependabot proposes changes rather than approving them. Keep the lockfile consistent; an audit result is a dated advisory check, not proof that application authorization is safe.

**Project:** [backend/package.json](evidence/node-backend-source-context.md#source-no19) · symbol: `"overrides":`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.npmjs.com · reference 1](https://docs.npmjs.com/cli/v11/commands/npm-audit) · [docs.npmjs.com · reference 2](https://docs.npmjs.com/cli/v11/configuring-npm/package-json).

<a id="no20"></a>

### NO20 · How are short-lived release identity and application identity different?

**Priority:** next. **Implementation:** Current source.

OpenID Connect (OIDC) lets a CI job exchange an identity token for scoped cloud credentials after configured trust checks. That workload identity is separate from a user’s JSON Web Token (JWT) used by the marketplace. Bind release evidence to the exact source commit and image digest; a movable image tag alone cannot identify the bytes deployed. This lesson explains configured controls, not a new cloud release.

**Project:** [.github/workflows/deploy-dev.yml](evidence/node-backend-source-context.md#source-no20) · symbol: `id-token:`.

**Lessons:** [15 · aws terraform and delivery](generated/15-aws-terraform-and-delivery.md) · [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md) · [40 · aws release pipeline and oidc](generated/40-aws-release-pipeline-and-oidc.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.github.com · reference 1](https://docs.github.com/en/actions/concepts/security/openid-connect).

<a id="no21"></a>

### NO21 · Why serialize deployment and separate rollback from data recovery?

**Priority:** next. **Implementation:** Current source.

A host lock prevents two release scripts from replacing the same running stack at once. A release manifest binds source identity to image content. Switching to an older image does not undo a destructive schema change or restore deleted rows. Plan compatible migrations and test restoration separately. The preserved remote script illustrates a historical EC2 delivery path, not proof of the newer ECS application’s activation.

**Project:** [scripts/aws-remote-deploy.sh](evidence/node-backend-source-context.md#source-no21) · symbol: `flock -n 9`.

**Lessons:** [15 · aws terraform and delivery](generated/15-aws-terraform-and-delivery.md) · [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md) · [68 · disaster recovery and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/17/backup.html).

<a id="no22"></a>

### NO22 · What makes an AI-assisted backend change reviewable?

**Priority:** next. **Implementation:** Current source.

Write the expected behavior and negative cases, inspect the actual diff, update its requirement/specification and traceability, then run tests that could reject the change. An independent reviewer should challenge security, contracts and recovery. For a price filter, prove valid bounds and reject invalid input without changing existing defaults. Draft tickets and architecture decision records (ADRs) locally; only real external execution establishes a Jira or GitHub result.

**Project:** [CONTRACT.md](evidence/node-backend-source-context.md#source-no22) · symbol: `executable reference`.

**Lessons:** [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md) · [18 · interview drills and capstone](generated/18-interview-drills-and-capstone.md) · [19 · source and requirement coverage](generated/19-source-and-requirement-coverage.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.github.com · reference 1](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows).

<a id="no23"></a>

### NO23 · How would cache-aside preserve correct provider results?

**Priority:** extension. **Implementation:** Absent implementation.

Cache-aside checks a cache, reads the authoritative store on a miss, then caches the result. Include every response-changing input and tenant/authorization scope in keys. Choose a time to live (TTL) and invalidation rule, and avoid many simultaneous misses overwhelming PostgreSQL (a cache stampede). A cache hit can still be stale. This application has no shared cache; PostgreSQL remains authoritative. Negative caching briefly remembers a not-found result; it needs its own expiry and must not leak authorization decisions. Coordinate concurrent misses and add expiry jitter so many keys do not refill together.

**External worked example (not installed here):** Follow the official lazy-loading pseudocode: miss → database read → cache write. Trace two reads of the same public provider, then a profile edit and invalidation. Expect the first read to populate, the second to hit, and the edit to force fresh data; this is a design exercise, not installed cache behavior. [Official example](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html).

**Project:** [backend/src/catalog/catalog.service.ts](evidence/node-backend-source-context.md#source-no23) · symbol: `async search`.

**Lessons:** [58 · data caching and dynamodb design](generated/58-data-caching-and-dynamodb-design.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html).

<a id="no24"></a>

### NO24 · How would I model a DynamoDB query instead of replacing SQL with Scan?

**Priority:** extension. **Implementation:** Absent implementation.

Start from access patterns. To list a user’s notifications, a partition key selects the user and a sort key orders their records. Query requires one partition-key value; Scan examines a broader scope and is not a substitute for a missing access pattern. Secondary indexes add costs and read-consistency choices. No DynamoDB table exists here; a migration needs explicit backfill and ownership design. Denormalization stores access-pattern-specific copies instead of joining them at read time. Define how edits update those copies and how backfill catches up with concurrent writes before cutover.

**External worked example (not installed here):** Open the linked key-condition and pagination examples. Model PK=USER#u123 with notification timestamps in the sort key, query that partition, and continue with LastEvaluatedKey until absent. Check that a second user’s records are excluded; no query is executed here. [Official example](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html).

**Project:** [backend/src/notifications/notifications.service.ts](evidence/node-backend-source-context.md#source-no24) · symbol: `async list`.

**Lessons:** [58 · data caching and dynamodb design](generated/58-data-caching-and-dynamodb-design.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html) · [docs.aws.amazon.com · reference 3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql.html).

<a id="no25"></a>

### NO25 · Do many partition keys and TTL guarantee safe DynamoDB writes?

**Priority:** extension. **Implementation:** Absent implementation.

No. One busy key can dominate traffic even with many distinct keys. A conditional create can reject a repeated event identity; a transaction coordinates a defined set of operations. DynamoDB TTL is asynchronous cleanup, so code must reject expired authorization data itself. These are absent-feature design examples, not replacements for the current durable PostgreSQL deduplication.

**External worked example (not installed here):** Use the official conditional PutItem example with attribute_not_exists on the identity key. Predict first create succeeds and repeating it fails the condition. Separately assign 90 of 100 synthetic writes to one key to expose skew; an expiry timestamp must be checked before accepting an item. [Official example](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html).

**Project:** [backend/src/notifications/notifications.service.ts](evidence/node-backend-source-context.md#source-no25) · symbol: `ON CONFLICT`.

**Lessons:** [58 · data caching and dynamodb design](generated/58-data-caching-and-dynamodb-design.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html) · [docs.aws.amazon.com · reference 3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html).

<a id="no26"></a>

### NO26 · How do a queue, pub/sub, an event bus and a workflow differ?

**Priority:** extension. **Implementation:** Absent implementation.

A work queue distributes tasks; publish/subscribe (pub/sub) gives independent subscribers their own event paths; an event bus routes by rules; a workflow tracks steps and failure transitions. Kafka currently retains a partitioned log for replay. In Simple Queue Service (SQS), processing normally ends by deleting the message. A visibility timeout can expire after a committed effect, so retries still need durable idempotency and a monitored dead-letter queue (DLQ).

**External worked example (not installed here):** Follow the official SNS-to-SQS example conceptually with separate notification and analytics queues. Each subscriber keeps independent progress; two workers on a single queue compete for work. Check queue policies, routing filters and DLQ delivery permissions before any real implementation. No resources are created. [Official example](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html).

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-no26) · symbol: `class InquiryConsumer`.

**Lessons:** [60 · sqs sns eventbridge and workflows](generated/60-sqs-sns-eventbridge-and-workflows.md) · [28 · aws data and messaging decisions](generated/28-aws-data-and-messaging-decisions.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html) · [docs.aws.amazon.com · reference 3](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html).

<a id="no27"></a>

### NO27 · What do FIFO groups and partial batch failure actually guarantee?

**Priority:** extension. **Implementation:** Absent implementation.

First-in-first-out (FIFO) ordering is scoped to a message group; one busy group limits parallelism. Broker deduplication has a finite window and cannot make database effects exactly once. A Lambda SQS batch can repeat successful items when one fails. With ReportBatchItemFailures configured, report failed item IDs; for FIFO stop after failure and report unprocessed items too to preserve order.

**External worked example (not installed here):** Walk the official JavaScript batch handler with records a (success) and b (failure). Expect batchItemFailures to contain b, and enable the matching event-source response setting. This models a proposed SQS consumer; current KafkaJS code does not return that response. [Official example](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html).

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-no27) · symbol: `class InquiryConsumer`.

**Lessons:** [60 · sqs sns eventbridge and workflows](generated/60-sqs-sns-eventbridge-and-workflows.md) · [61 · lambda apigateway and serverless design](generated/61-lambda-apigateway-and-serverless-design.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html).

<a id="no28"></a>

### NO28 · How would an event-triggered Lambda differ from this listening Nest process?

**Priority:** extension. **Implementation:** Absent implementation.

An event handler receives an invocation payload and returns or throws; this Nest app creates a server and listens on a port. Validate the specific trigger’s event/response contract, initialize reusable clients outside repeated handler work and await required effects. Authentication, gateway invocation permission and business authorization are separate checks. An API Gateway design must choose required HTTP API or REST API features deliberately; no such resources exist here.

**External worked example (not installed here):** Read the official order-receipt Node handler, its exported name, input event and awaited storage call. Trace valid input to a receipt response, then missing input to failure. Contrast that entry point with bootstrap/app.listen; deployment and storage writes are not executed here. [Official example](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html).

**Project:** [backend/src/main.ts](evidence/node-backend-source-context.md#source-no28) · symbol: `await app.listen`.

**Lessons:** [61 · lambda apigateway and serverless design](generated/61-lambda-apigateway-and-serverless-design.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html).

<a id="no29"></a>

### NO29 · Why must Lambda retry and concurrency policy depend on its trigger?

**Priority:** extension. **Implementation:** Absent implementation.

A synchronous caller observes a failure and decides its retry policy; asynchronous invocation and polled queues have different retry mechanisms. More concurrent handlers can multiply downstream database connections, so cap concurrency and connection use against the database budget. Cold initialization adds work before an invocation. Do not assume one universal retry count, an always-warm process, or that Promise.all makes downstream capacity unlimited.

**External worked example (not installed here):** Use the official reserved-concurrency example to reason about ten concurrent handlers, each allowed two database connections: budget up to twenty plus other clients, not ten. Trace a retry from the selected invocation mode before choosing a cap. No Lambda configuration is changed. [Official example](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html).

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-no29) · symbol: `connectionTimeoutMillis`.

**Lessons:** [61 · lambda apigateway and serverless design](generated/61-lambda-apigateway-and-serverless-design.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html).

<a id="no30"></a>

### NO30 · What would useful tracing show across the inquiry and notification flow?

**Priority:** extension. **Implementation:** Absent implementation.

A trace links spans describing work across boundaries. Instrument the request, catalog lookup and transaction, then propagate context or links through the later outbox publish and Kafka consume. A trace ID is not a durable idempotency key. Bound attribute values and avoid secrets; sampling or exporter drops can hide work. There is no installed OpenTelemetry pipeline here, so shared log fields do not establish distributed tracing.

**External worked example (not installed here):** Follow the official local Node instrumentation walkthrough in a scratch project, start the instrumented app and request its test route. Confirm a span is exported to the selected console/exporter, then break exporter configuration and distinguish request success from telemetry delivery. This guide links the example; it does not claim that stack is installed. [Official example](https://opentelemetry.io/docs/languages/js/getting-started/nodejs/).

**Project:** [backend/src/common/messaging.ts](evidence/node-backend-source-context.md#source-no30) · symbol: `class OutboxPublisher`.

**Lessons:** [67 · otel tracing slos and incidents](generated/67-otel-tracing-slos-and-incidents.md) · [65 · cloudwatch agent logs metrics and alarms](generated/65-cloudwatch-agent-logs-metrics-and-alarms.md) · [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [opentelemetry.io · reference 1](https://opentelemetry.io/docs/languages/js/getting-started/nodejs/) · [opentelemetry.io · reference 2](https://opentelemetry.io/docs/concepts/context-propagation/).

<a id="no31"></a>

### NO31 · How do SLI, SLO and an error budget guide an incident?

**Priority:** extension. **Implementation:** Absent implementation.

A service-level indicator (SLI) measures a user outcome; a service-level objective (SLO) sets its target over a window. The error budget is the permitted unsuccessful fraction. A 99% target over 1,000 eligible requests permits ten failures. Measure accepted inquiries separately from notification delay. A health response is not that business measure. Investigate hypotheses using latency, errors, backlog and dependency saturation; record impact and recovery in a post-incident note. A service-level agreement (SLA) is an external commitment with consequences; an internal SLO is not automatically an SLA. Burn rate compares observed failures with the budget’s permitted rate over the same basis.

**External worked example (not installed here):** Use the official example SLO document structure: name the journey, eligible denominator, success rule, observation window and owner. For 1,000 eligible inquiries and 15 failures, the 99% target is missed by five. This is synthetic arithmetic, not a measured production SLO. [Official example](https://sre.google/workbook/implementing-slos/).

**Project:** [backend/src/common/health.ts](evidence/node-backend-source-context.md#source-no31) · symbol: `class HealthController`.

**Lessons:** [67 · otel tracing slos and incidents](generated/67-otel-tracing-slos-and-incidents.md) · [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [sre.google · reference 1](https://sre.google/workbook/implementing-slos/).

<a id="no32"></a>

### NO32 · How would a saga recover when several services cannot share one transaction?

**Priority:** extension. **Implementation:** Absent implementation.

Keep each local transaction inside its owning service. A saga coordinates steps and compensating business actions when later steps fail; compensation is not automatically a database rollback. Retry only a bounded, repeat-safe operation and preserve its stable identity. Step Functions can express retry and catch transitions, but repeated task effects still need idempotency. This project implements an outbox flow, not a saga engine.

**External worked example (not installed here):** Read the official Retry/Catch state examples. Sketch reserve → charge → confirm, then charge failure → release reservation, with a stable operation key and a separately recoverable failed compensation. Inspect the predicted execution states rather than treating retries as an atomic transaction. [Official example](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html).

**Project:** [backend/src/inquiries/inquiries.service.ts](evidence/node-backend-source-context.md#source-no32) · symbol: `class InquiriesService`.

**Lessons:** [60 · sqs sns eventbridge and workflows](generated/60-sqs-sns-eventbridge-and-workflows.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md) · [68 · disaster recovery and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html).

<a id="no33"></a>

### NO33 · What proves recovery after database failover or restoration?

**Priority:** next. **Implementation:** Current source.

A reconnected socket is only one layer. Re-establish connections with bounded retries, verify migrations and ownership, read expected rows and test a new write/event journey. A recovery point objective (RPO) limits data loss; a recovery time objective (RTO) limits time to recovery. Measure both with recorded timestamps and known records. Read replicas serve reads and are not an automatic writer failover or tested backup. Cold recovery rebuilds from retained data; warm recovery keeps some capacity ready; hot recovery keeps live capacity. Their costs and recovery times need a tested design, not a label.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-no33) · symbol: `readonly pool =`.

**Lessons:** [57 · rds postgresql backups and failover](generated/57-rds-postgresql-backups-and-failover.md) · [68 · disaster recovery and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/features/pooling) · [www.postgresql.org · reference 2](https://www.postgresql.org/docs/17/backup.html).

<a id="no34"></a>

### NO34 · What changes when a Node service scales to more process replicas?

**Priority:** next. **Implementation:** Current source.

Each process has its own heap, connection pool and in-memory throttle. More replicas can increase database connections or broker consumers without fixing the bottleneck. Keep durable data outside process memory, measure latency/errors/saturation and allow for startup delay. Rolling and blue-green releases both need schema compatibility; a healthy new process alone does not establish business acceptance. Rolling replacement mixes old and new replicas during rollout; blue-green keeps two environments and switches traffic. These deployment alternatives are design extensions, not activated release strategies in this guide.

**Project:** [compose.yaml](evidence/node-backend-source-context.md#source-no34) · symbol: `mem_limit:`.

**Lessons:** [31 · aws production design tradeoffs](generated/31-aws-production-design-tradeoffs.md) · [53 · ecs fargate tasks and services](generated/53-ecs-fargate-tasks-and-services.md) · [55 · ecs scaling and deployment strategies](generated/55-ecs-scaling-and-deployment-strategies.md) · [56 · ec2 autoscaling and eks comparison](generated/56-ec2-autoscaling-and-eks-comparison.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [nodejs.org · reference 1](https://nodejs.org/docs/latest-v22.x/api/cluster.html) · [docs.docker.com · reference 2](https://docs.docker.com/compose/how-tos/startup-order/).

<a id="no35"></a>

### NO35 · Is a persistent volume a backup, and how do object, file and block storage differ?

**Priority:** next. **Implementation:** Current source.

A persistent volume survives a container replacement but can retain corrupted or deleted data; a backup needs a separate recoverable copy. Object storage addresses objects by key, file storage offers shared filesystem paths, and block storage provides a disk-like device. Database backups need consistency, retention and a tested restore. This local stack uses volumes; it does not establish a tested object/file-storage migration.

**Project:** [compose.yaml](evidence/node-backend-source-context.md#source-no35) · symbol: `volumes:`.

**Lessons:** [62 · s3 ebs efs storage and recovery](generated/62-s3-ebs-efs-storage-and-recovery.md) · [68 · disaster recovery and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md) · [14 · local runtime and containers](generated/14-local-runtime-and-containers.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/engine/storage/volumes/) · [www.postgresql.org · reference 2](https://www.postgresql.org/docs/17/backup.html).

<a id="no36"></a>

### NO36 · Why is secret rotation a state transition instead of a text edit?

**Priority:** extension. **Implementation:** Absent implementation.

A secret is credential data; an encryption key controls cryptographic operations. Rotation must update the credential authority and clients coherently, including old/new overlap and recovery if only one side changes. Never put values in source, logs or infrastructure-state exports. These processes read settings at startup; editing a secret store does not hot-refresh their pools or signing keys. Automatic application rotation is absent. Encryption-key rotation is different from password rotation: older key material may still be needed to decrypt retained data. A disabled or deleted decryption key can make a backup unusable; restoration therefore depends on usable keys as well as data.

**External worked example (not installed here):** Follow the official rotation-method links and draw create → set → test → finish for a database credential. Predict the failure if clients receive a new password before the database accepts it, then define rollback/overlap and an authenticated test. No secret value is read and no rotation runs. [Official example](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html).

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-no36) · symbol: `export function databaseOptions`.

**Lessons:** [27 · aws s3 artifacts and secrets](generated/27-aws-s3-artifacts-and-secrets.md) · [54 · ecs networking identity and secrets](generated/54-ecs-networking-identity-and-secrets.md) · [63 · kms secrets and rotation](generated/63-kms-secrets-and-rotation.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) · [docs.aws.amazon.com · reference 3](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html).

<a id="no37"></a>

### NO37 · How do logs, metrics, traces and administrative audit differ?

**Priority:** next. **Implementation:** Current source.

Logs describe individual events, metrics summarize measurements, traces relate work across boundaries, and administrative audit records identity/action/outcome for management operations. Correlate them by time and appropriate IDs, but a cloud audit event does not prove an inquiry was persisted. Keep metric labels bounded (service/status rather than every user ID), protect retention/access and verify collection plus export instead of assuming console output reached a backend. Management events describe control-plane operations; data events describe operations such as S3 object reads. Default administrative event history is not complete data-access audit and does not record this app’s SQL business actions.

**Project:** [backend/src/common/database.ts](evidence/node-backend-source-context.md#source-no37) · symbol: `database_pool_error`.

**Lessons:** [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md) · [65 · cloudwatch agent logs metrics and alarms](generated/65-cloudwatch-agent-logs-metrics-and-alarms.md) · [66 · cloudtrail config and audit evidence](generated/66-cloudtrail-config-and-audit-evidence.md) · [67 · otel tracing slos and incidents](generated/67-otel-tracing-slos-and-incidents.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [opentelemetry.io · reference 1](https://opentelemetry.io/docs/concepts/signals/) · [prometheus.io · reference 2](https://prometheus.io/docs/practices/naming/) · [docs.aws.amazon.com · reference 3](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html).

<a id="no38"></a>

### NO38 · What would prove that a monitoring alarm works?

**Priority:** extension. **Implementation:** Absent implementation.

A metric alarm evaluates measurements over configured periods; missing data policy and the threshold affect its state. A resource declaration proves configuration, not signal arrival or responder delivery. Define an actionable user symptom, a query that narrows the failing layer and a controlled exercise with timestamps. This guide performs no new cloud alarm or delivery test.

**External worked example (not installed here):** Follow the official metric-alarm example conceptually: choose metric/statistic/period/evaluation count, then predict OK, ALARM and missing-data behavior for a short synthetic sequence. A later authorized test must record notification receipt and recovery; no alarm is created here. [Official example](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html).

**Project:** [backend/src/common/health.ts](evidence/node-backend-source-context.md#source-no38) · symbol: `class WorkerHealth`.

**Lessons:** [65 · cloudwatch agent logs metrics and alarms](generated/65-cloudwatch-agent-logs-metrics-and-alarms.md) · [29 · aws observability and incidents](generated/29-aws-observability-and-incidents.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html).

<a id="no39"></a>

### NO39 · Why can TypeScript tests fail on imports when the app builds?

**Priority:** next. **Implementation:** Current source.

The test runner and application use separate loading paths. This backend configures ts-jest for ECMAScript modules (ESM), treats TypeScript test files as ESM and maps relative .js imports back to source. Jest also uses Node’s experimental VM-module support here. A transformer emits executable code; it does not prove runtime input validity. Check package type, transform settings and source specifiers together before changing imports to satisfy one tool.

**Project:** [backend/package.json](evidence/node-backend-source-context.md#source-no39) · symbol: `"moduleNameMapper":`.

**Lessons:** [02 · typescript and modules](generated/02-typescript-and-modules.md) · [13 · testing and debugging](generated/13-testing-and-debugging.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [jestjs.io · reference 1](https://jestjs.io/docs/ecmascript-modules).

<a id="no40"></a>

### NO40 · Where do the demo users come from, and is that a sign-up API?

**Priority:** next. **Implementation:** Current source.

When SEED_DEMO equals true, Identity reads synthetic provider seed data and inserts demo accounts with salted password hashes; conflict handling preserves existing accounts. Catalog separately seeds provider profiles. This is controlled laboratory initialization, not public registration or shared identity tables. An existing database volume retains prior records. Disable demo seeding for a real environment and design registration separately; do not claim it exists from a seed hook.

**Project:** [backend/src/identity/identity.service.ts](evidence/node-backend-source-context.md#source-no40) · symbol: `if (process.env.SEED_DEMO !== 'true') return;`.

**Lessons:** [08 · identity jwt and security](generated/08-identity-jwt-and-security.md) · [14 · local runtime and containers](generated/14-local-runtime-and-containers.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/17/sql-insert.html).

<a id="noi01"></a>

### NOI01 · Install or build fails before any service starts

**Priority:** start now. **Implementation:** Current source.

Treat installation, compilation and startup as separate failing stages.

**Symptom:** npm ci rejects a lock mismatch, or tsc is missing in a nested package.

**Checks:** Run node --version and npm --version; confirm the current directory and the backend engine range. Check which package emitted the failure and whether its manifest and lock agree.

**Repair:** Use a supported runtime and install the affected package with its committed lock. If a dependency change was intended, regenerate and review that lock through the normal update process; preserve the original failure.

**Recovery verification:** Run that package’s ci, check and build successfully, then start it with validated configuration. A repaired install alone is not a running service.

**Project:** [backend/package.json](evidence/node-backend-source-context.md#source-noi01) · symbol: `"engines":`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [02 · typescript and modules](generated/02-typescript-and-modules.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.npmjs.com · reference 1](https://docs.npmjs.com/cli/v11/commands/npm-ci).

<a id="noi02"></a>

### NOI02 · Port in use or the browser reaches the wrong runtime

**Priority:** start now. **Implementation:** Current source.

Identify the actual listener before stopping anything.

**Symptom:** Startup reports EADDRINUSE, or new edits are invisible on port 8180.

**Checks:** Inspect docker compose ps and local listeners for 8180–8184/5183. Determine whether host dev and container APIs overlap; verify the URL and SERVICE process.

**Repair:** Stop this project’s container stack with npm run down before host dev, or stop its host supervisor before npm run up. Do not kill an unidentified process or reset data.

**Recovery verification:** Only the selected runtime owns its ports; its health probes pass and one visible source change appears through the matching frontend (5183 for dev).

**Project:** [scripts/dev.mjs](evidence/node-backend-source-context.md#source-noi02) · symbol: `PORT:String(8181+index)`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/reference/cli/docker/compose/ps/).

<a id="noi03"></a>

### NOI03 · Database refuses the service after changing environment settings

**Priority:** start now. **Implementation:** Current source.

An existing volume keeps its initialized users and passwords.

**Symptom:** An API fails authentication or connection while PostgreSQL itself is running.

**Checks:** Check service logs without exposing secrets, the host/container address, selected database/user and whether .env changed after volume initialization. Check dependency health before assuming a password problem.

**Repair:** Restore the matching local configuration or use the documented controlled credential-change procedure. Preserve existing data; a volume reset is deliberate data loss, not routine connection repair.

**Recovery verification:** Each capability connects only to its own database; readiness and an authenticated business read succeed. Verify unrelated service data remains intact.

**Project:** [scripts/setup-local.sh](evidence/node-backend-source-context.md#source-noi03) · symbol: `Keeping existing .env`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/compose/how-tos/networking/).

<a id="noi04"></a>

### NOI04 · A fresh build starts but cannot find migrations

**Priority:** start now. **Implementation:** Current source.

A compiled entry point can still be packaged without runtime assets.

**Symptom:** The process reports missing migration/seed files after the image build passed.

**Checks:** Read the startup error and final Docker build stage. Check the expected relative runtime path and whether migrations, seeds and certificates were copied; avoid printing secret files.

**Repair:** Repair the image’s runtime asset copies and rebuild the image, retaining non-root ownership and the intended working directory.

**Recovery verification:** Start the rebuilt image against isolated local dependencies, observe migration success, then verify ready health and a real database-backed API read.

**Project:** [backend/Dockerfile](evidence/node-backend-source-context.md#source-noi04) · symbol: `COPY --chown=node:node migrations`.

**Lessons:** [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [07 · postgresql and transactions](generated/07-postgresql-and-transactions.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/build/building/multi-stage/).

<a id="noi05"></a>

### NOI05 · The UI displays old results or reports failure after a committed write

**Priority:** start now. **Implementation:** Current source.

A late read and an uncertain write need different recovery actions.

**Symptom:** Search results revert to an older query, or an inquiry reports a network error despite appearing later.

**Checks:** Reproduce response order with controlled promises. For the inquiry, retain its original key/payload and query durable results; cancellation is not proof the server rolled back.

**Repair:** Abort obsolete reads and guard every state continuation. Reconcile/retry the uncertain inquiry with its existing identity rather than creating a new attempt.

**Recovery verification:** The stale-response regression keeps current results; retrying the same inquiry returns one durable inquiry and eventually one notification effect.

**Project:** [frontend/src/hooks/useMarketplace.ts](evidence/node-backend-source-context.md#source-noi05) · symbol: `if (controller.signal.aborted) return;`.

**Lessons:** [12 · react effects http and accessibility](generated/12-react-effects-http-and-accessibility.md) · [13 · testing and debugging](generated/13-testing-and-debugging.md) · [09 · inquiries idempotency and outbox](generated/09-inquiries-idempotency-and-outbox.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [react.dev · reference 1](https://react.dev/reference/react/useEffect#fetching-data-with-effects).

<a id="noi06"></a>

### NOI06 · Tests pass but the API route fails through nginx

**Priority:** start now. **Implementation:** Current source.

Check the complete routed path instead of treating unit success as deployment proof.

**Symptom:** A unit suite passes, but a browser request returns 404, 502 or an HTML body.

**Checks:** Record the exact method/path/status/content type. Check frontend proxy routing, target service readiness and matching source/image. A direct API port bypasses nginx and is a different path.

**Repair:** Repair the incorrect route, proxy target or unhealthy dependency at its owning layer. Preserve contract paths and management-route isolation.

**Recovery verification:** Replay the same request through http://localhost:8180, including a negative authorization case, then run the real acceptance suite and inspect its individual results.

**Project:** [scripts/acceptance.mjs](evidence/node-backend-source-context.md#source-noi06) · symbol: `const base=`.

**Lessons:** [13 · testing and debugging](generated/13-testing-and-debugging.md) · [14 · local runtime and containers](generated/14-local-runtime-and-containers.md) · [06 · http contracts and validation](generated/06-http-contracts-and-validation.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [docs.docker.com · reference 1](https://docs.docker.com/reference/cli/docker/compose/logs/).

<a id="noi07"></a>

### NOI07 · A cache or proposed queue consumer returns stale or repeated work

**Priority:** extension. **Implementation:** Absent implementation.

This scenario is an absent-feature rehearsal; the current project uses PostgreSQL/Kafka.

**Symptom:** A proposed cache serves the wrong tenant, or an SQS worker repeats a committed effect.

**Checks:** Compare cache key inputs and freshness with the authoritative store. For the queue, correlate stable event IDs, effect commits, visibility expiry and delete acknowledgments.

**Repair:** Correct scoped keys/invalidation and bound fallback load. Persist event identity atomically with effects; set realistic visibility/renewal and investigate DLQ causes before redrive.

**Recovery verification:** Replay a synthetic cross-tenant read and repeated event. Expect no leakage, freshness within the stated policy and one durable effect across retries; queue progress must resume.

**External worked example (not installed here):** Walk the official visibility-timeout timeline: receive, commit, crash before delete, receive again. The repeated delivery must leave one durable effect. For caching, compare two tenant-scoped keys; no SQS/cache system is installed or tested here. [Official example](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html).

**Project:** [backend/src/notifications/notifications.service.ts](evidence/node-backend-source-context.md#source-noi07) · symbol: `ON CONFLICT`.

**Lessons:** [58 · data caching and dynamodb design](generated/58-data-caching-and-dynamodb-design.md) · [60 · sqs sns eventbridge and workflows](generated/60-sqs-sns-eventbridge-and-workflows.md).

**Lesson relationship:** The linked lesson teaches the design concept; implementation remains absent. The external example is a separate worked extension.

**Official documentation:** [docs.aws.amazon.com · reference 1](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html) · [docs.aws.amazon.com · reference 2](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html).

<a id="noi08"></a>

### NOI08 · A rollback starts but expected records are missing

**Priority:** start now. **Implementation:** Current source.

Application rollback and data restoration are distinct recovery work.

**Symptom:** An older app starts, but deleted records or incompatible schema still break a journey.

**Checks:** Record source/image/schema versions, the destructive change and last usable backup point. Check whether the old app can read the current schema before changing traffic.

**Repair:** Choose a compatible forward repair or rehearsed restore to an isolated target. Verify data and credentials before a controlled cutover; do not overwrite the only recoverable copy.

**Recovery verification:** Check known rows and timestamps, new write/read/event behavior, ownership denials and measured data-loss/recovery intervals against RPO/RTO; image health alone is insufficient.

**Project:** [scripts/aws-remote-deploy.sh](evidence/node-backend-source-context.md#source-noi08) · symbol: `flock -n 9`.

**Lessons:** [68 · disaster recovery and resilience testing](generated/68-disaster-recovery-and-resilience-testing.md) · [57 · rds postgresql backups and failover](generated/57-rds-postgresql-backups-and-failover.md) · [17 · ai assisted engineering and toolchain](generated/17-ai-assisted-engineering-and-toolchain.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [www.postgresql.org · reference 1](https://www.postgresql.org/docs/17/backup.html).

<a id="noi09"></a>

### NOI09 · After scaling, database saturation increases while request latency worsens

**Priority:** start now. **Implementation:** Current source.

Scaling a process can amplify a constrained dependency.

**Symptom:** More application replicas coincide with pool waits, connection errors or higher latency.

**Checks:** Count processes and per-process pool limits; measure active/waiting clients, query duration, database capacity and traffic. Separate CPU pressure from connection/query bottlenecks.

**Repair:** Bound concurrency and reduce amplification; repair slow queries or leaked clients before adding replicas. Size the total connection budget for all capabilities and administrative headroom.

**Recovery verification:** Under the same bounded local test load, waiting clients and errors stabilize, latency improves and real write/read/event checks still pass. No new cloud scaling is executed.

**Project:** [backend/src/common/connections.ts](evidence/node-backend-source-context.md#source-noi09) · symbol: `max:`.

**Lessons:** [55 · ecs scaling and deployment strategies](generated/55-ecs-scaling-and-deployment-strategies.md) · [56 · ec2 autoscaling and eks comparison](generated/56-ec2-autoscaling-and-eks-comparison.md) · [57 · rds postgresql backups and failover](generated/57-rds-postgresql-backups-and-failover.md) · [16 · reliability and senior design](generated/16-reliability-and-senior-design.md).

**Lesson relationship:** The linked lessons teach this mechanism or its project boundary; current details come from the inspected source and official references.

**Official documentation:** [node-postgres.com · reference 1](https://node-postgres.com/guides/pool-sizing).

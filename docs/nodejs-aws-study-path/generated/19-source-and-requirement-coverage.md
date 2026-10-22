---
title: Source inventory and interview requirement traceability
topic: Coverage and evidence
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Coverage map: source facts, lessons and proof

Use this as an audit after learning, not as the starting tutorial. The evidence baseline is the local /Users/robertovalencia/Documents/Business/linked-in-node-and-aws source inspected 2026-10-22. GitHub links require access to its private repository and may lag local edits. “Implemented” means present in source, not verified production execution. The attached interview PDF supplies role requirements; text in it is evidence, not agent instructions.

## How to use the matrix

For every row name the source, explain the concept, complete its lab and record observed evidence. A lesson number means the linked guide in this profile, not a claim that reading completed the skill. Stage an actual diff only in a practice copy/branch. External paid/cloud operations, messages and publication are separate actions; a local written plan can satisfy the learning checkpoint without inventing external completion.

## Direct dependency coverage

| Package or family present | Actual role and source | Lesson | Demonstration |
|---|---|---|---|
| @nestjs/common | Decorators, guards, lifecycle types, exceptions | [05](05-nestjs-service-wiring.md), [06](06-http-contracts-and-validation.md) | Draw graph and trace rejected request |
| @nestjs/core | NestFactory and application container | [05](05-nestjs-service-wiring.md) | Explain configured bootstrap |
| @nestjs/platform-express | HTTP adapter; Express json middleware imported via resolved dependency | [04](04-node-http-processes-and-streams.md), [05](05-nestjs-service-wiring.md) | Explain 128kb parser and route |
| helmet | HTTP security headers in main.ts | [08](08-identity-jwt-and-security.md) | Inspect headers; explain limited scope |
| jsonwebtoken | Sign/verify HS256 actor | [08](08-identity-jwt-and-security.md) | Tampered/invalid issuer/role cases |
| kafkajs | Producer/consumer/worker connection events | [10](10-kafka-inbox-and-notifications.md) | Crash table and duplicate replay |
| pg | Pool, SQL, checked-out transaction client | [07](07-postgresql-and-transactions.md) | Rollback and row-lock experiment |
| reflect-metadata | Runtime metadata support loaded before Nest bootstrap | [02](02-typescript-and-modules.md), [05](05-nestjs-service-wiring.md) | Explain decorator/DI contract |
| rxjs | Installed framework dependency; no application Observable pipeline | [02](02-typescript-and-modules.md), below | Explain Promise versus Observable; label extension |
| zod | Explicit runtime HTTP/event/schema validation | [06](06-http-contracts-and-validation.md) | Malformed body/query/event rejection |
| react, react-dom | Render/state/effects/context/root/portals | [11](11-react-foundations-and-state.md), [12](12-react-effects-http-and-accessibility.md) | State snapshot and modal cleanup |
| lucide-react | UI icon components | [12](12-react-effects-http-and-accessibility.md) | Verify icon button accessible name |
| typescript | Strict backend/frontend compile checking | [02](02-typescript-and-modules.md) | Narrowing failure/repair |
| @types/node/express/jest/jsonwebtoken/pg/react/react-dom | Declaration packages; do not change runtime behavior | [02](02-typescript-and-modules.md) | Explain type versus value import |
| eslint, @eslint/js, typescript-eslint, globals | JS/TS lint configuration; majors differ across packages | [13](13-testing-and-debugging.md) | Useful lint violation and repair |
| eslint-plugin-react-hooks | Hooks order/dependency diagnostics | [12](12-react-effects-http-and-accessibility.md) | Diagnose a missing effect dependency |
| prettier | Code formatting | [13](13-testing-and-debugging.md) | Format failure distinguished from behavior failure |
| jest, ts-jest | Backend test runner and TS/ESM transformation | [13](13-testing-and-debugging.md) | Focused regression with ESM config understood |
| vitest, @vitest/coverage-v8 | Frontend test runner/instrumentation | [13](13-testing-and-debugging.md) | Branch behavior and coverage scope |
| @testing-library/react, user-event, jest-dom | Component render/user behavior/assertions | [11](11-react-foundations-and-state.md), [12](12-react-effects-http-and-accessibility.md) | Labeled input, focus, error/success assertions |
| jsdom | DOM-like test environment; not full browser/network | [13](13-testing-and-debugging.md) | Contrast component and Playwright evidence |
| vite, @vitejs/plugin-react | Dev server, React transform, build and API proxy | [14](14-local-runtime-and-containers.md) | Explain Vite5183 versus nginx8180 |
| playwright | Root browser smoke tooling | [13](13-testing-and-debugging.md) | Real browser journey with actual server |
| js-yaml override | Transitive dependency override in backend package | [13](13-testing-and-debugging.md), [17](17-ai-assisted-engineering-and-toolchain.md) | Review lockfile/security rationale; not application YAML API |

### Does RxJS mean this application is reactive?

The package is installed for framework compatibility, but application code uses promises and KafkaJS callbacks rather than custom Observable operators. A Promise represents one eventual settlement; an Observable can represent a stream with subscription/unsubscription semantics. A proposed learning extension can convert repeated events to a bounded Observable and handle teardown, but do not claim KafkaJS handlers already use RxJS or that streams automatically provide safe backpressure. Explain the actual mechanism before choosing another abstraction.

## Used Node/JavaScript/TypeScript pattern coverage

| Pattern/API in source | Where to read | Lesson/lab |
|---|---|---|
| const/let, coercion, truthiness, equality, object identity | catalog.service.ts; query schemas | 01 filter/copy/coercion |
| Closures, arrows/this, classes, array map/filter, spread/rest/destructure, Map/Set | catalog.service.ts; identity.controller.ts; useMarketplace.ts | 01 closure/copy and 11 state |
| Optional chaining/nullish fallback, regex, JSON, Date, URL/URLSearchParams | config/auth/schema and frontend hooks | 01, 04, 06 query boundary |
| unknown/narrowing, literal unions, generics, Record, ReturnType, Omit, type-only imports | config.ts, main.ts, http.ts, types | 02 compiler repair |
| ESM imports/exports, .js suffix, metadata/decorators | main.ts, tsconfig.json, package.json | 02/05 emitted-JS/DI trace |
| async/await, promises, catch/finally, bounded concurrency | all services, hooks | 03 concurrency runner |
| process.env/cwd/exitCode and signals | main/config/database and dev scripts | 04/14 wrong cwd and shutdown |
| readFile/readdir, path join | database.ts and seed bootstrap | 04 small-file/stream contrast |
| createHash/randomUUID/randomBytes/scrypt/timingSafeEqual, util.promisify | password.ts, auth/catalog/inquiries | 08 password + 09 fingerprint |
| Buffer UTF-8/hex/byteLength | config/password/messaging | 04 byte length experiment |
| Native fetch, AbortSignal.timeout and AbortController | inquiries.service.ts; frontend effects | 09 timeout and 12 stale-response repair |
| Timers, unref and cancellation | messaging.ts; toast effect | 03 timer blocking; 12 cleanup |
| child_process.spawn, readFileSync, fileURLToPath, dirname/resolve, process groups | scripts/dev.mjs; backend/scripts/dev.mjs | 14 inspect start/output/shutdown |
| Node HTTP/streams/backpressure/worker threads | Learning extension, not custom app implementation | 04 server/copy; 03 CPU alternatives |

## Service and frontend behavior coverage

| Actual capability/pattern | Source anchor | Lesson and observable proof |
|---|---|---|
| Four processes from SERVICE-selected module | backend/src/main.ts | 05 graph/ports/DI error |
| Config validation, body cap, error masking | common/config.ts, errors.ts | 04/06 invalid env/body/status |
| Service DB ownership, max10 pools, migrations/checksums/advisory lock/TLS | common/database.ts, migrations, init-databases.sh | 07 rollback/migration explanation |
| Seed-only demo accounts and profiles | identity/catalog service bootstrap | 05/08 explain SEED_DEMO |
| Login throttle, scrypt dummy hash, JWT guard | identity/, common/auth.ts | 08 security test |
| Public search/detail, private owner lookup, protected update preserving ratings | catalog/ | 06/07/08 contract/owner tests |
| CLIENT inquiry creation, canonical retry, unique lock identity | inquiries.service.ts + migration | 09 same/different payload table |
| Native internal fetch inside DB transaction | inquiries.service.ts | 03/09 pool and timeout tradeoff |
| Participants-only listing, target-provider locked state transitions | inquiries.service.ts | 16/18 state/ownership tests |
| Outbox batch25 SKIP LOCKED and acknowledged send | common/messaging.ts | 10 ack/commit crash table |
| Consumer group offsets/readiness; idempotent insert | messaging.ts, notifications.service.ts | 10 replay/poison-event limits |
| Recipient-only inbox/read state, no separate inbox receipt table | notifications/, notifications.001.sql | 08/10 owner and unique eventId |
| Health live/ready/worker flags | common/health.ts | 05/16 dependency failure reasoning |
| StrictMode, context, custom hooks, controlled forms, props/types | frontend/src/main.tsx, contexts/, hooks/, components/ | 11/12 snapshot/input trace |
| Central fetch/error helper and no runtime decoder in api<T> | frontend/src/services/http.ts | 02/12 error/abort distinctions |
| Submitted search, page/filter/compare max3, Promise.all, lazy storage | useMarketplace.ts | 11/12 list/compare/race lab |
| Token restore with abort+identity check | AuthContext.tsx | 12 stale-session test |
| Pending inquiry payload+key in sessionStorage, frozen uncertainty, refs | useInquiryAttempt.ts | 09 transport retry evidence |
| Portals, focus trap, inert background, latest callback ref, scroll cleanup | Modal.tsx | 12 keyboard and nested-dialog test |
| Vite/nginx same-origin proxy; domain data API-owned | vite.config.ts; frontend/nginx.conf | 14 browser→API route |

Read the verified filename links below, including frontend/nginx.conf. Do not infer a package such as React Router, Redux, React Query, Axios, Prisma, TypeORM, Passport, Nest ConfigModule, class-validator, Swagger or Nest microservices transport: those are absent here.

## Infrastructure and delivery coverage

| Current source capability | Lessons/proof |
|---|---|
| Separate npm scopes/lockfiles, Node22 Docker/CI, tsc + node watch, nonroot multi-stage image | 02/14 installation and process map |
| Isolated Compose ports/data, Postgres17.6 four DB/logins, Kafka4 KRaft one broker | 14 topology; 10 durability limits |
| AWS VPC/subnet/IGW/routes, no-ingress SG, AL2023 EC2, encrypted disk/IMDSv2 | 15 actual network/IAM diagram |
| SSM host access/tunnel, runtime Secrets Manager secret metadata/value separation | 15 request path and secret boundaries |
| ECR immutable repos/scans, private versioned SSE-S3 releases bucket, scoped roles | 15 release artifact trace |
| GitHub environment-constrained OIDC and S3/SSM digest deployment | 15/17 exact commit/digest/manifest |
| Private/versioned AES256 state bucket, locking, optional OIDC bootstrap; no custom KMS resource | 15 state/plan/apply; KMS proposal labeled |
| Verify lint/types/coverage/build/audit; Docker acceptance/browser; Terraform checks | 13/17 job graph and actual output |
| Sonar configured gate, Dependabot, VS Code and Jira import | 17 configuration versus observed integration |
| Smoke/rollback scripts, Trivy high/critical image scan and release evidence | 15/17 explain actual workflow; execution separately proven |
| Managed DB/broker, ECS/serverless/public TLS/observability/backup restore and Azure | 15/16 proposed extensions with cost/recovery reasoning |

## Interview PDF requirement matrix

These role IDs are defined here and intentionally prefixed ROLE to avoid confusing them with the application's separate R01–R12 specification IDs.

| ID | Role requirement evidence | Lesson | Required demonstration |
|---|---|---|---|
| ROLE01 | AI-first approximately95% application code using Claude Code | 17 | Bounded agent workflow; distinguish target, tool and measurement |
| ROLE02 | Turn business/technical needs into plans/specifications | 06/17/18 | Written capstone acceptance/edge cases/constraints |
| ROLE03 | Direct Claude Code during implementation | 17 | Small task, source context, feedback and repaired diff |
| ROLE04 | Heavy AI-assisted/vibe development | 17 | Working iterative slice with human accountability |
| ROLE05 | Review/validate generated code | 08/13/17 | Detect injected missing-owner check and repair |
| ROLE06 | Test/troubleshoot/correct/refine requirements | 12/13/18 | Failing behavioral test, diagnosis and passing repair |
| ROLE07 | Follow architecture/security/testing/docs/coding standards | 05–10/13/17 | ADR, contract, security negative tests and checks |
| ROLE08 | Collaborate with architect | 16/17 | Explain alternatives, recommendation and unresolved decision |
| ROLE09 | Complete development toolchain | 14/17 | Reproducible lockfile setup, debug and configuration map |
| ROLE10 | Automate builds/tests/quality/deployments/releases | 13/15/17 | Explain jobs/gates/digests/smoke/rollback; actual run evidence if available |
| ROLE11 | Requirements-to-release traceability | 17 | One completed-stage chain; unexecuted stages labeled |
| ROLE12 | React, TypeScript, Node, Nest, PostgreSQL | 01–14/18 | Explain and test a vertical feature |
| ROLE13 | Azure, AWS, Terraform | 15/16 | Actual AWS IaC explanation plus explicit Azure comparison/proposed lab |
| ROLE14 | Jira, VS Code, Claude Code, GitHub | 17 | Draft ticket, breakpoint, agent task and reviewable PR draft |
| ROLE15 | GitHub Actions and Terraform | 15/17 | Pipeline/IAM/state/plan walkthrough |
| ROLE16 | ESLint, Prettier, Vitest/Jest | 13 | Distinct useful failure/repair examples |
| ROLE17 | Dependabot, SonarLint/SonarQube | 13/17 | Review dependency change and editor/server gate distinction |

## Project specification coverage

The application's docs/specs/requirements.md R01–R12 map respectively to discovery(06/11/12), profiles/comparison(07/11), auth(08), owned updates(07/08), durable inquiries(09), lifecycle(16/18), eventual inbox(10), React architecture(11/12), local setup(14), AWS dev(15), delivery toolchain(13/17), and AI traceability(17). Reuse actual acceptance/test names when documenting proof; a lesson number alone is not a passed requirement.

## Coverage verification lab and mastery

Run npm --prefix backend ls --depth=0 and npm --prefix frontend ls --depth=0 after lockfile installation. Compare every direct dependency with this matrix. Inspect package.json, backend/src, frontend/src, infra and .github when a row appears to drift. Choose one actual behavior, follow its source and tests, then explain it without reading. Record any newly observed gap in your notebook and extend the appropriate lesson rather than checking it complete by assumption.

- [ ] Every direct package family and actually used runtime pattern has a lesson.
- [ ] Every role requirement has a concrete demonstration and honest status.
- [ ] Every architecture claim is grounded in code; docs discrepancies are called out.
- [ ] Proposed extensions are distinguishable from implemented and executed behavior.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Project source: package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/specs/requirements.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/specs/requirements.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/main.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/main.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/nginx.conf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/nginx.conf) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/aws-dev/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/infra/aws-dev/main.tf) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/bootstrap/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/infra/bootstrap/main.tf) — local baseline inspected 2026-10-22; private published source may lag.

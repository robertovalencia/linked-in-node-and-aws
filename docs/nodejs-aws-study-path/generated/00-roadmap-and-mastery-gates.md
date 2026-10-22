---
title: NodeJs/AWS: roadmap and mastery gates
topic: Roadmap
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# NodeJs/AWS: from first JavaScript to defensible engineering decisions

This path uses the actual service marketplace as your laboratory. You will learn to explain code before changing it, change it before optimizing it, and defend it with evidence before claiming mastery. Reading twenty guides does not establish seniority. Senior knowledge means independently making sound decisions under incomplete requirements, recognizing failure modes, and showing the results of your work.

## Start here

Know how to open a terminal, edit a text file, navigate folders, and use basic Git commands. No prior Node.js is assumed. If Java/Spring is familiar, use it as a bridge, but do lessons 01–04 rather than translating every Java habit literally. First read the repository README, CONTRACT.md, docs/architecture.md and docs/interview-topics/java-to-nestjs.md. The source is at /Users/robertovalencia/Documents/Business/linked-in-node-and-aws. All relative source paths in these guides start there.

Use the repository's declared Node range (backend engines: >=22 <25), lockfiles, and exact project scripts. That is the compatibility baseline, not a claim that the pinned versions are newest. Do not upgrade frameworks while learning the existing behavior.

Create a separate practice branch or copy. Run JavaScript scratch files with node path/to/file.mjs. Commands that start the application need Docker Desktop/Compose v2 and the repository's local setup. Never use a cloud deployment to test a JavaScript lesson.

## Twelve-week route and six-week compressed route

| Gate | Twelve-week pace | Six-week pace | Lessons | Observable exit evidence |
|---|---|---|---|---|
| A: language | Weeks 1–2 | Week 1 | 01–04 | Predict async output; implement validation without any; explain an HTTP request |
| B: backend | Weeks 3–4 | Week 2 | 05–08 | Draw dependency graph; trace login; demonstrate bad input and ownership rejection |
| C: distributed workflow | Weeks 5–6 | Week 3 | 09–10 | Reproduce retry safely; explain all commit/ack crash windows |
| D: UI | Weeks 7–8 | Week 4 | 11–12 | Trace a button to SQL; diagnose stale response; keyboard-test modal |
| E: engineering | Weeks 9–10 | Week 5 | 13–15, 17 | Meaningful tests, CI evidence, release/rollback plan and Terraform review |
| F: senior rehearsal | Weeks 11–12 | Week 6 | 16, 18–19 | Defend capstone, failures, tradeoffs and requirement-to-release evidence |

Pace is optional; gates are mandatory. With 60–90 minutes daily, spend 25 minutes reading, 30 building, 15 debugging and 10 explaining without notes. If you cannot pass a gate, repeat its lab with a changed input instead of rereading everything. Every seventh session is a retrieval and repair session.

## Interview in 48 hours

First learn the four capability names and one complete inquiry journey (05, 09, 10). Then explain JWT versus ownership (08), Node concurrency (03), React effects (12), and the real AWS topology (15). Rehearse the AI review workflow (17), then answer the drills in 18 aloud. Be candid: “I have Java/backend experience; I am building Node depth through this implementation. Here is the behavior I tested and the gap I would address next.” Do not present an exercise or prepared Terraform as production experience.

## Week 1 — JavaScript without framework shortcuts

- Complete [01 JavaScript](01-javascript-language-foundations.md), including the closure/copy output and non-mutating filter. Explain each line without notes.
- Evidence: runnable scratch file, predicted versus actual output, four edge-case assertions.

## Week 2 — TypeScript and the Node runtime

- Complete [02 TypeScript](02-typescript-and-modules.md), [03 async](03-node-runtime-and-async.md) and [04 HTTP](04-node-http-processes-and-streams.md).
- Evidence: a useful compiler error repaired, measured blocking experiment and two curl responses. Pass gate A.

## Week 3 — Service wiring and API contracts

- Complete [05 Nest wiring](05-nestjs-service-wiring.md) and [06 contracts](06-http-contracts-and-validation.md).
- Evidence: draw the four process/provider graphs and demonstrate invalid input and unauthenticated rejection.

## Week 4 — PostgreSQL and identity

- Complete [07 persistence](07-postgresql-and-transactions.md) and [08 security](08-identity-jwt-and-security.md).
- Evidence: rollback experiment, ownership rejection and an explained login trace. Pass gate B.

## Week 5 — Safe HTTP retry

- Complete [09 idempotency](09-inquiries-idempotency-and-outbox.md), including changed-payload and concurrent-request cases.
- Evidence: stable inquiry identity on replay; explain key, hash, lock and unique constraint separately.

## Week 6 — Events and failure recovery

- Complete [10 messaging](10-kafka-inbox-and-notifications.md). Draw every commit/ack crash window before the drill.
- Evidence: observed isolated-local recovery and reasoned limitations. Pass gate C.

## Week 7 — React render and state ownership

- Complete [11 React state](11-react-foundations-and-state.md), controlled fields, immutable updates and list identity.
- Evidence: functional-update experiment and source-grounded click/state/API trace.

## Week 8 — Effects and a complete UI-to-SQL feature

- Complete [12 effects/accessibility](12-react-effects-http-and-accessibility.md), including the proposed minRate vertical lab.
- Evidence: stale-response test, keyboard checklist and minimum-rate HTTP/UI cases. Pass gate D.

## Week 9 — Tests and reproducible engineering

- Complete [13 testing](13-testing-and-debugging.md) and [14 local runtime](14-local-runtime-and-containers.md).
- Evidence: deliberate meaningful regression then repair, source/unit/build output and correct local process map.

## Week 10 — Cloud preparation and AI delivery

- Complete [15 AWS/Terraform](15-aws-terraform-and-delivery.md) and [17 AI/toolchain](17-ai-assisted-engineering-and-toolchain.md).
- Evidence: actual infrastructure diagram, local IaC checks when available, bounded agent task and traceability record. Pass gate E.

## Week 11 — Design under failure

- Complete [16 reliability](16-reliability-and-senior-design.md) and draft the [18 capstone](18-interview-drills-and-capstone.md) contract/ADR.
- Evidence: dependency-slowdown diagnosis, failure timelines and defensible alternative with explicit assumptions.

## Week 12 — Capstone and interview defense

- Finish [18 interview/capstone](18-interview-drills-and-capstone.md), audit [19 coverage](19-source-and-requirement-coverage.md) and repeat weak drills with new inputs.
- Evidence: independent review, repaired biggest gap, executed test evidence and an honest mock interview. Pass gate F.

## Your evidence notebook

For each lesson record date, command/input, expected result, observed result, source location, and one remaining question. An unrun exercise stays “planned.” No check box starts checked. For code changes capture a failing test first when it verifies a real behavior, the repair, and the passing result. Record uncertainty rather than fabricate deployment, coverage, external integrations, or AI authorship percentages.

## First runnable checkpoint

From the repository root run these commands; mkdir -p creates the scratch folder if missing and keeps existing contents:

~~~bash
node --version
npm --version
mkdir -p work
node --input-type=module -e 'console.log(typeof process, typeof window, typeof Promise)'
~~~

Read package.json, backend/package.json and frontend/package.json. Expect object, undefined and function in Node. In a browser console, window exists. This difference explains why React browser code and backend runtime code need different environments despite sharing TypeScript. Save subsequent scratch examples under work/ as .mjs files and run node work/the-file-name.mjs.

## Mastery check

- [ ] I can identify the next gate and the evidence needed to pass it.
- [ ] I distinguish implementation evidence, interview requirements, and proposed extensions.
- [ ] I have run the language checkpoint and recorded what actually happened.
- [ ] I can explain why a short schedule cannot promise senior proficiency.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Node introduction](https://nodejs.org/en/learn/getting-started/introduction-to-nodejs) — accessed 2026-10-22.
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) — accessed 2026-10-22.
- [Project source: README.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/README.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: CONTRACT.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/CONTRACT.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/package.json](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/package.json) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/architecture.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/architecture.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/interview-topics/java-to-nestjs.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/interview-topics/java-to-nestjs.md) — local baseline inspected 2026-10-22; private published source may lag.

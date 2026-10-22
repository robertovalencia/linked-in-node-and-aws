---
title: Interview answers, practical drills and capstone
topic: Interview practice
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Rehearse explanations that survive follow-up questions

Prerequisites: gates A–E. Speak a concise answer, draw the relevant path, then prove it from code or a lab. A memorized answer that contradicts the implementation is a liability. Use the Java Interview Process question-bank style as a retrieval tool, but ground answers in Node behavior.

## Core questions with model answers

### What happens from clicking Send to seeing a notification?

The form creates/persists a logical attempt with key and payload. The API helper sends JWT and Idempotency-Key through the same-origin proxy. Nest's guard verifies identity. The service checks role/input, locks client/key in a DB transaction, replays or looks up catalog through bounded internal HTTP, then commits inquiry plus outbox. A worker publishes to Kafka; notifications validates and inserts with unique eventId. Provider inbox HTTP reads that persisted data. A success response proves the inquiry committed, not immediate delivery to every downstream channel.

### Why Node for this backend?

It fits asynchronous I/O and a shared TypeScript ecosystem with React. CPU-bound JavaScript can block the event loop, pools and native resources remain limited, and runtime validation is still necessary. Choose based on workload/team constraints rather than a universal faster-than-Java claim.

### How do four Nest services share one package?

SERVICE selects a controller/provider graph at startup; four processes use distinct configuration and database credentials. One image does not imply one process or shared domain tables.

### How do you avoid duplicate writes?

Stable client-scoped key, canonical payload hash, a cross-replica DB advisory lock and durable uniqueness. UI double-click guards help usability but cannot prove distributed correctness. HTTP retry identity and event identity solve related but distinct problems.

### Can Kafka make it exactly once?

This implementation has a DB/Kafka commit gap. It uses at-least-once delivery and idempotent notification effects. Broker transaction features do not automatically include PostgreSQL.

### How do you secure it?

Async password derivation, validated JWT algorithm/issuer/audience/claims, runtime Zod schemas, role/ownership checks, parameterized SQL, internal-key boundary and request limits exist. Shared HMAC verification, browser-readable tokens, per-process throttling and single-host dev topology need honest production discussion.

### What would you improve first?

Name a measured problem. For example, if catalog delay causes pool contention, measure transaction/pool waits and evaluate moving provider validation outside the lock with explicit replay and consistency semantics. Do not propose microservices or Redis simply to sound senior.

## Live coding drills

Implement a concurrency-limited promise runner (03), a discriminated-union result handler (02), a non-mutating provider filter (01), a controlled React form with errors (11), and a parameterized paginated SQL query (07). For each explain time/space cost, invalid input, cancellation/failure policy and one meaningful test. Prefer a clear working solution before optimizing.

## Capstone: status-change notification proposal

This is an extension, not existing behavior. Providers currently resolve inquiries; only inquiry-created events are implemented. Specify an event notifying the client after an accepted/declined decision. Define permission, transition, retry identity, schema/version, recipient privacy and duplicate-effect invariant. Keep the status update and new outbox record atomic. Decide message key, eventId generation on compatible replay, consumer validation/deduplication and UI refresh semantics. Explain whether using the existing notification service/group/topic is compatible or requires versioned changes.

Build the smallest vertical slice in a practice branch. First show a negative ownership test and duplicate-compatible-retry test. Then implement SQL/event/UI changes without cross-service database access. Run source checks/unit tests/build, real HTTP integration, duplicate event replay and the relevant browser journey. Supply an ADR and requirement-to-release evidence table; mark cloud execution planned unless performed separately. A separate critic should challenge contracts, data privacy, failure windows and actual outputs and identify the largest gap for repair.

## Mock interview scoring by evidence

| Area | Pass demonstration |
|---|---|
| Language/runtime | Predict output and explain concurrency without myths |
| Backend/security | Trace guard/role/ownership/SQL with a rejected attack |
| Distributed data | Enumerate every commit/ack gap and safe retry |
| React | Diagnose a stale response and explain focus cleanup |
| Infrastructure | Draw real EC2/SSM/ECR/S3 topology and a justified alternative |
| AI delivery | Show requirement, review gap, repair and executed evidence |

Fail a category if you cannot explain it without notes or if your claim outruns evidence. Repeat that exercise with changed inputs. Prepare two honest STAR stories from your own work; study labs are practice stories and must not be represented as production incidents.

- [ ] Give the complete journey in 90 seconds, then defend each boundary.
- [ ] Solve two drills without copying and diagnose a failure.
- [ ] Specify and validate capstone invariants across UI/HTTP/DB/events.
- [ ] Distinguish personal experience, current source and proposed design.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Project source: CONTRACT.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/CONTRACT.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/interview-demo.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/interview-demo.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/inquiries/inquiries.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/inquiries/inquiries.service.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: frontend/src/hooks/useInquiryAttempt.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/frontend/src/hooks/useInquiryAttempt.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/messaging.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/messaging.ts) — local baseline inspected 2026-10-22; private published source may lag.

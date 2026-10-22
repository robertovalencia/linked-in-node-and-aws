---
title: Reliability, architecture decisions and senior tradeoffs
topic: System design
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Senior answers connect choices to consequences

Prerequisites: backend, messaging and AWS gates. Begin with a business invariant: a client inquiry must be durable and target the intended provider, and only that provider may decide it. Architecture is how you preserve that invariant under load, faults and change. A named pattern without a failure explanation is not a design argument.

## Work one scenario end to end

The catalog becomes slow. Inquiries calls it inside a DB transaction with a five-second timeout. Connection slots and idempotency locks remain occupied during the wait. New inquiry latency rises, then the pool can queue. A worker's outbox operations also need database capacity. A timeout returns an availability error, while already committed prior attempts remain replayable. Blindly adding frontend retries may amplify the incident.

Measure request rate, latency distribution, error rate, transaction age, pool wait time, event-loop delay, oldest pending outbox age and consumer lag. The repository has console logs, health routes and worker readiness flags; a full metrics/tracing platform is an extension. Define a request/correlation ID propagation design without leaking actor emails or message text into broad logs. Useful traces would connect edge → inquiries → catalog → SQL and eventId → notifications across asynchronous delivery.

## Health and failure domains

Liveness answers whether the process can respond. Readiness asks whether it can currently perform its intended role according to chosen checks. The project ready route runs SELECT 1 and checks WorkerHealth. Identity/catalog do not need a broker check; inquiries/notifications track worker state. A recent group join is not proof that every message will validate and reach an inbox. Restarting a process for a downstream outage can worsen availability; route traffic and repair the dependency deliberately.

Four logical databases on one PostgreSQL host preserve ownership but share host failure. Four services on one EC2 host share compute failure. A single Kafka broker limits durable redundancy regardless of producer acknowledgements. Backups need restore tests, retention and ownership; Terraform remote state and S3 release manifests are not application-data backup.

## Executable tabletop and code lab

Write a one-page incident exercise with three timelines: Kafka unavailable after inquiry commit; catalog timeout before inquiry insert; notification DB insert committed before consumer offset commit. For each write client-visible behavior, durable rows, retry identity, expected health and recovery evidence. Compare against actual code in common/messaging.ts, inquiries.service.ts and health.ts. Then run the applicable isolated-local failure drill and record observed behavior. Mark any timing window you cannot deterministically reproduce as reasoned, not tested.

Add a practice-only test proving only a PENDING inquiry can transition to ACCEPTED/DECLINED, and a compatible repeat is safe while an incompatible resolved transition conflicts. Row locking prevents concurrent providers/actions from racing the same status, but role/ownership still matter. No status-changed event currently exists; a notification-on-decision feature needs a new contract/outbox path rather than a side-effect HTTP call after commit.

## Design decisions to defend

Modular monolith versus microservices: compare team ownership, independent scaling, release cadence, failure isolation and operational burden. Synchronous HTTP versus event: direct lookup gives immediate validation but couples latency/availability; events decouple timing but introduce consistency/versioning/replay concerns. JSONB versus normalized tables: weigh query/index constraints and flexible document shape. Shared JWT key versus asymmetric issuer: weigh simplicity and the ability of verifiers to mint tokens. Node versus Java CPU-heavy service: measure actual workload, then consider worker threads/jobs or an appropriate runtime.

Interview:

### How would you scale?

First name the measured bottleneck and correctness invariant. Horizontal replicas require aggregate pool sizing, durable idempotency, safe outbox concurrency, partition strategy and session/rate-limit redesign.

### What is your SLO?

A user-centered target such as successful inquiry submission latency or notification delay, with a defined measurement window and error budget; arbitrary 99.99% without evidence is not a plan.

- [ ] Explain three failure timelines and their durable states.
- [ ] Identify every single-host failure domain accurately.
- [ ] Write an ADR with constraints, alternatives, decision and revisit trigger.
- [ ] Propose metrics and a restore experiment without claiming them implemented.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [AWS Well-Architected reliability](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html) — accessed 2026-10-22.
- [Node profiling](https://nodejs.org/en/learn/getting-started/profiling) — accessed 2026-10-22.
- [Project source: backend/src/common/health.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/health.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/common/messaging.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/common/messaging.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: backend/src/inquiries/inquiries.service.ts](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/backend/src/inquiries/inquiries.service.ts) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/architecture.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/architecture.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/aws-dev.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/aws-dev.md) — local baseline inspected 2026-10-22; private published source may lag.

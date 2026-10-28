---
title: "OpenTelemetry, tracing, SLOs and incident response"
topic: "OpenTelemetry, tracing, SLOs and incident response"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 67 · OpenTelemetry, tracing, SLOs and incident response

**Prerequisites:** 65–66 and the inquiry/outbox/Kafka request flow.

[Previous lesson](66-cloudtrail-config-and-audit-evidence.md) · [Next lesson](68-disaster-recovery-and-resilience-testing.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. Define the user-visible promise first

An SLI is a measured indicator of service behavior. An SLO is a target for that indicator over a stated period. An SLA is an agreement with defined consequences and should not be casually claimed by an interview project. For this marketplace, successful inquiry creation and eventual notification delivery are different indicators with different failure windows.

A request can successfully commit an inquiry while its notification is delayed. Measuring only HTTP 200 responses hides that second part of the user experience. Define what counts as eligible work, success, delay and measurement source before choosing an SLO threshold. Targets in a learning exercise are assumptions, not measured production promises.

## 2. Model traces across synchronous and asynchronous work

A trace contains spans describing operations and their relationships. Propagated context helps connect work across HTTP boundaries. Messaging can require explicit context/link handling because processing happens later, may repeat and may be performed by different consumers. An inquiry ID, event ID and trace ID have different purposes. Deduplication must still rely on the correct durable business/event identities.

OpenTelemetry supplies common instrumentation/collection concepts. A collector pipeline can receive, process and export telemetry. A span created in a process is not proof an external backend received it. Export failures, sampling, queue limits and dropped events affect what an operator can see.

## 3. Choose useful, bounded attributes

Record service identity, operation, error class and appropriate correlation context. Avoid putting secret values, complete user messages or credentials into span attributes. Consider the privacy and cardinality implications of user IDs and raw URLs. Sampling reduces telemetry volume but can omit rare failure paths; a missing trace does not prove no request occurred.

For the Node project, instrumenting an HTTP handler without the outbox publisher and Kafka consumer would give an incomplete picture. Propose boundaries deliberately rather than claiming tracing exists because logs share an inquiry ID.

## 4. Use error budgets as a decision aid

An error budget expresses the permitted unsuccessful fraction implied by an SLO. A burn-rate view compares observed consumption with that allowance. Use a deterministic script for numerical examples and record the observation window. A short spike and sustained degradation need different operational responses. Alerting should identify actionable symptoms and a responder, not merely decorate a dashboard.

## 5. Investigate incidents with explicit hypotheses

Start with the reported user symptom, scope and first known failing boundary. Preserve timestamps and correlate logs, metrics, traces and administrative events. Check dependencies and recent changes, then choose a reversible action with a predicted result. After recovery, distinguish the immediate trigger, contributing conditions and a durable prevention or detection improvement.

## 6. State the current implementation honestly

The repository has local health, acceptance and resilience evidence, not a deployed OpenTelemetry collector or production SLO. The deployment owner can later cost telemetry ingestion, retention and sampling choices. This lesson remains useful now through a synthetic incident and instrumentation design.

## Example and current-project boundary

**Illustrative span map; not an installed tracing stack:**

```text
POST inquiry span
  -> Catalog lookup child span
  -> SQL transaction child span
  -> commit response
later: outbox publish span -> Kafka record context/link -> notification persist span
```

Compare the asynchronous boundary with the real [outbox and consumer code](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/backend/src/common/messaging.ts). A published record can replay even when the tracing system misses or samples its span.

## Practice with observable evidence

1. Define separate inquiry-creation and notification-delay SLIs, with explicit success/eligible-event rules.
2. Draw instrumentation points and identify where context crosses HTTP, SQL and Kafka.
3. Create a synthetic timeline for “HTTP success, delayed notification” and explain which signal distinguishes broker outage from consumer handler failure.
4. Write a brief post-incident note containing impact, evidence, hypotheses tested, recovery and a measurable follow-up.

**Expected evidence:** two precise SLI definitions, a span map and an incident explanation that respects replay and missing-telemetry limits.

## Recall and interview defense

### Is a trace ID an idempotency key?

No. Traces describe observed work; retry correctness depends on stable operation/event identity and durable enforcement.

### Why can an HTTP success SLO miss a user problem?

The accepted write and eventual effect are separate parts of the journey. Measure each at the correct durability and time boundary.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [OpenTelemetry concepts](https://opentelemetry.io/docs/concepts/)
- [OpenTelemetry context propagation](https://opentelemetry.io/docs/concepts/context-propagation/)
- [AWS reliability framework](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)

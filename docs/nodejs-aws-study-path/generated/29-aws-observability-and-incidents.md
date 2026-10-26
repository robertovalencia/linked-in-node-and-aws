---
title: "Observability: health, logs, metrics, audit and incidents"
topic: "Observability: health, logs, metrics, audit and incidents"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 29 · Observability: health, logs, metrics, audit and incidents

**Prerequisites:** 24–28 and basic HTTP status codes.

[Previous: 28](28-aws-data-and-messaging-decisions.md) · [Next: 30](30-aws-costs-and-cleanup.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Ask a different question of each signal

Logs describe events; metrics summarize values over time; traces connect work across boundaries; audit records describe administrative/API activity. A readiness response asks whether a process and its relevant dependencies can serve work now. A passing deployment acceptance suite asks whether specific business flows worked for that release. These are complementary observations, not interchangeable “green” statuses.

## 2. Inventory the actual implementation

Compose provides container health checks, restart policies and bounded JSON-file log rotation. The deployment runs readiness and full acceptance checks. The current infrastructure does not install a CloudWatch agent, create application dashboards/alarms, export traces or define a production SLO. Standard EC2 monitoring and AWS API audit should not be described as implemented application telemetry.

## 3. Choose useful proposed metrics

For a later operational extension, measure API error/latency rates, database pool waits, pending outbox age, consumer lag, failed handler attempts, host memory/disk and successful deployment time. A queue length alone can mislead: a healthy burst and one permanently stuck event may produce different urgency. Alert on user impact and sustained symptoms, and define who responds.

## 4. Follow an inquiry across boundaries

Start with request/inquiry/event identity; correlate creation, SQL commit, outbox publication and notification persistence. Do not log bearer tokens or whole secret-bearing configuration. A correlation ID aids investigation but does not prove every service exported a distributed trace. Distinguish actual available fields from a tracing proposal.

## 5. Diagnose a reported outage systematically

Reproduce the symptom, identify its scope, check the earliest failed boundary, preserve relevant timestamps and select the smallest reversible repair. For “no notification,” verify the inquiry row, outbox pending state, broker availability, consumer processing and unique recipient effect. Restarting every service immediately destroys useful evidence and may hide the actual mechanism.

## Walk the real project

[infra/aws-dev/compose.yaml · lines 8–15](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/compose.yaml#L8-L15)

```yaml
  healthcheck:
    test: [CMD, node, -e, "fetch('http://127.0.0.1:'+process.env.PORT+'/health/ready').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"]
    interval: 10s
    timeout: 5s
    retries: 18
    start_period: 30s
  depends_on:
    postgres: {condition: service_healthy}
```

[infra/aws-dev/compose.yaml · lines 17–17](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/compose.yaml#L17-L17)

```yaml
  logging: {driver: json-file, options: {max-size: 10m, max-file: '3'}}
```

Find the readiness URL in the Compose health check and compare with `scripts/aws-smoke.sh` and `scripts/acceptance.mjs`. Each check has a different depth. Read `docs/evidence/failure-drill.json` as historical local evidence; it is not a CloudWatch dashboard or an AWS deployment result.

## Practice step by step

1. Make a signal table: health, business acceptance, logs, proposed metrics, proposed traces and API audit.
2. Assign an example question to each signal and label actual versus proposed.
3. On an already-running local Node stack, inspect `docker compose ps` and bounded logs without printing secrets.
4. Write an incident timeline for an inquiry committed during broker outage and later notification recovery.

**Expected evidence:** A signal inventory and timestamped diagnostic timeline; no fictional alarms, traces or hosted-cloud results.

## Check your understanding

### If EC2 status checks pass, does login necessarily work?

No. Host health does not establish database availability, application readiness or correct credentials.

### Is CloudTrail a replacement for application logs?

No. Its audit purpose differs from application request, SQL and event-processing evidence.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [CloudWatch monitoring](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [CloudTrail auditing](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)

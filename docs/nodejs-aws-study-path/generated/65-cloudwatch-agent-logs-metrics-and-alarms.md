---
title: "CloudWatch agent, logs, metrics and alarms"
topic: "CloudWatch agent, logs, metrics and alarms"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 65 · CloudWatch agent, logs, metrics and alarms

**Prerequisites:** Host/task lifecycle, IAM roles and current log/readiness behavior.

[Previous lesson](64-waf-shield-and-security-detection.md) · [Next lesson](66-cloudtrail-config-and-audit-evidence.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. Inventory signals before installing an agent

Metrics summarize a measured quantity over time. Logs describe discrete events. Traces connect spans of work. An alarm evaluates a configured condition; a dashboard presents selected data. These are separate responsibilities. Begin with an operational question, such as whether the root disk is filling or inquiry delivery is delayed, then choose a signal capable of answering it.

The current Compose stack rotates local JSON-file container logs and runs health checks. It does not have a CloudWatch agent, centralized log groups, application dashboards or configured alarms. EC2 host monitoring is not a claim that in-guest memory, application events or Kafka lag are already collected.

## 2. Understand collection and delivery boundaries

The CloudWatch agent can collect host metrics and selected logs from supported hosts. It needs configuration, appropriate identity/permissions, network access and a running process. A configuration file on disk does not establish successful ingestion. A growing local log file also does not prove the agent can deliver it. Diagnose collection, buffering and delivery separately.

An ECS/Fargate proposal uses task logging and supported sidecar/telemetry patterns; there is no EC2 guest host under the same operational control. Do not paste an EC2 systemd-agent runbook into a Fargate task and assume host-memory collection works the same way. The deployment chat should choose a compatible observability design for its selected compute model.

## 3. Design metrics and labels deliberately

A namespace groups related metrics. Dimensions identify a time series. Useful examples include memory utilization, disk utilization, HTTP error ratio, database pool waits and oldest pending outbox age. Percentiles and averages answer different questions: an average can hide slow tail requests. Define units and aggregation periods, and avoid treating a counter as an instantaneous rate without calculating the interval.

High-cardinality dimensions such as individual request IDs or unbounded user IDs can create a large number of series. Keep correlation IDs in logs/traces where appropriate instead of using them as every metric’s dimension. The deployment owner must account for ingestion, retention, queries and metric volume when estimating cost.

## 4. Read an alarm as an evaluation rule

A CloudWatch metric alarm needs a metric/expression, statistic, period, threshold, comparison and evaluation window. For this metric-alarm example, M out of N evaluation determines how many points must breach. Missing data is not equivalent to a measured zero. A missing heartbeat can mean failed collection, while absent error samples may mean no events; choose a missing-data policy that matches the signal. Always test the notification path rather than assuming an ALARM state reached a human.

## 5. Give logs a lifecycle and a query

Choose structured fields, timestamp behavior, retention and access restrictions. Redact secrets before writing the event. A short log query should filter the correct service and time range, then summarize a relevant symptom. Do not enable every log source indefinitely simply because storage initially appears cheap. Logs can contain personal data and operational details, so retention and reader permissions belong to the design.

## 6. Verify operation after a proposed deployment

Future acceptance should distinguish agent running, metric visible, logs ingested, alarm condition evaluated and notification received. These are not interchangeable green checks. The existing portfolio’s readiness and 48 API checks remain useful, but do not substitute for telemetry delivery tests.

## Example and current-project boundary

**Illustrative agent configuration only; not deployed:**

```json
{
  "metrics": {
    "namespace": "Marketplace/Lab",
    "metrics_collected": {
      "mem": {"measurement": ["mem_used_percent"]},
      "disk": {"measurement": ["used_percent"], "resources": ["/"]}
    }
  }
}
```

This fragment selects measurements. It does not install an agent, grant an AWS role, create an alarm or show that any metric exists. The [actual AWS Compose file](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/compose.yaml) is the baseline for local logging and health checks.

## Practice with observable evidence

1. Pick three questions: disk exhaustion, API latency and delayed notification delivery. Specify one measurable signal for each.
2. Write a signal contract containing unit, dimensions, aggregation, collection interval and missing-data interpretation.
3. Prepare a synthetic table of five measurements and manually classify which windows would satisfy your chosen M-of-N alarm rule. Verify calculations with a small local script.
4. Draft a validation checklist separating collection, delivery, evaluation and notification. No AWS configuration is created by this exercise.

**Expected evidence:** three signal contracts, an evaluated synthetic window and an explicit future ingestion/notification acceptance test.

## Recall and interview defense

### Why does “agent running” not mean monitoring works?

The collector can be alive while configuration, permissions or connectivity prevent delivery. Verify actual signal ingestion and its timestamps.

### Should missing data always count as healthy?

No. Interpret it according to the metric’s contract. A missing heartbeat and an absent error counter do not mean the same thing.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)
- [CloudWatch alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html)
- [Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)


## Recognize the console screen

Use the [AWS visual study guide](../visuals/README.md) to identify the console fields and connect them to source. Official AWS examples demonstrate concepts and are not screenshots of this project’s deployment.

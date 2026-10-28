---
title: "CloudTrail, Config and audit evidence"
topic: "CloudTrail, Config and audit evidence"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 66 · CloudTrail, Config and audit evidence

**Prerequisites:** IAM authorization, resource identity and telemetry vocabulary.

[Previous lesson](65-cloudwatch-agent-logs-metrics-and-alarms.md) · [Next lesson](67-otel-tracing-slos-and-incidents.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. Ask separate audit questions

“Who called a control-plane API?” differs from “What configuration did the resource have?” and “Did a customer request succeed?” CloudTrail, Config and application telemetry serve these different questions. Correlation can build a useful timeline, but none should be presented as a universal transcript of the entire system.

A CloudTrail event describes an API-related activity with identity/time/context fields. An AWS Config record describes supported resource configuration and relationships over time; rule evaluations compare configurations to a chosen policy. Application logs describe business requests or background work. A compliance evaluation does not prove a user journey worked.

## 2. Distinguish management and data events

Management activity covers operations on AWS resources. Data events address supported activity on or within resources, such as selected object access, and need deliberate selection. Do not assume that a default control-plane history includes every S3 object read, all database queries or all container commands. A durable trail/event-store design also differs from merely viewing recent event history in a console.

The current Terraform source does not create an organization-wide audit pipeline or Config recorder/rules. It is incorrect to say these features are enabled because AWS offers them. The deployment owner must establish what exists in the actual account and how long it is retained before adding anything.

## 3. Read identity and outcome carefully

For an event, identify account, region, event source/name, principal/session context, event time and any error. Assumed-role session information needs interpretation: a session can show a role without proving which application-level end user caused the action. Correlate deployment command IDs and source SHA where available. Avoid treating a local operator nickname or an unverified header as authoritative identity.

An AccessDenied event is a failed authorization attempt, not a successful change. An accepted asynchronous API operation is not necessarily completed resource provisioning. Check subsequent resource state or operation status rather than inferring success from a single request record.

## 4. Protect the audit system itself

Restrict writers/readers, define retention, protect encryption keys, and decide which account owns centralized logs in a multi-account design. Tamper resistance and integrity evidence have prerequisites; a versioned bucket alone does not establish immutable compliance retention. An audit store can also contain sensitive identifiers and request metadata. Define who may inspect detailed records and what is safe to share in an interview screenshot.

## 5. Trace a deployment as evidence, not a narrative

A useful chain connects reviewed source → verification run → exact image digest → manifest → authorized SSM invocation → completed command output → acceptance report. The repository already contains parts of that operational evidence contract. Cloud audit would add administrative context, not replace the acceptance report. Record actual gaps rather than filling them with plausible events.

## 6. Define future coverage before estimating cost

List regions/accounts, event categories, selected data resources, supported Config resource types, evaluation frequency, retention and archive requirements. Those quantities can materially affect the deployment chat’s cost comparison. This lesson teaches that inventory; it does not run a recorder, enable a trail or obtain account logs.

## Example and current-project boundary

**New synthetic audit exercise:**

```json
{
  "eventSource": "ssm.amazonaws.com",
  "eventName": "SendCommand",
  "eventTime": "2026-10-27T12:00:00Z",
  "userIdentity": {"type": "AssumedRole"},
  "requestParameters": {"documentName": "AWS-RunShellScript"}
}
```

This invented teaching record omits identifiers and response details. It supports discussion of an attempted SSM operation; it does not prove the remote script ran or all 48 API checks passed. Compare with the real [deployment evidence checks](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/scripts/aws-deploy.sh).

## Practice with observable evidence

1. Make a table matching administrative change, object read, SG configuration history and failed login to the signal that could answer it.
2. Write a synthetic deployment timeline with separate attempted, accepted, completed and verified stages.
3. List missing fields that prevent attribution or outcome conclusions from the sample record.
4. Define a proposed audit coverage/retention inventory to hand to the deployment owner, without requesting any live data.

**Expected evidence:** a correctly scoped signal table and a timeline that never equates API acceptance with business success.

## Recall and interview defense

### Is Config compliance equivalent to security or availability?

No. A rule evaluates a selected condition for supported resource configuration. It does not prove every security invariant, current exploitation status or business availability.

### Does an SSM SendCommand record prove application deployment succeeded?

No. Follow the specific invocation to completion and inspect the corresponding acceptance evidence.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [CloudTrail management events](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html)
- [CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)
- [AWS Config](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)

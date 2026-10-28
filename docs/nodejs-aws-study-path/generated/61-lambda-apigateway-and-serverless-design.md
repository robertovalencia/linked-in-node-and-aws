---
title: "Lambda, API Gateway, and serverless application design"
topic: "Lambda, API Gateway, and serverless application design"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 61 · Lambda, API Gateway, and serverless application design

**Prerequisites:** 46–49 and 60; HTTP requests and asynchronous processing.

[Previous: 60](60-sqs-sns-eventbridge-and-workflows.md) · [Next: 62](62-s3-ebs-efs-storage-and-recovery.md) · [Study path](../README.md)

**Implementation boundary:** The current application runs long-lived NestJS processes in containers. Lambda and API Gateway are not declared; this lesson explores a separate handler-based design rather than claim a serverless migration.

For conventional event-driven use, AWS Lambda runs a handler in response to an invocation and manages its execution infrastructure. An execution role authorizes the function’s AWS calls. API Gateway provides an HTTP API front door with routing and authorization features. “Serverless” changes operational responsibilities; it does not remove concurrency limits, downstream capacity, data modeling, authentication, or incident response. Current Lambda includes multiple compute models, so identify the chosen invocation model instead of treating every new capability as the classic event-handler contract.

## 1. Choose a handler boundary and invocation contract

A short event transformation or bounded API operation can fit an event-function handler. A long-lived Node HTTP server, untrusted session execution, and a durable multi-step workflow have different lifecycle requirements and may call for different supported compute models. Start with trigger, payload, duration, state, and response expectations. Do not put every existing NestJS process into Lambda merely because the code is JavaScript. A migration needs an adapter and behavior analysis, not a change of product label.

## 2. Separate HTTP API features from REST API features

API Gateway HTTP APIs and REST APIs are distinct products with different feature sets. For a handler-backed API, HTTP API can suit simpler routing and JWT authorization; REST API may be needed for features such as usage plans, per-client throttling, request validation, or its WAF integration. Verify the current matrix against requirements. This is a feature comparison, not a cost recommendation. An API key identifies a client for supported management features and is not a substitute for user authentication.

## 3. Define authentication, integration permission, and authorization

The gateway may validate an identity or invoke an authorizer, but business ownership checks still belong in the application. API Gateway also needs permission to invoke the intended Lambda target; that resource-based permission is distinct from the function execution role. Limit routes and origins deliberately. CORS controls browser behavior, not whether a non-browser attacker can call an endpoint. Keep request validation, authentication, IAM integration permissions, and business authorization as separately reviewable decisions.

## 4. Model concurrency and downstream protection

Each concurrent invocation can consume a database connection, call a partner, or publish an event. Reserved concurrency can bound a function’s concurrent executions, while other controls may limit event-source concurrency. Initialization and connection reuse affect latency, but no invocation may rely on process memory surviving indefinitely. VPC-attached functions need the intended routes and endpoints; putting a function in a public subnet does not automatically supply public internet access. Protect downstream systems before raising concurrency.

## 5. Specify retry and error behavior by trigger

A synchronous caller handles its own response and retry policy; asynchronous delivery and event source mappings have different retry semantics. For SQS, partial-batch response behavior requires integration configuration as well as correct code. Validate the HTTP proxy response shape for the chosen payload format; a malformed result can become a gateway error even when the handler ran. Use structured logs, correlation IDs, and deadlines, while excluding tokens, secret values, and unnecessary personal data.

## Source or illustrative example

**New illustrative local handler:** return an explicit proxy-style JSON response for one documentation-only health request. This is not an AWS deployment, a complete authentication flow, or an adapter for the existing application. The [actual architecture](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/docs/architecture.md) remains four long-lived capability processes with their own business and database boundaries.

## Safe exercise

Run a local handler contract check:

```sh
node --input-type=module <<'JS'
const handler = async event => ({statusCode:200,
  headers:{'content-type':'application/json'},
  body:JSON.stringify({request:event.requestContext.requestId, ok:true})});
const response = await handler({requestContext:{requestId:'local-study'}});
if (typeof response.body !== 'string') throw Error('body must be encoded');
console.log(response.statusCode, JSON.parse(response.body).ok);
JS
```

Expected outcome: `200 true`. This checks one chosen response shape locally, not API Gateway wiring. Add a failure response and decide which caller may safely retry. Explain why the response contract and idempotent business behavior require separate checks.

## Failure diagnosis

A gateway 502 can result from an integration response mismatch; inspect the exact payload contract before diagnosing a network outage. A 401/403 may come from an authorizer, invocation policy, or business layer, so identify the rejecting component. Timeouts can involve cold initialization, DNS, VPC egress, database waits, or an unbounded partner call. Rising throttles with a healthy function can mean concurrency controls are doing their job; compare the workload contract and downstream capacity before changing them.

## Recall and answers

### Does CORS authenticate an API caller?

No. It constrains browser cross-origin behavior and does not replace server-side authorization.

### Which role authorizes function code to call S3?

The Lambda execution role, subject to applicable resource policies and other authorization layers.

## Mastery check

Produce a trigger/retry matrix, an HTTP feature choice, and a concurrency-to-database risk explanation. Distinguish gateway invocation permission from execution-role permission. Show the local handler output and clearly state that no Lambda function or API has been provisioned or verified.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [Lambda overview and compute models](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [API Gateway HTTP versus REST APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html)
- [Lambda SQS error handling](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html)

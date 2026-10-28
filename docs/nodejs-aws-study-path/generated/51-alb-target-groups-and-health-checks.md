---
title: "ALB listeners, target groups, and health checks"
topic: "ALB listeners, target groups, and health checks"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 51 · ALB listeners, target groups, and health checks

**Prerequisites:** 48 and 50; request routing and TLS.

[Previous: 50](50-dns-route53-acm-and-tls.md) · [Next: 52](52-cloudfront-s3-origins-and-caching.md) · [Study path](../README.md)

**Implementation boundary:** Application Load Balancers and target groups are absent from the current development root. This is a proposed production-entry design; it does not modify the current SSM-only access model.

An Application Load Balancer (ALB) routes HTTP and HTTPS requests at the application layer. A listener accepts connections on a protocol and port. Listener rules select actions such as forwarding or redirecting. A target group defines the backend targets, protocol, port, and health checks. Health checks observe a narrow readiness signal; they are not a full business acceptance suite and do not establish that every dependency or user journey works.

## 1. Start with listener behavior and rule precedence

Define the intended HTTPS listener, certificate, and HTTP-to-HTTPS redirect where appropriate. Listener rules can use host and path conditions; priorities determine which applicable rule wins. Specify a safe default action for requests that match nothing. For the project’s multiple capabilities, write an explicit route table so a private internal endpoint is not accidentally exposed by a broad path rule. The existing nginx routing is evidence of application boundaries, not evidence of ALB configuration.

## 2. Choose targets that match the runtime

An instance target references an instance; an IP target references addresses. Fargate tasks using awsvpc networking need the appropriate IP target arrangement. Target registration and target-group attachment are separate from creating a listener. Define the actual listening port and protocol of each service rather than copying a frontend port into every target group. Distribute suitable targets across enabled zones and account for the consequences of having no healthy target in a zone.

## 3. Make health checks useful and bounded

Choose a path that answers without browser credentials and indicates whether the target can accept intended work. Avoid an expensive check that repeatedly amplifies a database outage. Set expectations for interval, timeout, success matcher, and startup grace based on measured behavior when evidence exists. Deep business acceptance belongs in a separate suite. If every registered target is unhealthy, ALB can fail open and route to unhealthy targets; “unhealthy” is not a guarantee of traffic isolation.

## 4. Build the directional security-group relationship

The ALB SG permits intended client traffic to the listener. The application SG permits the application and health-check ports from the ALB SG. ALB egress must reach those targets; database ingress should trust the application SG on its own port, not the ALB SG by assumption. This keeps the public entry and data tier distinct. Adding ingress is justified by this proposed traffic design and is not an automatic improvement to the current zero-ingress host.

## 5. Coordinate draining, deployments, and timeouts

During replacement, stop sending new work before terminating a target, and allow existing requests to finish within bounded deadlines. Align load-balancer deregistration behavior, application SIGTERM handling, request timeout, and runtime stop timeout. Long-running work may need an asynchronous model rather than ever-larger HTTP deadlines. Preserve old target capacity until the new revision becomes healthy. A deployment can be infrastructure-complete while failing customer workflows, so include separate synthetic or acceptance checks.

## Source or illustrative example

**New illustrative route design, not HCL or deployed configuration:** `/api/inquiries` and `/api/inquiries/*` forward to an inquiries target group; `/api/providers` and `/api/providers/*` forward to catalog; unmatched API paths receive a controlled response. An inquiries target uses `/health/ready` on its configured service port, matching the [existing API contract](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/CONTRACT.md). Including both collection and descendant paths avoids omitting the collection request. The exact listener patterns and health behavior must still be verified before implementing a target group; this sketch is deliberately not presented as existing Terraform.

## Safe exercise

Model the health-path response locally without opening a network listener:

```sh
node --input-type=module <<'JS'
const route = path => path === '/health/ready'
  ? {status:200, body:'ready'}
  : {status:404, body:'missing'};
for (const path of ['/health/ready','/wrong']) console.log(route(path).status);
JS
```

Expected outcome: `200`, then `404`. Explain how a wrong health path can reject a functioning listener. This tests a routing decision only: it does not verify HTTP transport, listener binding, headers, application readiness, or an AWS load balancer. Add those missing layers to the proposed validation checklist. A network-enabled local environment could later check the same behavior through an actual loopback HTTP server.

## Failure diagnosis

Use target health reason codes to distinguish response mismatch, timeout, registration, and availability problems. A 502 suggests examining backend protocol, connection handling, and invalid responses; a timeout suggests a different path than a deliberate 404. Compare the health-check request with successful manual requests, including Host header and auth expectations. If new targets repeatedly fail, preserve the stopped-task or application logs and deployment events before retrying the identical revision.

## Recall and answers

### Is a healthy target proof an inquiry can be committed?

No. A health check validates only the endpoint’s chosen readiness condition.

### Does ALB always stop routing when every target is unhealthy?

No. Its documented fail-open behavior can route to unhealthy registered targets, so do not use health as an authorization control.

## Mastery check

Produce a listener-rule table, target-port map, SG chain, and drain timeline. Diagnose wrong-path health failure and backend protocol failure separately. Explain why the proposed design is broader than the current development access model and how later business acceptance would complement health checks.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [ALB target-group health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
- [Fargate task networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html)
- [Security group rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)
- [ALB listener rules](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-rules.html)

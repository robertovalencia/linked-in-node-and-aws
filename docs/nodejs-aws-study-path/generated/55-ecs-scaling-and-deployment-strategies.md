---
title: "ECS service scaling and deployment strategies"
topic: "ECS service scaling and deployment strategies"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 55 · ECS service scaling and deployment strategies

**Prerequisites:** 51 and 53–54; readiness versus business acceptance.

[Previous: 54](54-ecs-networking-identity-and-secrets.md) · [Next: 56](56-ec2-autoscaling-and-eks-comparison.md) · [Study path](../README.md)

**Implementation boundary:** No ECS scaling policy or deployment controller is implemented by the existing AWS root. These are proposed operational mechanisms and local simulations.

Service scaling changes the desired number of application tasks. Compute-capacity scaling changes the underlying capacity available to run tasks; the concepts differ even when Fargate hides host provisioning. A rolling deployment gradually replaces tasks. A blue/green approach maintains old and new populations and shifts traffic under a chosen controller. A deployment circuit breaker detects certain failures to reach a steady state and can roll back to an eligible previous completed deployment.

## 1. Choose a signal that represents bottleneck pressure

CPU and memory can suit some HTTP services, but queue backlog age or in-flight work may better describe a worker. Target tracking aims to maintain a metric near a chosen target, within configured minimum and maximum tasks. Scale-out startup time and downstream limits matter: more workers can overload PostgreSQL or exhaust connections. Start with an explicit hypothesis about the bottleneck, then later validate it with measurements rather than treating a default CPU percentage as universal.

## 2. Model count bounds and startup delay

A minimum task count expresses baseline capacity and affects availability expectations; a maximum limits scale and protects downstream systems only imperfectly. Scaling is not instantaneous because task placement, image pull, initialization, and readiness take time. Headroom and cooldown decisions follow the workload’s burst behavior. During a rollout, old and new tasks can coexist, consuming additional subnet addresses and downstream connections. Capacity planning must include deployment overlap, not just the steady desired count.

## 3. Choose a deployment mechanism deliberately

Rolling replacement can be straightforward for compatible stateless revisions. Blue/green or weighted traffic shifting can expose a candidate to bounded traffic while preserving an earlier population. Current ECS deployment capabilities and supported controllers evolve, so verify the selected mechanism and its configuration before implementation. Define success signals, bake observation, and abort conditions. A task count reaching desired state proves less than correct authorization, durable writes, and event delivery under real requests.

## 4. Make rollback compatible with data evolution

Reverting an image digest does not undo a schema migration or external side effect. Use expand/contract changes where old and new code must overlap, and make workers tolerant of event-version compatibility during rollout. Stop accepting new work, drain bounded requests, and let durable work be retried safely. Keep the previous image and configuration available. A circuit breaker also needs a previous eligible completed deployment to roll back to; it cannot invent a known-good release.

## 5. Collect control-plane and application evidence

Inspect service events, stopped-task reasons, target health, revision identity, and application outcomes. For repeated placement or rollout failures, consider ECS Action Logs as a separate lifecycle evidence source if supported and intentionally enabled later. Application logs explain process behavior; control-plane logs explain orchestration steps. Configure retention and access deliberately and redact sensitive material. The curriculum does not enable logging or deploy resources; it teaches what evidence a future operator should collect.

## Source or illustrative example

**New illustrative rollout:** desired count 4, old revision A serves traffic, revision B starts, B readiness fails, and the rollout stops before retiring healthy A capacity. These counts are local reasoning inputs, not workload sizing or cost estimates. A different failure—B writes a backward-incompatible schema—cannot be solved by pretending traffic rollback reverses data changes.

## Safe exercise

Run a local rollout arithmetic check:

```sh
python3 - <<'PY'
desired, maximum_percent, minimum_percent = 4, 150, 100
import math
print('maximum running:', math.floor(desired * maximum_percent / 100))
print('minimum healthy:', math.ceil(desired * minimum_percent / 100))
PY
```

Expected outcome: maximum 6 and minimum healthy 4 for this illustrative rolling-count model. It is not a complete ECS scheduler. Draw the timeline for one new healthy task, one failed task, and database-connection growth. Then explain why a deployment could stall when no overlap capacity is available.

## Failure diagnosis

If desired count rises but running count does not, inspect placement constraints, subnet addresses, permissions, quotas, and startup failures. If adding tasks worsens latency, investigate the shared database, lock contention, or connection pool rather than increasing the maximum blindly. If deployments oscillate, compare health behavior, startup grace, scaling signals, and application shutdown. A circuit-breaker rollback with a healthy old revision is a release failure to investigate, not proof that all customer requests were unaffected.

## Recall and answers

### Is scaling a remedy for every latency incident?

No. It can increase pressure on a constrained downstream dependency.

### Does image rollback reverse a migration?

No. Schema and side effects need their own compatibility and recovery strategy.

## Mastery check

Produce a scaling hypothesis, count-bound model, rollout timeline, and rollback limitation statement. Diagnose desired-versus-running mismatch and an incompatible schema rollout. Identify the evidence needed to evaluate business success beyond a service reaching steady state.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [ECS service auto scaling](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html)
- [ECS deployment circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html)
- [ECS Action Logs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/action-logs.html)

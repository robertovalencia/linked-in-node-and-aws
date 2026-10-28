---
title: "ECS Fargate task definitions and services"
topic: "ECS Fargate task definitions and services"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 53 · ECS Fargate task definitions and services

**Prerequisites:** 46–49 and 51; image versus container from lesson 26.

[Previous: 52](52-cloudfront-s3-origins-and-caching.md) · [Next: 54](54-ecs-networking-identity-and-secrets.md) · [Study path](../README.md)

**Implementation boundary:** The repository currently runs Compose on EC2 and has no ECS task definition, ECS service, or Fargate deployment. All ECS examples in this sequence are new illustrative designs.

Amazon ECS is a container orchestrator. A task definition is a versioned blueprint describing one or more containers and their runtime requirements. A task is a running or attempted instance of that blueprint. An ECS service maintains a desired population of tasks and coordinates replacements. AWS Fargate supplies task compute without requiring the team to administer the underlying EC2 hosts. This changes host operations; application reliability, permissions, data ownership, and release correctness remain engineering responsibilities.

## 1. Choose the task boundary using lifecycle

Containers in one task share a scheduling and lifecycle boundary. An application plus a tightly coupled sidecar can fit together; four independently scaled business capabilities usually deserve separate service decisions. Do not translate an entire Compose file into one task solely because it worked on one host. The project shares a backend image across capabilities, but its SERVICE setting selects distinct processes. Image reuse does not require shared deployment, resource limits, credentials, or failure boundaries.

## 2. Describe the immutable runtime blueprint

Include image digest, command/environment configuration, container ports, log driver, health checks, CPU/memory, architecture, and role references. Select a currently supported Fargate CPU/memory combination rather than inventing arbitrary values. A task-definition revision describes an artifact and configuration, not an automatically updated service. Secrets belong in secret references rather than literal container-definition environment values. Keep compatibility with the built image architecture and the intended operating-system family explicit.

## 3. Separate a one-off task from a service

A migration or bounded batch job may be a one-off task; an HTTP API generally needs a service maintaining desired count. A service can replace failed tasks but does not make a single task continuously available during every failure. Define desired count, placement across suitable subnets, health integration, deployment overlap, and graceful stop behavior. Do not run a schema migration independently in every replica without deliberate locking and compatibility strategy.

## 4. Connect compute to network and data dependencies

Fargate uses awsvpc networking and a task network interface. Private tasks still need startup access to their registry, logs, and secrets. For a future ALB, use the target registration model appropriate for task IPs and restrict target ingress to the ALB SG. Durable PostgreSQL and Kafka data should not be assumed to survive on task-local ephemeral storage. Externalize data through an explicit service and recovery design rather than expecting an orchestrator to preserve a container disk.

## 5. Define evidence before a future rollout

Local JSON parsing checks only syntax. Terraform validation checks configuration against provider schemas; neither proves scheduling, image pull, runtime health, or business behavior. A later authorized rollout would inspect deployment events, stopped-task reasons, logs, target health, and acceptance results, and would preserve the exact image digest and task revision. This lesson stops at local modeling because deployment and cost decisions belong to the separate authorized workflow.

## Source or illustrative example

**New illustrative task-definition fragment, not registered or deployed:**

```json
{
  "family": "study-inquiries",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [{
    "name": "inquiries",
    "image": "REGISTRY/IMAGE@sha256:REPLACE_WITH_REAL_DIGEST",
    "essential": true,
    "portMappings": [{"containerPort": 8183}]
  }]
}
```

This deliberately incomplete fragment omits real role ARNs, logging, health configuration, and service networking. Placeholder image text is not a usable release identity.

## Safe exercise

Copy the fragment into a temporary local JSON file and run `python3 -m json.tool path/to/task.json`. Expected outcome: formatted valid JSON, not a runnable AWS task. Next write a checklist of the omitted runtime requirements. Compare the proposed task boundary with the [actual development infrastructure](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) and identify why existing PostgreSQL/Kafka volumes cannot simply be copied into stateless task assumptions.

## Failure diagnosis

A task that never reaches running status may fail placement, image retrieval, secret retrieval, or logging initialization. A running task that exits may have the wrong command, port, configuration, or resource limit. A service that repeatedly replaces tasks may be reacting to container or target health failures. Read the failed task’s reason before starting another identical attempt. Use application logs for code behavior and control-plane events for scheduling and lifecycle behavior; one stream cannot explain every failure.

## Recall and answers

### Does registering a task definition update every service automatically?

No. It creates a revision; the intended service must select and deploy the revision through an explicit release operation.

### Does Fargate make container-local data durable?

No. Persistence and recovery require a deliberate storage and data-service design.

## Mastery check

Explain task definition, task, service, and compute capacity without using them interchangeably. Produce a proposed per-capability task boundary and a missing-configuration checklist. State exactly what local JSON validation establishes and what remains unverified until a separately authorized runtime deployment.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [ECS task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [Fargate networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html)
- [ECS task execution role](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_execution_IAM_role.html)
- [ECS services](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_services.html)

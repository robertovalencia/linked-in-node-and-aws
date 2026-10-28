---
title: "EC2 Auto Scaling and EKS: choosing an operating model"
topic: "EC2 Auto Scaling and EKS: choosing an operating model"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 56 · EC2 Auto Scaling and EKS: choosing an operating model

**Prerequisites:** 53–55 and the existing EC2/bootstrap lesson.

[Previous: 55](55-ecs-scaling-and-deployment-strategies.md) · [Next: 57](57-rds-postgresql-backups-and-failover.md) · [Study path](../README.md)

**Implementation boundary:** The project has one EC2 instance, not an Auto Scaling group or EKS cluster. The comparisons below identify future options rather than recommend or deploy a replacement.

EC2 Auto Scaling maintains a group of virtual machines according to desired capacity and configured policies. A launch template describes instance launch settings. ECS orchestrates tasks; EKS provides managed Kubernetes control-plane capabilities and associated operating options. Kubernetes schedules Pods, which are groups of containers sharing a lifecycle and network context. The professional decision is which responsibilities and ecosystem requirements fit the team, not which service name appears most advanced.

## 1. Separate the application replica from its host

A VM group can replace a failed machine, but it does not automatically coordinate four services, migrate their data, or preserve local disks. The project’s PostgreSQL/Kafka volumes share its host failure boundary. Before proposing an Auto Scaling group, externalize durable data and define reproducible bootstrap, readiness, registration, and release identity. A replacement that launches successfully with empty data is not recovery. State the unit that scales: host, task, Pod, database, or worker concurrency.

## 2. Understand launch templates and replacement

A launch template can specify AMI, instance characteristics, networking, metadata settings, and bootstrap. Version changes do not mean every existing instance has been replaced immediately; a controlled refresh strategy is separate. Health checks and lifecycle hooks can coordinate readiness and draining. Design immutable replacement rather than relying on undocumented manual host edits. Review root-volume deletion behavior and backup independence, especially when a template change can cause instances to be replaced.

## 3. Compare ECS operating choices

Fargate removes direct host administration for supported tasks. ECS on self-managed EC2 gives more host control and requires capacity/patching operations. ECS Managed Instances offers another service-managed compute model with its own capabilities and constraints. All still require container image provenance, task identity, traffic controls, logs, and application-level correctness. Compare required kernel features, hardware, isolation, operational ownership, and support constraints using current documentation. Do not reduce the choice to a price claim in this curriculum.

## 4. Understand what EKS adds and leaves to you

EKS supports the Kubernetes API and ecosystem, including workloads, controllers, and policy tooling. Deployment resources manage Pod revisions; Services provide stable service abstractions; Ingress or Gateway integrations can connect external traffic through supported controllers. Managed node groups and EKS Auto Mode change parts of node operations, but cluster access, application policy, upgrades, add-ons, network behavior, and workload security still need accountable owners. Using Kubernetes names without operating these responsibilities is not a production design.

## 5. Make a requirement-driven decision record

Write the required workload features, team skills, portability needs, failure tolerance, deployment frequency, and debugging workflow. Then explain why simpler options do or do not satisfy them. “We already run Docker” does not imply a need for Kubernetes; a required operator or established Kubernetes platform can be a concrete reason. Separate technical suitability from a future cost/deployment decision, which belongs to the other project workflow. Record uncertainty and the evidence that would change the recommendation.

## Source or illustrative example

**Actual source anchor:** [EC2 instance, metadata, root storage, and user-data replacement settings](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf). **New illustrative comparison:** an inquiry API might run as an ECS service, Kubernetes Deployment, or software on an Auto Scaling group. Each requires a distinct readiness and data-recovery design. These are alternatives for reasoning, not three resources present in the repository.

## Safe exercise

Create a local responsibility matrix using a plain text file or this command:

```sh
python3 - <<'PY'
models = ['single-ec2', 'asg', 'ecs-fargate', 'eks']
for model in models:
    print(model, ': app-health=?, data-recovery=?, host-patching=?, identity=?')
PY
```

Expected outcome: four rows to complete using the lesson and references. For each model, assign responsibility to AWS or the team at a specific layer; mixed responsibility is allowed. Explain what happens when the host disappears and when an application process becomes unhealthy without the host failing.

## Failure diagnosis

If a VM group keeps replacing instances, inspect readiness, bootstrap, health-check grace, and registration rather than assuming the AMI is corrupt. If Pods remain pending, distinguish node capacity, scheduling constraints, networking, and identity. If an orchestrator reports healthy replicas but data vanished, the problem is storage/recovery architecture. A comparison missing a named owner for upgrades or credentials is incomplete even if its service diagram looks resilient.

## Recall and answers

### Does an Auto Scaling group make host-local PostgreSQL highly available?

No. Replacing compute is different from replicating and recovering durable database state.

### When is EKS a defensible choice?

When concrete Kubernetes ecosystem or platform requirements justify its responsibilities and the team can operate them.

## Mastery check

Defend a compute choice using a written requirement and responsibility matrix. Identify one reason each alternative may be unsuitable. Explain the existing single-host failure boundary honestly, and distinguish orchestration, host replacement, and data recovery in every answer.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [EC2 Auto Scaling overview](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [Amazon EKS overview](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
- [ECS task definitions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html)
- [ECS compute choices](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ManagedInstances.html)

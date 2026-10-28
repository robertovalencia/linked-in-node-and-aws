---
title: "Professional AWS/Terraform capstone and question bank"
topic: "Professional AWS/Terraform capstone and question bank"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 83 · Professional AWS/Terraform capstone and question bank

**Prerequisites:** Complete the core coverage map and local labs; repair weak prerequisites first.

[Previous lesson](82-terraform-advanced-local-lab.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. Assess coverage at concept level

Reading every page is not the same as mastering its mechanisms. Use the coverage map to track foundations, networking, identity, compute, data, messaging, delivery, security, observability, recovery and Terraform lifecycle. Each item needs an explanation, an example and evidence appropriate to the learning stage. A service absent from the project remains a valid learning topic with an explicitly new example.

Treat specialist topics as continuing study rather than claiming the syllabus contains every possible AWS feature. A professional engineer must recognize unfamiliar services, find current primary documentation, understand quotas/constraints and choose evidence before acting. That skill is more durable than memorizing the service catalog.

## 2. Assemble an architecture defense packet

Include a current baseline diagram, proposed-example diagram, identity/permission matrix, allowed/denied traffic table, data/recovery model, event-delivery crash windows, Terraform root/module/state map, release evidence chain, observability contracts and a decision-status table. Keep actual implementation and hypothetical design visually distinct.

Explain the current no-ingress SSM path before discussing an ALB. Explain the business transaction/outbox before proposing RDS/MSK. Explain local Terraform state and module identity before discussing remote runners. The order makes your reasoning auditable and prevents a new service name from hiding an unresolved invariant.

## 3. Demonstrate the local mechanics

Run the basic Terraform lab, advanced module/state lab and network reasoning lab. For each, predict the result, show actual output and name what it cannot establish about AWS. A built-in-provider test can demonstrate local identity/refactoring mechanics, but cannot establish IAM authorization, availability-zone failover, managed-service connectivity or actual account cost.

A useful review also includes a failed-then-repaired local result. Do not weaken assertions to achieve green output. Explain the violated invariant and why the repair changes the behavior.

## 4. Rehearse a ten-minute professional explanation

Spend the first two minutes on the business journey and real baseline; the next two on identity and network boundaries; the next two on state/data/recovery; the next two on Terraform/delivery/observability; and the final two on tradeoffs, evidence limits and pending cost-first decisions. Time allocation is a practice suggestion, not an assessment result.

Support every claim of execution with an actual artifact. “I designed an example” and “I operated this in AWS” are different statements. It is strong engineering judgment to say what remains pending and which test would resolve it.

## 5. Grade with observable criteria

For each domain score missing, definition-only, project/example explanation, or demonstrated mechanism with limits. Repeat weak areas using changed inputs, not just rereading. A correct answer includes failure behavior and a tradeoff. For example, private networking needs an intentional egress/endpoints path; a backup needs a proven restore; a Terraform plan needs secure artifact handling and a matching source/account context.

## 6. Respect the deployment owner’s sequence

The other chat owns all real cost assessment, selected modernization plan and eventual deployment work. Your capstone may produce questions and requirements for it, but does not authorize provisioning. Read the owner’s published cost/HTTPS review linked from lesson80. Keep bootstrap approval, final S3-backed plan review and live gates pending; source proposals do not establish deployment.

## Example and current-project boundary

**Capstone artifact list:**

```text
Baseline and illustrative diagrams
Concept-level evidence checklist
Identity/traffic threat model
State, modules, migrations and recovery explanation
Local lab transcripts and limits
Delivery/telemetry acceptance matrix
Cost/deployment owner handoff status
Largest remaining learning gap
```

Use the pinned [current architecture](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/docs/architecture.md) as baseline evidence. For absent services, cite the official source and your clearly labeled example instead of inventing a project file.

## Practice with observable evidence

1. Finish all three local labs and annotate one failed/passing transition in each relevant domain.
2. Ask a reviewer to select ten coverage concepts randomly; explain them without notes.
3. Rehearse the architecture defense and record claims needing source or execution evidence.
4. Submit a final packet with unresolved owner decisions, rather than filling them with assumed prices or deployed resources.

**Expected evidence:** a coherent ten-minute defense, complete concept checklist and a prioritized remaining-gap list.

## Recall and interview defense

### How would you secure ingress in a proposed ALB architecture?

Start with intended clients and TLS, then narrow ALB-to-app and app-to-data group permissions. Verify forbidden direct paths, task identity, encryption and application authorization separately.

### When would NAT be preferable to interface endpoints, or vice versa?

Compare required destinations, availability, traffic paths, operational constraints and current assessed costs. Neither choice is universally cheaper or automatically required.

### What makes an RDS backup or Multi-AZ choice defensible?

State recovery requirements, tested restore/failover behavior, connection handling and cost implications. Do not confuse replication, backup and regional disaster recovery.

### Why separate Terraform state by ownership/environment?

To control credentials, visibility, blast radius and lifecycle. A workspace name alone is not a complete security boundary.

### What is still pending in this portfolio?

The owner has published the cost comparison and private preview-plan review. Separate bootstrap approval, the final S3-backed application plan, provisioning, live security/recovery/smoke checks and teardown evidence remain pending. Certificate issuance alone is verified.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [Terraform language reference](https://developer.hashicorp.com/terraform/language)
- [AWS architecture decision records](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)

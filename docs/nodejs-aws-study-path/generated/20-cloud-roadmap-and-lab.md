---
title: "AWS and Terraform: a practical learning roadmap"
topic: "AWS and Terraform: a practical learning roadmap"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 20 · AWS and Terraform: a practical learning roadmap

**Prerequisites:** Node lesson 14, basic terminal/Git, JSON, HTTP and Docker. No prior AWS account or Terraform experience is required.

[Cloud overview](15-aws-terraform-and-delivery.md) · [Next: 21](21-aws-accounts-regions-and-cli.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Start with the responsibility of each tool

AWS supplies infrastructure APIs: machines, networks, identities, storage and operational services. Terraform is a client that declares desired resources, compares them with recorded/observed infrastructure and proposes actions. Docker packages processes. GitHub Actions coordinates checks and releases. Node.js runs application business logic. Learn which problem each solves before learning command flags.

The portfolio is deliberately small: four NestJS services, PostgreSQL, Kafka and nginx share one EC2 host. A single host is understandable and economical for a temporary demonstration, but remains one failure domain. Terraform files are a prepared deployment design. Reading them or passing mock tests does not establish that the cloud deployment has run.

## 2. Follow four learning gates

| Gate | Sessions | Lessons | Show before continuing |
|---|---|---|---|
| AWS foundations | 1–8 |21–27 |Draw identity, network, machine, image and secret paths |
| Operations and tradeoffs |9–12 |28–31 |Explain persistence, failure diagnosis, costs and a production redesign |
| Terraform mechanics |13–20 |32–39 |Run the local no-AWS lab; explain state, plans, replacements and tests |
| Release and interview |21–24 |40–43 |Trace exact-SHA verification to image digest, SSM deployment and rollback |

Spend roughly 60–90 minutes per session: read a concept, open its source, predict the result, run a small exercise, and explain it aloud. A session may take several evenings; gates are based on evidence, not speed. After every four sessions, redraw the architecture without notes and revisit your weakest explanation.

## 3. Know what is implemented and what is an extension

The current source uses a public subnet for outbound access, no ingress security-group rules, and SSM port forwarding to a loopback-bound frontend. The selected runbook uses temporary local credentials with GitHub verification. Optional OIDC deployment is supported but is not the selected mode. There is no ALB, NAT gateway, RDS, MSK, ECS service, or CloudWatch agent in this stack.

Production alternatives are studied as design exercises, not represented as implemented resources. Their configuration, costs and operation need separate work. This foundation block explains the project’s AWS/Terraform responsibilities. Continue with [44 · the complete professional core syllabus](44-cloud-complete-syllabus-and-mastery-map.md) for important concepts beyond this repository; absent services receive explicitly illustrative examples.

## 4. Separate learning modes

Read-only source exercises need no account. The Terraform lab in 32 uses only the built-in provider and creates local state in a temporary directory. Mock tests in 39 exercise the real AWS configuration without provisioning resources. Optional account inspection requires credentials. Cloud creation, secret population, deployment and destruction use the existing reviewed-plan process; do not run them just to finish a lesson.

## Walk the real project

[docs/aws-dev.md · lines 5–8](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/docs/aws-dev.md#L5-L8)

```text
## Why one EC2 host

The four Node services, PostgreSQL, Kafka, and frontend run on one `m7i-flex.large` Amazon Linux 2023 x86_64 host (2 vCPU, 8 GiB RAM) in `us-east-2` for the selected 24-hour Free plan demonstration. Each service still owns a distinct database and role. A single host keeps a small dev environment explainable and avoids an ALB, NAT gateway, RDS, and managed Kafka baseline bill. ECS/Fargate plus RDS/MSK would improve service lifecycle and database resilience, but brings more infrastructure and a higher minimum bill. This deployment has no high availability, automated backups, or production SLO claim. Database and Kafka volumes live on the encrypted root disk: replacing/terminating the instance loses them. Snapshot/export before replacement.

```

Open the diagram in the full operating guide. Identify two paths: browser requests go through an SSM tunnel, while release preparation publishes images and bundles before the host retrieves them. Terraform provisions infrastructure; the release scripts start application versions. Keeping those paths separate will make the later lessons easier.

## Practice step by step

1. Create a personal table with columns: lesson, prediction, command/source, observed result, explanation, next question.
2. Draw AWS account → region → VPC → subnet → EC2 → Docker services. Add S3/ECR/Secrets Manager beside it.
3. Mark implemented resources in one color and proposed managed-service replacements in another.
4. Begin 21; defer cloud commands until their prerequisites are satisfied.

**Expected evidence:** A labeled diagram, a personal evidence table and a clear distinction between local learning and cloud-changing operations.

## Check your understanding

### Can Terraform replace Docker or Node.js?

No. Terraform manages the resource graph; containers package the running software; Node executes its application logic. Explain the handoff through EC2 bootstrap and release scripts.

### How do I know I have learned a lesson?

You can predict an observable result, demonstrate it, explain the mechanism and name a failure case. Copying a command without those steps is not the exit criterion.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [AWS service overview](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)

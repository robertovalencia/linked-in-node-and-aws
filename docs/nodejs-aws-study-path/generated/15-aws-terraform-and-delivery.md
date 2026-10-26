---
title: Infrastructure overview: AWS, Terraform and delivery
topic: AWS and Terraform overview
last_researched: 2026-10-26
---

# Infrastructure overview: how the cloud learning path fits together

This lesson is the bridge from local containers to cloud responsibilities. Continue with [the detailed AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md), which breaks the material into 24 ordered lessons with source walkthroughs, exercises and mastery checks.

## 1. Separate the responsibilities

Terraform manages infrastructure resources and their state. AWS supplies the account APIs. Docker images package application processes. The release scripts select verified image digests, retrieve runtime configuration and start the application. GitHub checks source/runtime quality. These are separate tools and quality boundaries.

The real Node.js project has two Terraform roots: bootstrap manages the protected state bucket and optional OIDC provider; aws-dev manages the VPC, subnet, no-ingress security group, EC2 host/profile, ECR app repositories, release bucket and secret metadata. Read [the current resource definitions](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf) and [the operating guide](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/docs/aws-dev.md).

## 2. Explain the current access path

A public subnet/public IPv4 supports outbound package, registry and AWS API access. No security-group ingress is permitted. An authenticated SSM tunnel forwards laptop 8088 to host loopback 80; Compose maps it to frontend container 8180. PostgreSQL/Kafka stay on the Docker network. This is a single-host dev design, not a private-subnet or high-availability architecture.

## 3. Learn the selected delivery mode first

The selected runbook uses temporary local AWS login in us-east-2 and enable_github_deployment=false. GitHub performs exact-source verification; the local release helper publishes/scans images and invokes SSM. Optional GitHub OIDC mode is retained for a separately eligible/authorized environment. Its trust pins audience and repository environment; it is not the selected account path. Generic Terraform defaults differ from selected example inputs, so always inspect effective configuration.

## 4. Use the expanded path for individual mechanisms

- [21–27: accounts, IAM, networking, SSM, EC2, ECR, S3 and secrets](21-aws-accounts-regions-and-cli.md).
- [28–31: data decisions, observability, cost/cleanup and production tradeoffs](28-aws-data-and-messaging-decisions.md).
- [32–39: HCL, versions, inputs, graph, state, plans, lifecycle and tests](32-terraform-hcl-and-first-local-lab.md).
- [40–43: CI/OIDC, SSM rollout/rollback, troubleshooting and capstone](40-aws-release-pipeline-and-oidc.md).

## Practice and checkpoint

Draw source SHA → verification → image digest → manifest → SSM → readiness → 48-check acceptance. Add Terraform state alongside the infrastructure graph rather than confusing it with a release bundle. Explain why image rollback cannot reverse destructive database migration.

**Answer:** Images, database state, Terraform state and release evidence have different ownership and lifetimes. Each requires its own recovery/validation story. A passing plan or local lab proves only its actual assertions. No cloud creation is needed to finish this overview.

## References

- [Terraform configuration language](https://developer.hashicorp.com/terraform/language)
- [AWS IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [SSM Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)

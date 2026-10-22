---
title: AWS dev infrastructure, Terraform and immutable delivery
topic: AWS and Terraform
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Explain the infrastructure that exists

Prerequisites: 14 and basic IP/port concepts. AWS infrastructure is described in code; its presence does not prove it was provisioned. The current design is a private-access development environment on one EC2 host running Compose. RDS, MSK, ECS/Fargate, Lambda, API Gateway, ALB, CloudFront and multi-zone failover are possible extensions, not current application components.

## Walk the actual request and release paths

infra/aws-dev/main.tf creates a VPC, subnet, internet gateway and outbound route. The subnet allows a public IP, but the security group has zero ingress rules. EC2 uses AL2023, an encrypted gp3 disk, IMDSv2 and an instance role. SSM Session Manager manages the host and tunnels browser traffic to the loopback frontend. A public-IP-capable subnet is not the same as a public-facing application; SSM availability still depends on agent, IAM and network reachability.

The host role can read the runtime secret, pull designated ECR images and read release objects. ECR has separate backend/frontend repositories with immutable tags, scanning and lifecycle rules. The S3 release bucket is private, versioned and encrypted and denies insecure transport. Runtime configuration uses Secrets Manager; metadata creation in Terraform is distinct from setting a secret value. Do not put secret values into a tfvars file or show them in lesson evidence.

GitHub's dev-environment OIDC identity assumes a constrained deployment role instead of storing long-lived AWS access keys. Deployment builds/images/scans resolve immutable commit tags to digests, stores a release manifest in S3 and uses SSM to invoke the host deployment. Smoke checks and rollback scripts operate on exact release artifacts. Source configuration is not evidence that GitHub, Sonar or AWS integrations have run successfully.

## Terraform model and safe local lab

Terraform configuration is desired resources; state maps them to actual infrastructure. plan computes proposed changes against state/provider observations; apply performs them. State and saved plans may contain sensitive material. infra/bootstrap prepares the private, versioned state bucket with AES256 server-side encryption and optional GitHub OIDC provider; application backend configuration enables S3 locking. The release bucket separately uses AES256 server-side encryption. No custom KMS key resource is defined in these Terraform files. Learn KMS key-policy/rotation tradeoffs as a proposed extension; do not label this design as customer-managed-KMS-encrypted or confuse state infrastructure with runtime data.

Read infra/aws-dev/{main,variables,outputs,versions}.tf, infra/bootstrap/main.tf, infra/aws-dev/tests/security.tftest.hcl, .github/workflows/deploy-dev.yml and scripts/aws-remote-deploy.sh. Then execute only local preparation, if Terraform/provider dependencies are available:

~~~bash
terraform -chdir=infra/aws-dev fmt -check
terraform -chdir=infra/aws-dev init -backend=false
terraform -chdir=infra/aws-dev validate
terraform -chdir=infra/aws-dev test
~~~

Expect format/validation/test success only if prerequisites are satisfied. init can download providers; it does not create cloud resources. Review the test's mock/provider behavior before running. A real plan requires credentials/backend inputs and may query AWS; save/review it separately. Provisioning needs approval of the concrete saved plan and current cost estimate under the project agreement. No apply/deploy is required by this study lesson.

## Senior design extension lab

Draw a production alternative with managed database/broker, multiple application instances, TLS ingress, centralized logs/metrics/traces and tested backup restore. State RTO/RPO, connection/partition capacity and expected spend drivers. Compare it with a modular monolith on fewer services. Do not assume “more AWS services” is better. Price and quota claims must be verified when used; do not memorize an old cost estimate as current fact.

Azure is explicitly required by the role but not implemented here. Map EC2 to VM, ECR to ACR, S3 to Blob Storage, IAM/workload identity to Entra/workload identity and Secrets Manager to Key Vault. These are purpose comparisons, not identical semantics. Specify one Azure deployment plan with networking, identity and rollback evidence; execution is a separately approved extension.

Interview:

### How does the browser reach AWS?

Through an authenticated SSM tunnel in this dev design.

### What survives host loss?

Single-host volumes are a shared failure domain; state/release buckets do not magically back up PostgreSQL.

### Why immutable digests?

They identify exact image content for audit and rollback.

- [ ] Draw actual AWS networking and IAM boundaries.
- [ ] Explain state, plan, apply, locking and sensitive artifacts.
- [ ] Trace requirement → commit → digest → manifest → smoke result.
- [ ] Distinguish actual AWS source, unverified execution and proposed Azure/production designs.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [AWS Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) — accessed 2026-10-22.
- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan) — accessed 2026-10-22.
- [GitHub OIDC in AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) — accessed 2026-10-22.
- [Azure for AWS professionals](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/) — accessed 2026-10-22.
- [Project source: infra/aws-dev/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/infra/aws-dev/main.tf) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/aws-dev/versions.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/infra/aws-dev/versions.tf) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/bootstrap/main.tf](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/infra/bootstrap/main.tf) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: infra/aws-dev/tests/security.tftest.hcl](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/infra/aws-dev/tests/security.tftest.hcl) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: .github/workflows/deploy-dev.yml](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/.github/workflows/deploy-dev.yml) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: scripts/aws-remote-deploy.sh](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/scripts/aws-remote-deploy.sh) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/azure-mapping.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/azure-mapping.md) — local baseline inspected 2026-10-22; private published source may lag.

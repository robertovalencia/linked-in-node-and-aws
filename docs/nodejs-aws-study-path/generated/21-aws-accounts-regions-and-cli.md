---
title: "AWS accounts, regions, resource names and CLI identity"
topic: "AWS accounts, regions, resource names and CLI identity"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 21 · AWS accounts, regions, resource names and CLI identity

**Prerequisites:** 20 and the difference between a process, machine and network.

[Previous: 20](20-cloud-roadmap-and-lab.md) · [Next: 22](22-aws-iam-roles-and-policies.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Account and region are part of every investigation

An account is an administrative/billing boundary. A region selects a geographical AWS operating area; Availability Zones are separate locations within a region. A VPC is regional and a subnet belongs to one zone. This project creates one subnet, not a multi-zone service. An ARN identifies a resource or principal with service-specific structure; a resource name alone does not prove which account owns it.

## 2. Trace configuration before executing commands

Named CLI profiles select configuration and credential sources. Temporary sessions expire. Environment variables can affect profile/region selection, so “it worked yesterday” is not a reliable identity check. Never copy authentication tokens into a lesson or Git file. The project selected profile `marketplace-dev` and region `us-east-2`; those are runbook choices rather than universal AWS defaults.

## 3. Distinguish examples from effective values

`variables.tf` defaults to `us-east-1`, while `dev-local.tfvars.example` explicitly selects `us-east-2`. A default is used only when nothing overrides it. The S3 backend has its own region setting; changing the AWS provider region does not relocate a backend bucket. Teach yourself to identify provider configuration, backend configuration and release-script environment separately.

## 4. Use read-only inspection deliberately

`aws sts get-caller-identity` reports the effective identity. It does not prove permission to create EC2, read a secret or run SSM. An organization policy can still deny a later action. The existing account's OIDC restriction led to a local-login design; bypassing policy is not part of the learning route. Basic identity inspection is optional for this lesson; the source-only exercise is sufficient before you have credentials.

## Walk the real project

[infra/aws-dev/dev-local.tfvars.example · lines 1–7](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/dev-local.tfvars.example#L1-L7)

```hcl
# Selected 24-hour Free plan demo: GitHub validates; local temporary credentials deploy.
# This mode does not create or manage an account-wide GitHub OIDC provider.
region                   = "us-east-2"
project                  = "linked-in-node"
github_repository        = "robertovalencia/linked-in-node-and-aws"
instance_type            = "m7i-flex.large"
enable_github_deployment = false
```

[infra/aws-dev/outputs.tf · lines 8–10](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/outputs.tf#L8-L10)

```hcl
output "deployment_account_id" { value = data.aws_caller_identity.current.account_id }

output "deployment_region" { value = var.region }
```

Compare the selected input file with `variables.tf`. Then locate the local release helper's `get-caller-identity` call and its comparison with Terraform's `deployment_account_id` and `deployment_region` outputs. This is a concrete guard against deploying into the wrong account, not merely a convenient CLI display.

## Practice step by step

1. From the repository, run `git rev-parse HEAD` and inspect the two example tfvars files.
2. Write the selected profile, provider region, backend region and expected account ID as four separate fields; leave unknown IDs explicitly unknown.
3. Optional, when already authenticated: run `AWS_PROFILE=marketplace-dev AWS_REGION=us-east-2 aws sts get-caller-identity` and `aws configure list --profile marketplace-dev`.
4. Compare returned account/ARN with the intended environment. Do not publish credential files or token-bearing output.

**Expected evidence:** A configuration table explaining exactly where each effective value comes from; optional identity output with sensitive context excluded from public notes.

## Check your understanding

### Does successful login authorize every deployment operation?

No. Authentication establishes the principal; policies authorize individual actions. Investigate the denied operation and its resource scope.

### Why can provider and backend regions differ?

They address different things: managed AWS resources versus the S3 object storing Terraform state. Both must be configured intentionally.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [AWS CLI profiles and settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- [Temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html)

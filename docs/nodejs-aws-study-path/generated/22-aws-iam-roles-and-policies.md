---
title: "IAM: principals, roles, trust and scoped permissions"
topic: "IAM: principals, roles, trust and scoped permissions"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 22 · IAM: principals, roles, trust and scoped permissions

**Prerequisites:** 21 and basic JSON objects/arrays.

[Previous: 21](21-aws-accounts-regions-and-cli.md) · [Next: 23](23-aws-vpc-subnets-and-routing.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Separate who may assume a role from what it may do

A role is an assumable identity. Its trust policy admits particular principals; its permission policies describe allowed actions/resources after assumption. A role ARN is an identifier, not a credential. STS provides temporary credentials to an authorized session. These concepts differ from the marketplace JWT, which identifies application users and roles.

## 2. Read an IAM statement from left to right

Find Effect, Action, Resource and optional Condition. In the host policy, secret reads are scoped to one secret ARN, image pull operations to two ECR repositories, and bundle reads to `releases/*`. `ecr:GetAuthorizationToken` uses wildcard resource scope, but that is not a reason to grant wildcard image or secret access. A scoped permission should match the operation's supported resource type.

## 3. Follow the EC2 identity chain

EC2 assumes the host role through its instance profile. The host runs bootstrap and deployment commands. Containers here receive configuration from a protected environment file; they do not each assume distinct AWS task roles. Consequently, host root/SSM access is a powerful trust boundary. Requiring IMDSv2 and hop limit 1 reduces exposure but is not a substitute for permission scoping.

## 4. Understand denial before changing policy

An explicit deny can override allows. Effective authorization can also depend on organization controls, boundaries, session policies and resource policies. Do not “fix” AccessDenied by attaching administrator access. First identify caller, API action, resource ARN and applicable policy layer. The application's provider ownership check remains necessary even if AWS infrastructure permissions are correct.

## 5. Compare the two deployment identities

The selected temporary-login path uses the operator's authorized AWS session. The optional GitHub path creates a distinct deploy role and restricts OIDC audience and repository environment. Disabling that optional role does not remove the EC2 host role. The Terraform tests explicitly verify this distinction.

## Walk the real project

[infra/aws-dev/main.tf · lines 90–98](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L90-L98)

```hcl
resource "aws_iam_role_policy" "host" {
  role = aws_iam_role.host.id
  policy = jsonencode({ Version = "2012-10-17", Statement = [
    { Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = aws_secretsmanager_secret.runtime.arn },
    { Effect = "Allow", Action = ["ecr:GetAuthorizationToken"], Resource = "*" },
    { Effect = "Allow", Action = ["ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer", "ecr:BatchCheckLayerAvailability"], Resource = [for r in aws_ecr_repository.app : r.arn] },
    { Effect = "Allow", Action = ["s3:GetObject"], Resource = "${aws_s3_bucket.releases.arn}/releases/*" }
  ] })
}
```

[infra/aws-dev/main.tf · lines 99–100](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L99-L100)

```hcl
resource "aws_iam_instance_profile" "host" { role = aws_iam_role.host.name }
resource "aws_instance" "dev" {
```

Annotate every host-policy statement with caller, purpose and allowed resource. Then open the optional deploy policy and compare upload/publish/RunCommand permissions with the host's download/read permissions. The release producer and release consumer need different capabilities.

## Practice step by step

1. Make a table for operator, optional GitHub deploy role, EC2 host role, and marketplace JWT user.
2. For each, name credential type, trust decision, allowed operation and boundary it cannot cross.
3. Locate one broad resource scope and explain its API-specific reason; locate three narrowed scopes.
4. Diagnose a hypothetical ECR pull denial before proposing any policy change.

**Expected evidence:** An annotated identity matrix and a diagnosis that distinguishes trust failure, permission failure and application ownership failure. No IAM writes are needed.

## Check your understanding

### Does an EC2 trust policy grant permission to read Secrets Manager?

No. It permits role assumption; a separate permission statement authorizes the secret read.

### Can a valid marketplace JWT invoke SSM?

Not by itself. Application claims and AWS principal credentials belong to different authorization systems.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [Temporary credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html)

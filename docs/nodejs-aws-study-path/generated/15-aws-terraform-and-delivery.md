---
title: "Infrastructure tools: Terraform, IAM, SSM, ECR and releases"
topic: "Infrastructure tools: Terraform, IAM, SSM, ECR and releases"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Infrastructure tools: Terraform, IAM, SSM, ECR and releases

Prerequisites: containers, configuration and failure boundaries. These are infrastructure mechanisms used by the prepared AWS development setup.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## Terraform resources, references and plans

**What:** Terraform describes desired resources. A plan compares configuration, state and provider observations to propose changes.

**How:** Resource references form dependency relationships. State tracks managed identities and can contain sensitive values; it is not just a harmless configuration cache.

**Real code:** [infra/aws-dev/main.tf · lines 13–17](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L13-L17).

```hcl
resource "aws_subnet" "dev" {
  vpc_id                  = aws_vpc.dev.id
  cidr_block              = "10.84.1.0/24"
  map_public_ip_on_launch = true
}
```

**Watch for:** Preparing a plan is different from approving and applying it; no cloud provisioning is needed to read these lessons.

### What does vpc_id = aws_vpc.dev.id express?

The subnet uses the managed VPC’s identity and depends on that resource relationship.

## Security groups and the actual access path

**What:** A security group filters instance traffic. An internet gateway route does not automatically permit inbound application access.

**How:** This development group has no ingress rules. SSM manages the instance and tunnels browser access; it is not an existing public load-balanced multi-AZ deployment.

**Real code:** [infra/aws-dev/main.tf · lines 30–36](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L30-L36).

```hcl
resource "aws_security_group" "dev" {
  name        = local.name
  description = "No ingress. SSM manages host and tunnels browser traffic."
  ingress     = []
  vpc_id      = aws_vpc.dev.id
  egress {
    from_port   = 0
```

**Watch for:** A public-IP-capable subnet and an open application endpoint are not equivalent.

### Why does a route to the internet not make port 8180 public?

Other controls still apply, including the security group’s absence of ingress permission.

## IAM roles and GitHub OIDC

**What:** IAM permissions say what a principal may do. A trust policy says which identity may assume a role.

**How:** The deploy role trusts GitHub’s OIDC subject for this repository’s dev environment. Temporary identity avoids placing permanent AWS access keys in the workflow.

**Real code:** [infra/aws-dev/main.tf · lines 122–125](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L122-L125).

```hcl
resource "aws_iam_role" "deploy" {
  name               = "${local.name}-github-deploy"
  assume_role_policy = jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Allow", Principal = { Federated = var.oidc_provider_arn }, Action = "sts:AssumeRoleWithWebIdentity", Condition = { StringEquals = { "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com", "token.actions.githubusercontent.com:sub" = "repo:${var.github_repository}:environment:dev" } } }] })
}
```

**Watch for:** A valid role session still needs appropriately scoped resource permissions.

### Why restrict the OIDC subject?

Otherwise an unintended repository or workflow identity might obtain deployment credentials.

## ECR tags, digests and immutability

**What:** ECR stores container images. A tag is a name; a digest identifies image content.

**How:** The repositories make tags immutable and enable scanning. Deployment resolves digest references so an approved release describes exact image content rather than a mutable nickname.

**Real code:** [infra/aws-dev/main.tf · lines 46–52](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L46-L52).

```hcl
resource "aws_ecr_repository" "app" {
  for_each             = toset(["backend", "frontend"])
  name                 = "${local.name}/${each.key}"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = true
  image_scanning_configuration { scan_on_push = true }
  encryption_configuration { encryption_type = "AES256" }
```

**Watch for:** A clean scan is one security input, not proof that application permissions or business behavior are correct.

### Why use a digest in a release manifest?

It fixes the image content that deployment should pull.

## Secrets Manager and scoped reads

**What:** Secrets Manager stores runtime secret values. Terraform here creates secret metadata; values are supplied separately.

**How:** The host role receives scoped read permission for that secret and release objects. Application code then reads environment variables, not a Secrets Manager SDK in every handler.

**Real code:** [infra/aws-dev/main.tf · lines 90–98](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L90-L98).

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

**Watch for:** A secret ARN is an identifier, not the secret value; do not confuse prepared metadata with configured credentials.

### Does this Node backend call Secrets Manager on every login?

No. The deployment path assembles runtime configuration for the processes.

## State storage, encryption and locking

**What:** Versioning keeps older object versions; encryption protects stored bytes; locking coordinates competing Terraform writers.

**How:** Bootstrap config enables versioning and AES256 encryption for its state bucket. That is SSE-S3; a custom customer-managed KMS key is a separate design choice.

**Real code:** [infra/bootstrap/main.tf · lines 16–23](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/bootstrap/main.tf#L16-L23).

```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "state" {
  bucket = aws_s3_bucket.state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

**Watch for:** Versioning and locking do not replace least-privilege state access or a recovery plan.

### Does encryption prevent two simultaneous state writers?

No. Encryption and concurrency locking address different risks.

## Azure equivalents require a fresh design

**What:** Cloud services can serve similar roles without having identical APIs, permissions or operational behavior.

**How:** The project documents an Azure mapping. Treat an Azure lab as an extension: translate identity, networking, secrets and artifact access deliberately rather than renaming AWS resources.

**Real code:** [docs/azure-mapping.md · lines 1–5](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/docs/azure-mapping.md#L1-L5).

```text
# Explaining the Azure equivalents

AWS is the implemented deployment target. This is an interview comparison, not an Azure deployment or tested portability claim. The mappings follow [Microsoft's AWS/Azure comparison](https://learn.microsoft.com/en-us/azure/architecture/aws-professional/services), reviewed October 21, 2026.

| Responsibility here | AWS implementation | Azure equivalent and difference |
```

**Watch for:** A comparison document is not evidence that an Azure environment was deployed.

### What must an Azure comparison include beyond service names?

Identity permissions, access paths, state, deployment behavior and recovery assumptions.

## Practice and mastery

- Read the Terraform graph from subnet → VPC and instance → role/profile/security group.
- On a machine with Terraform installed, run fmt/validate using the repository’s documented backend-free validation flow. Do not apply infrastructure for this study task.
- Explain one trust condition, one scoped permission and one image digest.
- Proposed production extensions include managed databases/brokers, multi-AZ hosting, TLS entry points, tracing and restore drills; these are not the current single-host topology.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [AWS IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [SSM sessions](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [Project example: Terraform resources, references and plans](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L13-L17)
- [Project example: Security groups and the actual access path](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L30-L36)
- [Project example: IAM roles and GitHub OIDC](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L122-L125)
- [Project example: ECR tags, digests and immutability](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L46-L52)
- [Project example: Secrets Manager and scoped reads](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/aws-dev/main.tf#L90-L98)
- [Project example: State storage, encryption and locking](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/infra/bootstrap/main.tf#L16-L23)
- [Project example: Azure equivalents require a fresh design](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/docs/azure-mapping.md#L1-L5)

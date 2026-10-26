---
title: "AWS and Terraform troubleshooting workbook"
topic: "AWS and Terraform troubleshooting workbook"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 42 · AWS and Terraform troubleshooting workbook

**Prerequisites:** 21–41 and the local Terraform lab.

[Previous: 41](41-aws-ssm-deployment-and-rollback.md) · [Next: 43](43-aws-terraform-capstone-and-interview.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Classify the failure before choosing a fix

Separate syntax/schema, credentials, permissions, network path, resource lifecycle, host bootstrap and application behavior. Record the command, intended account/region, relevant resource address and first meaningful error. A long error output is not a reason to change several unrelated layers at once. Preserve a failing case before repair so you can explain the causal change.

## 2. Use this diagnostic table

| Symptom | First evidence | Next bounded check |
|---|---|---|
| Terraform init cannot find state bucket | Backend config and bucket identity | Distinguish absent bootstrap from wrong bucket region/permission |
| Provider installation fails | Registry/DNS/checksum/version error | Check cache/network and committed lockfile; do not remove trust checks |
| Plan shows instance replacement | Exact replacement-triggering attribute | Review user data/AMI/type and data retention before applying |
| AccessDenied | Effective caller, action and resource | Inspect applicable trust/permission/organization controls |
| Instance missing from SSM | Agent/profile/network readiness | Check bootstrap and endpoint connectivity |
| Tunnel opens, browser fails | Host listener/Compose health | Verify loopback 80 and frontend 8180 routing |
| ECR image pull fails | Registry/account/region/digest | Distinguish login, repository permission and image availability |
| Login works, notifications absent | Inquiry/outbox/broker/consumer state | Trace one stable event identity to a durable notification |
| Rollback image starts but queries fail | Migration compatibility | Prefer a safe roll-forward or verified restore decision |

## 3. Respect the boundary between local and cloud evidence

A mock Terraform plan cannot detect account service-control restrictions, actual AMI availability or SSM connectivity. A local48-check pass cannot prove AWS networking. A successful Terraform apply cannot prove database readiness. When explaining an incident, state which environment was exercised and what evidence remains unavailable.

## 4. Repair one hypothesis at a time

For example, a wrong optional OIDC variable should be fixed by selecting the intended deployment mode, not by weakening the role trust. A source change after plan review needs a new plan, not a reused approval. If a transient download fails, distinguish it from HCL failure and preserve the original error. For state-lock conflicts, identify the real owner before considering force-unlock; an active owner must not be bypassed.

## Walk the real project

[infra/aws-dev/variables.tf · lines 22–31](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/variables.tf#L22-L31)

```hcl
variable "oidc_provider_arn" {
  type        = string
  default     = null
  nullable    = true
  description = "Existing account GitHub OIDC provider ARN; required only for GitHub deployment."
  validation {
    condition     = !var.enable_github_deployment || can(regex("^arn:aws[a-z-]*:iam::[0-9]{12}:oidc-provider/token\\.actions\\.githubusercontent\\.com$", var.oidc_provider_arn))
    error_message = "GitHub deployment requires an existing GitHub OIDC provider ARN. For temporary local login deployment, set enable_github_deployment = false."
  }
}
```

[scripts/aws-release-local.mjs · lines 71–74](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/scripts/aws-release-local.mjs#L71-L74)

```javascript
  requireThat(backendMetadata.backend?.type === 's3' && backendMetadata.backend.config?.key === 'linked-in-node/dev/terraform.tfstate' && backendMetadata.backend.config?.bucket, 'Require initialized isolated AWS dev S3 Terraform state');
  requireThat(execute('terraform', ['-chdir=infra/aws-dev', 'workspace', 'show']).trim() === 'default', 'Require the default workspace with the explicit AWS dev state key');
  const outputs = json('terraform', ['-chdir=infra/aws-dev', 'output', '-json']);
  const value = name => outputs[name]?.value;
```

The variable validation explains a configuration failure before cloud provisioning. The local release helper's backend/account checks explain another class of failure before publication. Source-level guards are useful diagnostic signals; bypassing them would erase the intended environment boundary.

## Practice step by step

1. Choose three rows from the table and write symptom → hypothesis → read-only check → expected observation → next action.
2. Reproduce an invalid variable or mock-test assertion only in the isolated lab/scratch copy; preserve the actual error.
3. Repair one input and rerun the same check without weakening its expected result.
4. Rehearse the incident in 90 seconds, including what the test cannot establish.

**Expected evidence:** Three bounded diagnostic plans and one actual local failed-then-repaired result, with no cloud mutation.

## Check your understanding

### Why not delete `.terraform.lock.hcl` whenever init fails?

It records selected provider versions/checksums. A network or platform issue should be diagnosed directly; unreviewed dependency changes create a new problem.

### Does passing `terraform validate` establish that the account allows creation?

No. Configuration validation is not a live authorization or service-availability test.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)
- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [AWS CLI profiles and settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

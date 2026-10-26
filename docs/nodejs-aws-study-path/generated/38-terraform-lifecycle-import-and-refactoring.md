---
title: "Terraform: lifecycle, import and safe address refactoring"
topic: "Terraform: lifecycle, import and safe address refactoring"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: lifecycle, import and safe address refactoring

Prerequisite: recognize create, update, replacement and no-op actions. This lesson separates an object's remote identity from its Terraform address and explains three different operations: lifecycle control, adopting an existing object, and renaming an already tracked object.

## Address and identity are different

An address such as `terraform_data.release` is how configuration and state refer to a resource. A generated ID identifies its managed instance. In AWS, a subnet ID identifies a real subnet while `aws_subnet.dev` is Terraform's address for it. Renaming the address without telling Terraform about the relationship may look like deleting one managed object and creating another. A refactor therefore needs evidence about identity, not only a prettier source layout.

A moved block records an address migration for something already in state. An import maps an existing remote object into Terraform ownership. Neither is a promise that every other argument already matches the object. A plan remains necessary to discover updates or replacement that the new configuration would request.

## Actual lifecycle protection in bootstrap

[The real state bucket](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/bootstrap/main.tf#L7-L15) declares:

```hcl
variable "state_bucket" { type = string }
resource "aws_s3_bucket" "state" {
  bucket = var.state_bucket
  lifecycle { prevent_destroy = true }
}
resource "aws_s3_bucket_versioning" "state" {
  bucket = aws_s3_bucket.state.id
  versioning_configuration { status = "Enabled" }
}
```

`prevent_destroy` rejects Terraform plans that would destroy the protected object while that lifecycle configuration applies. It is a useful brake for the bucket holding other ownership records. It is not an S3 API deletion prohibition and does not replace account access controls. Removing a resource block also removes its configured lifecycle guard, so deleting code is not a safe way to test protection.

The [release bucket](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L59-L62) instead has `force_destroy = true`, a provider-specific option allowing content removal when that bucket is destroyed. This is not the same feature as Terraform's lifecycle meta-argument. The separate roots give these buckets different purposes and teardown boundaries.

## Other lifecycle choices

`create_before_destroy` can reduce a replacement gap when a resource can coexist with its replacement. It can fail when names must be unique, quotas are exhausted, or consumers cannot switch safely. It is not a universal zero-downtime switch. `ignore_changes` intentionally gives up reconciliation for selected arguments after creation. That can be appropriate under a clearly defined shared-ownership agreement, but it can also hide security drift.

The project's instance explicitly enables replacement on user-data changes through the AWS provider's `user_data_replace_on_change` argument. That is another reminder to read provider-specific arguments alongside Terraform's general lifecycle rules. A short code diff may still replace the only host.

## Runnable practice: a moved block that proves identity

The local lab creates `terraform_data.release`, changes its stored input, forces a replacement through `triggers_replace`, and records the replacement ID. Then its runner rewrites only the copied temporary configuration to rename the resource `terraform_data.artifact`, updates its output reference and appends this practice migration:

```hcl
moved {
  from = terraform_data.release
  to   = terraform_data.artifact
}
```

The runner plans this configuration with the same effective input values used before the rename. Expected result: a `no-op` resource action with `previous_address` identifying the old address. Applying records the move in state and retains the same ID. A further plan returns detailed exit code 0. Merely seeing a new label in the file is weaker evidence than this identity assertion.

The moved plan itself returns detailed exit code 2 because there is a state-address change to record. This is compatible with the resource action being a no-op: state metadata changed while the underlying managed instance did not need replacement.

## Import as a separate operational procedure

Imagine, as a hypothetical extension, an existing release bucket that the team wants Terraform to manage. First establish its owner, account, region, data-retention requirements and whether another state already manages it. Write matching resource configuration and a configuration-driven import using the exact provider-supported ID. Review the resulting plan for unexpected changes. Importing an object twice into competing states creates conflicting ownership rather than redundancy.

This teaching lab does not perform a cloud import. Import is introduced to explain adoption; moved blocks are executed to explain refactoring. An existing OIDC provider in this project's bootstrap story should usually be reused through its ARN when the selected mode needs it, rather than blindly recreated. The default bootstrap switch is false, and selected local-login deployment does not need a deploy OIDC role.

## Checkpoint and answer

**Question:** Does a moved block bring an untracked existing AWS bucket into state? **Answer:** No. It tells Terraform how an already tracked address changed. Import adopts an existing object. After either operation, a plan must still verify that configuration changes do not cause an unintended update or replacement.

## Interview tradeoff and pitfalls

Declarative migration blocks preserve reviewable history and support teammates upgrading through older configurations. Removing them too early can break migration paths for a state that has not yet moved. Prefer a small migration, explicit identity checks and a no-op follow-up plan over a combined rename, provider upgrade and architecture change that obscures cause. Never hand-edit state casually, delete state to solve a rename, or treat force-destroy options as harmless cleanup defaults for valuable data.

Primary references checked 2026-10-26: [lifecycle meta-arguments](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle), [module refactoring and moved blocks](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring), and [import overview](https://developer.hashicorp.com/terraform/language/import). The import scenario is explicitly hypothetical; the lifecycle excerpts and executed local move are concrete evidence.

[Previous lesson](./37-terraform-plan-apply-and-drift.md) · [Next lesson](./39-terraform-validation-and-mocked-tests.md)

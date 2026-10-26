---
title: "Terraform: state, locking and the bootstrap boundary"
topic: "Terraform: state, locking and the bootstrap boundary"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: state, locking and the bootstrap boundary

Prerequisite: explain resource addresses and module ownership. This lesson answers where Terraform remembers object identity, how teammates avoid simultaneous state writes, and how the state bucket exists before an application root can use it.

## State is an ownership record

Configuration says what you want; state binds Terraform addresses to managed object identities and stores attributes needed for future operations. A real VPC does not become a different VPC because you close a terminal. Terraform needs a durable record that `aws_vpc.dev` owns that particular remote ID. Losing the record can make existing infrastructure appear unmanaged; blindly applying from empty state can propose duplicates rather than reconnecting to the objects you intended.

A backend stores state and supplies its coordination behavior. Local state is a file on the machine. The application root uses S3 remote state so its ownership record can persist beyond one laptop. An S3 backend does not itself create an S3 bucket: initialization needs an existing bucket and access to its configured key.

## Actual bootstrap configuration

[The project bootstrap](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/bootstrap/main.tf#L1-L15) begins:

```hcl
terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 6.0" } }
}
provider "aws" { region = var.region }
variable "region" { default = "us-east-1" }
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

Notice the absence of a remote backend block. This bootstrap root initially keeps its own state locally. Its state file must be protected and retained; creating a remote bucket does not automatically move bootstrap's ownership record into it. The application root is a separate configuration with a separate state boundary. Never describe the bucket as magically managing its own original state.

The remainder of bootstrap enables AES256 encryption, blocks all four public-access mechanisms and [denies insecure transport](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/bootstrap/main.tf#L16-L35). It optionally creates the account GitHub OIDC provider only when explicitly enabled; the default is false. These controls are actual source, whereas a later backend migration is an operational design step requiring its own reviewed procedure.

## Partial backend configuration and locking

[The application backend example](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/backend.hcl.example#L1-L5) contains:

```hcl
bucket       = "YOUR-ACCOUNT-linked-in-terraform-state"
key          = "linked-in-node/dev/terraform.tfstate"
region       = "us-east-1"
encrypt      = true
use_lockfile = true
```

Bucket and key locate the state object. Region locates that bucket, independently of the application's AWS provider region. Encryption protects storage; lock-file coordination protects against conflicting Terraform operations. Native S3 lock-file support requires Terraform 1.10 or newer, matching the project's minimum. A lock is not a backup and does not prevent somebody from changing resources in the AWS console.

The S3 writer lock uses an object named `<state-key>.tflock`, so this example uses `linked-in-node/dev/terraform.tfstate.tflock`. In the default workspace, backend access needs bucket listing plus GetObject/PutObject on the state object, and GetObject/PutObject/DeleteObject on the lock object. Deleting the lock releases coordination; the state object does not normally need DeleteObject for routine operations. These are backend permissions, separate from application permissions. The `.terraform.lock.hcl` dependency selection file and the remote `.tflock` writer lock solve different problems. See the [official permission breakdown](https://developer.hashicorp.com/terraform/language/backend/s3#permissions-required).

During an operation that needs state locking, Terraform requests the backend lock, works with the state and releases the lock. A second writer should wait or fail with a lock diagnostic rather than overwrite concurrent work. Lock permissions are part of the backend access design. Do not force-unlock merely because a colleague's operation takes longer than expected; establish whether the owning process still runs and who owns recovery.

## Sensitive state and recovery

State can contain sensitive values even when their ordinary CLI display is redacted. Saved plans can also include sensitive configuration and values. Keep state, plans and credentials out of Git and out of public lesson screenshots. The source's secret ARN output identifies a secret rather than containing its runtime value, but that is not a general guarantee that all Terraform state is harmless.

Versioning gives an operator a way to recover older state-object versions after mistakes. It is not automatic permission to restore any old state: the cloud may already have changed since that version was recorded. Recovery must reconcile the ownership record with actual objects and current configuration. Encryption, access restriction, locking and backup/version recovery solve different failure modes.

## Local practice and predictable outcome

Run the built-in-provider lab and inspect its runner. It uses a brand-new temporary directory, local state and no backend block. After the first apply it records a generated resource identity, after a replacement it verifies a different identity, and after a moved block it verifies identity is preserved. At cleanup, `terraform state list` returns no addresses.

For a paper exercise, label the project buckets by responsibility: the bootstrap state bucket stores Terraform state; the application's release bucket stores release artifacts. The release bucket's `force_destroy = true` does not make the state bucket disposable. The state bucket has `prevent_destroy`; application destruction should not implicitly destroy the separate bootstrap root's bucket.

## Checkpoint and answer

### Recall: Does `sensitive = true` on an output remove its value from state, and does a lock recover a deleted state object?

**Answer:** No to both. Sensitivity controls normal display, while state requires storage protection. Locking coordinates writers; versioning and a tested recovery procedure address recovery.

## Interview tradeoff and pitfalls

Separating bootstrap from application state reduces accidental coupling but adds another ownership record to protect. Remote state enables collaboration but needs access control, service availability and recovery practice. Treat `prevent_destroy` as a useful planning guard while its configuration remains present, not an account-wide deletion policy. Avoid merging unrelated environments into one key, assuming provider credentials configure the backend, or mixing application cleanup with state-storage deletion.

## References

Official sources checked on 2026-10-26.

- [S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)
- [sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
- [lifecycle rules](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)


[Previous lesson](./35-terraform-graph-loops-and-modules.md) · [Next lesson](./37-terraform-plan-apply-and-drift.md)

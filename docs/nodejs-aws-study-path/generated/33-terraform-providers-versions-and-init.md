---
title: "Terraform: providers, version constraints and init"
topic: "Terraform: providers, version constraints and init"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: providers, version constraints and init

Prerequisite: complete the local lab in lesson 32. The goal now is to distinguish the Terraform program, the AWS plugin, the backend and the lock file. These are separate components, and confusing them makes initialization failures hard to diagnose.

## The four components

Terraform Core reads configuration, builds dependencies and coordinates operations. A provider is a plugin that supplies resource schemas and interacts with a target API. The AWS provider understands `aws_instance` and `aws_s3_bucket`. A backend decides where Terraform keeps state and how it coordinates access. The S3 backend is built into Terraform; it is not an `aws_s3_bucket` resource and does not use the provider block as its configuration. A dependency lock file records chosen external provider versions and checksums so teammates can reproduce those selections.

The application's backend and AWS resources can use different regions and access permissions. The backend must be available before normal resource operations begin. This explains why provider configuration cannot create the very backend needed to initialize that same root configuration.

## Read the actual constraints

[The project's entire versions file](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/versions.tf#L1-L11) contains:

```hcl
terraform {
  required_version = ">= 1.10, < 2.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 6.0" }
  }
  backend "s3" {}
}
provider "aws" {
  region = var.region
  default_tags { tags = { Project = var.project, Environment = "dev", ManagedBy = "Terraform" } }
}
```

`required_version` restricts the Terraform executable. `required_providers` declares the plugin source and acceptable versions. `~> 6.0` accepts compatible 6.x versions below 7.0; it does not mean exactly 6.0.0. By contrast, a constraint `~> 6.0.0` would limit the selection to 6.0 patch releases. The provider block supplies runtime configuration such as region and default tags. It does not select the plugin version.

The empty S3 backend block intentionally leaves environment-specific values for initialization. [The backend example](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/backend.hcl.example#L1-L5) supplies bucket, key, backend region, encryption and `use_lockfile = true`. It contains a placeholder bucket name, so copying it is preparation rather than proof that a real state bucket exists.

## What init actually prepares

Initialization reads backend settings, installs referenced modules where necessary, and selects and installs external providers using constraints and existing lock selections. Re-running init is normal after changing these settings. Initialization does not mean an application's resources have been deployed. It can nevertheless contact remote services when a remote backend is configured, so it is not universally an offline operation.

The `.terraform` directory is working data and downloaded tooling. The `.terraform.lock.hcl` file is reviewable dependency selection metadata and normally belongs in source control. State and saved plans need separate protection. Deleting a dependency lock file to fix every error trades a visible diagnostic for an unreviewed selection change.

The local lab needs no external plugin installation because `terraform_data` is built in. It runs `init -backend=false` in an isolated directory with no backend block. This deliberately avoids S3 access while teaching initialization mechanics. A mocked AWS test still needs the AWS plugin's schema available; mocking does not turn an external provider into a built-in provider.

## Predictable local practice

Run the lesson 32 runner again and inspect its `init` output. Expect a message identifying the built-in provider rather than an AWS download. Read its `required_version` declaration and compare that to `terraform version`. Then answer whether installing an AWS CLI would change Terraform's provider constraint. It would not: the CLI and provider are separate executables.

For a paper exercise, choose from versions 6.0.3, 6.69.1 and 7.0.0. The project's `~> 6.0` permits the first two and rejects 7.0.0. If a committed lock file already selects 6.0.3, a normal init should retain that compatible selection rather than silently upgrading to the newest acceptable release. An intentional `init -upgrade` is a dependency change requiring its own plan review and test evidence.

## Troubleshoot in dependency order

If initialization fails, first identify whether the message names Terraform's version, provider installation or backend access. A version constraint failure is not solved by AWS credentials. A backend bucket access failure is not solved by editing a resource's IAM policy before initialization. A provider registry network failure is not proof that the AWS account is misconfigured. Keep the original diagnostic and repair the component it identifies.

## Checkpoint and answer

**Question:** Does `provider "aws" { region = var.region }` set the S3 state bucket's region? **Answer:** No. The backend receives its own initialization configuration. The resource provider uses `var.region`; the backend example separately specifies its own region. Changing an application input does not migrate a backend or relocate an existing state bucket.

## Interview tradeoff and pitfalls

Broader compatible version ranges admit fixes without editing every module, while committed lock selections make actual runs reproducible. Strict pinning can simplify controlled upgrades but also postpones fixes unless someone maintains it. Explain both the constraint and the selected version before claiming reproducibility. Avoid committing `.terraform`, treating lock files as state backups, putting credentials in backend examples, or running init against a live backend during an exercise intended to be offline.

Primary references, checked 2026-10-26: [dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock), [S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3), and [validation initialization requirements](https://developer.hashicorp.com/terraform/cli/commands/validate). The inspected project declares Terraform 1.10 or newer because native S3 lock-file configuration is part of its intended backend setup.

[Previous lesson](./32-terraform-hcl-and-first-local-lab.md) · [Next lesson](./34-terraform-inputs-locals-and-outputs.md)

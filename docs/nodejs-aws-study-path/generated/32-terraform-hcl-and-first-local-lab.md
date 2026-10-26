---
title: "Terraform: HCL and your first local lab"
topic: "Terraform: HCL and your first local lab"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: HCL and your first local lab

Prerequisite: finish the AWS design tradeoffs lesson. You need a terminal, Python 3 and an already installed Terraform version at least 1.10 and below 2.0. You do not need an AWS account for this lesson. The first goal is to understand a configuration before learning cloud authentication.

## What Terraform and HCL mean

Infrastructure as code means recording desired infrastructure in reviewable files. Terraform is a tool that evaluates those files, compares them with tracked objects and proposes changes. HCL is its configuration language. A resource block describes something Terraform manages; its type identifies the implementation and its second label gives that object a local name. A resource address combines those labels, such as `aws_subnet.dev`. An address is Terraform's name for an object; the cloud provider assigns the actual subnet ID.

A block has a type, optional labels and a body in braces. An argument assigns a value with `=`. Strings use quotes, booleans use `true` or `false`, and collections group values. Expressions calculate values or reference other blocks. Files ending in `.tf` in the same directory belong to one module: splitting a file into `variables.tf` and `main.tf` helps people read it, but does not establish execution order.

## Read actual project HCL

Open [the project's subnet declaration](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L13-L17). This is an exact source excerpt, not a command to provision it:

```hcl
resource "aws_subnet" "dev" {
  vpc_id                  = aws_vpc.dev.id
  cidr_block              = "10.84.1.0/24"
  map_public_ip_on_launch = true
}
```

Read one line at a time. `aws_subnet` identifies a resource type from the AWS provider. `dev` is its Terraform label. The VPC reference takes the ID of another managed object. The CIDR string selects the subnet's address range. The boolean allows public IP assignment on launch. None of these lines says to open port 8180. The project's [security group](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L30-L41) has empty ingress, and its description explicitly names SSM management and tunneled browser traffic. Learn to distinguish a resource declaration from the complete system behavior it participates in.

## What happens from text to local state

The local teaching configuration uses `terraform_data`, a resource implemented by Terraform's built-in provider. It stores a value with a resource identity and participates in plans and lifecycle changes. It does not create a VM, bucket, file or AWS object. This is a practice extension; it is not a claim that the real application uses `terraform_data`.

First Terraform reads the files and checks language rules. Initialization prepares the working directory. Validation checks the configuration. A plan compares desired values and state. Applying the reviewed local plan records the resource and its identity in local state. A second plan with unchanged inputs should report no changes. This sequence separates syntax, preparation, prediction and mutation so that each has a clear purpose.

## Runnable practice: a complete safe first cycle

From the repository root run:

```sh
python3 docs/nodejs-aws-study-path/labs/terraform-local/run.py
```

Read [the lab source](../labs/terraform-local/main.tf), [its runner](../labs/terraform-local/run.py) and [the walkthrough](../labs/terraform-local/README.md). The runner creates a new temporary directory, copies only the teaching configuration and tests, and uses no AWS provider. It validates, plans, applies, checks idempotency, changes an input, proves replacement, preserves identity through a moved block, runs three configuration tests, destroys the local objects and verifies empty state. Its temporary directory is removed even after failure. The automatic approval flag appears only in this bounded built-in-resource cleanup.

Expected outcome: every printed command has `PASS`, including a first plan with exit code 2 and an unchanged plan with exit code 0. Exit code 2 is deliberately expected when `-detailed-exitcode` reports proposed changes. No AWS credentials are read and no cloud bill is created. Stop and read the diagnostic if your installed version fails the declared version constraint; the runner does not install tools for you.

## Practice slowly before moving on

Without executing cloud files, annotate the subnet excerpt with block type, resource type, label, argument and reference. Then open the local lab and predict its initial output name from the default project input and local expression. Finally read the initial plan output and locate `+ create`, the resource address and attributes known only after apply. The predicted name is `marketplace-local`; the generated resource ID is not a name you should hardcode.

## Checkpoint and answer

**Question:** If `variables.tf` sorts after `main.tf`, does Terraform create the resource before reading its variable declaration? **Answer:** No. Terraform loads the module configuration as a whole and evaluates references. File names organize people, while dependencies organize work. Moving declarations between files does not itself move resources between states.

## Interview tradeoff and common pitfalls

A useful junior explanation identifies the desired object. A senior explanation also identifies ownership, dependencies, state, review and recovery. Declarative code makes repeated execution predictable when configuration, observations and provider behavior agree; it does not remove failures or make every apply transactional. Avoid treating Terraform as a shell script, assuming a public subnet is an open firewall, or copying an AWS apply command just to understand syntax. The local lab builds mechanical confidence before any cloud action is considered.

Primary references, checked 2026-10-26: [HashiCorp types and values](https://developer.hashicorp.com/terraform/language/expressions/types), [references](https://developer.hashicorp.com/terraform/language/expressions/references), and [terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data). Read these alongside the project excerpt, because language rules and the project's design choices answer different questions.

[Previous lesson](./31-aws-production-design-tradeoffs.md) · [Next lesson](./33-terraform-providers-versions-and-init.md)

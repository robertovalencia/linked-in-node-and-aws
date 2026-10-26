---
title: "Terraform: inputs, locals and output contracts"
topic: "Terraform: inputs, locals and output contracts"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: inputs, locals and output contracts

Prerequisite: distinguish provider configuration from backend configuration. This lesson follows a value from the caller, through a derived expression, into a resource and back out through an output. That path explains most everyday Terraform configuration without memorizing a large language reference.

## Inputs are a module's arguments

An input variable lets a caller supply a value. A type constrains its shape, a default supplies an omitted value, and validation rejects values that violate the module's contract. A variable is not mutable storage like a JavaScript `let`. Expressions refer to it as `var.name`. A local value gives a reusable name to a derived expression, such as a common resource prefix. Outputs expose selected values after evaluation so people and automation can consume a defined interface.

The distinction is useful when designing a module: callers choose inputs, authors compute locals, and consumers rely on outputs. Exposing every implementation detail as a variable increases complexity. Hardcoding every value makes reuse awkward. Start with meaningful decisions and keep derivable values internal.

## Read project validation carefully

[The actual project input](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/variables.tf#L1-L8) is:

```hcl
variable "region" { default = "us-east-1" }
variable "project" {
  default = "linked-in-node"
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,24}$", var.project))
    error_message = "Use a short lowercase project slug."
  }
}
```

The project slug must start with a lowercase letter followed by 2–24 lowercase letters, digits or hyphens. Anchors constrain the whole string. `regex` can fail when it finds no match; `can` converts that evaluation success or failure into a boolean for validation. The diagnostic tells the caller what to change. This contract catches bad names before attempting AWS resource creation, but it does not guarantee every AWS naming requirement in every service.

The [locals declaration](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L1-L7) derives `name = "${var.project}-dev"` and an ARN prefix from the current partition. This interpolation inserts a value into a string. Resources reference `local.name`, keeping the naming expression consistent. It is not a second independently configurable input.

## Defaults versus the selected deployment

Defaults do not tell you which values a particular deployment uses. [The selected local-login example](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/dev-local.tfvars.example#L1-L7) sets `region = "us-east-2"`, `enable_github_deployment = false` and `instance_type = "m7i-flex.large"`. In contrast, [the variable declarations](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/variables.tf#L17-L36) default the GitHub switch to true and region elsewhere to us-east-1. Read the selected variable file before describing a deployment.

The GitHub repository variable is still a declared input in local mode. Its existence does not prove the GitHub deployment role is created. The boolean governs that branch, and OIDC validation permits a missing provider ARN when the branch is disabled. Explain the entire condition rather than equating a variable name with active behavior.

## Follow the output contract

[The actual outputs](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/outputs.tf#L1-L10) expose instance ID, secret ARN, release bucket, repository URLs, deployment account and region. `deploy_role_arn` uses `try(aws_iam_role.deploy[0].arn, null)`: the indexed role is absent when the feature is disabled, and the output becomes null. A null output conveys absence; it is not an empty string with an accidental meaning.

A secret ARN identifies a secret; it is not the runtime secret value. Marking an output `sensitive` suppresses ordinary display of a value but does not encrypt it out of state. Treat state and saved plans as potentially sensitive. Do not add passwords to this teaching lab just to demonstrate output formatting.

## Local practice with an observable result

Open the local lab's `main.tf`. Its project input defaults to `marketplace`, its local appends `-local`, and the output comes from the managed resource's stored value. Run the runner and find the `custom_input` test. It supplies `catalog` and `v2`; the expected output is a name of `catalog-local` and release `v2`.

Next inspect the `invalid_project` test. It deliberately supplies `Invalid Project` and expects the project variable validation to fail. That expected failure is a passing negative test: accepting the invalid input would fail the test. As a paper exercise, predict outcomes for `app`, `a`, `A-good` and `catalog-2`. The first and last pass the naming expression; `a` is too short and the uppercase initial fails the expression.

## Checkpoint and answer

**Question:** If the selected tfvars example says us-east-2, but the variable default says us-east-1, which describes that selected configuration? **Answer:** The supplied us-east-2 value overrides the default. It does not override the S3 backend region, because backend initialization has a separate configuration channel.

## Interview tradeoff and pitfalls

Strong contracts shorten feedback loops and make automation predictable. Excessively elaborate validation can reproduce a provider imperfectly and become harder to maintain than the problem it prevents. Validate decisions your module owns, give useful messages, and let the provider validate its full API schema. Avoid using `try` to hide every error: here it models one intentional optional resource. Review the difference between an absent feature, a malformed required input and a failed remote API request before choosing a fallback.

Primary references, checked 2026-10-26: [input variables](https://developer.hashicorp.com/terraform/language/values/variables), [local values](https://developer.hashicorp.com/terraform/language/values/locals), and [value references](https://developer.hashicorp.com/terraform/language/expressions/references). The examples above explain this repository's selected values rather than promising that a default instance type has universal pricing or eligibility.

[Previous lesson](./33-terraform-providers-versions-and-init.md) · [Next lesson](./35-terraform-graph-loops-and-modules.md)

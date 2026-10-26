---
title: "Terraform: validation, mocked tests and evidence limits"
topic: "Terraform: validation, mocked tests and evidence limits"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: validation, mocked tests and evidence limits

Prerequisite: complete the plan and lifecycle lab. This final Terraform lesson separates formatting, schema validation, configuration assertions and real cloud behavior. The goal is to know what a green check proves and what additional evidence a deployment still needs.

## Build a ladder of checks

Formatting makes a configuration consistent to read. `terraform fmt -check` reports formatting differences; it does not prove correctness. `terraform validate` checks configuration structure and internal consistency with initialized provider schemas; it does not prove a real account grants access, a region has capacity, or an application can start. A plan evaluates proposed behavior with supplied inputs and provider observations. Terraform tests add assertions and expected failures for configuration behavior.

A test can use real providers, so `terraform test` is not automatically harmless. Read the test's provider selection and commands before running it. A mocked provider substitutes synthetic behavior for provider operations, enabling logic checks without AWS API calls. Its schema still comes from the installed AWS plugin. A mock cannot demonstrate IAM permissions, actual EC2 compatibility, network reachability, billing eligibility or successful container startup.

## Read the actual mocked test

[The project's AWS test file](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/tests/security.tftest.hcl#L1-L25) begins:

```hcl
mock_provider "aws" {
  mock_data "aws_partition" {
    defaults = { partition = "aws" }
  }
  mock_data "aws_caller_identity" {
    defaults = { account_id = "123456789012" }
  }
  mock_data "aws_ssm_parameter" {
    defaults = { value = "ami-0123456789abcdef0" }
  }
}
```

Those values are deliberate test fixtures. The example account and AMI are not evidence of the actual deployment account or an AMI that was launched. Controlled fixtures make assertions predictable, especially when configuration assembles ARNs or chooses an AMI from a data source. Randomly generated computed values would make some assertions harder to interpret.

## Five application runs and two bootstrap runs

The application test file contains exactly five `run` blocks. `private_management` checks no ingress, IMDSv2, disk encryption, restricted GitHub trust and immutable image tags. `free_plan_demo_instance` checks the configured default instance type, absence of T-family credit options and the bounded root disk. `burstable_without_surplus_charges` supplies t3.medium and checks standard CPU credits. `temporary_local_login_deployment` supplies us-east-2, disables GitHub deployment and checks that deploy-role resources disappear while host SSM access and no-ingress controls remain. `github_mode_requires_oidc_provider` expects validation failure when GitHub mode lacks an OIDC provider ARN.

Open [the local-login and expected-failure cases](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/tests/security.tftest.hcl#L61-L89) to verify that branch behavior directly. A test label containing “free plan” verifies declared configuration, not current account pricing or free-plan eligibility. Avoid converting a source test name into a financial promise.

The separate [bootstrap test file](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/bootstrap/tests/security.tftest.hcl#L1-L36) has exactly two runs. The first uses a mocked apply so computed bucket ARNs become available, and asserts versioning, encryption, public-access blocking, default OIDC omission and denial of insecure transport. The second plans with OIDC creation explicitly enabled and checks the intended issuer and STS audience. An apply command inside a wholly mocked provider test does not create an AWS bucket.

## Local configuration practice

Run the credential-free lab runner. Its own three tests use the built-in resource rather than an AWS mock: `default_contract`, `custom_input` and `invalid_project`. The first two apply only local `terraform_data` test state and assert outputs. The third expects the invalid project input to fail validation. Terraform tests use their own test state and perform teardown; they do not intentionally reuse the runner's normal working state.

Expected outcome is three passed local test runs plus the runner's plan, update, replacement, moved-address and cleanup assertions. To inspect a negative test, read `expect_failures = [var.project]`. It names the exact validation expected to reject the input. If the input unexpectedly succeeds, the test fails; this prevents a missing validation rule from looking like success.

## Evidence from this study update

The credential-free runner was executed with Terraform 1.17.0. Its first plan, unchanged plan, in-place update, forced replacement, identity-preserving move, three configuration tests and empty-state cleanup all passed. The source's AWS tests were also executed from isolated temporary copies using the installed locked AWS provider schema, with the application S3 backend removed in that copy so no backend access was required. The result was five application runs and two bootstrap runs passing. These are local and mocked observations, not a claim that cloud resources were provisioned or an AWS integration passed.

## Checkpoint and answer

### Recall: Does a successful mocked assertion that the security group's ingress is empty prove an SSM tunnel will connect?

**Answer:** No. It verifies a configuration property. Real SSM connectivity also needs a healthy agent, credentials, network access, instance registration and caller permissions. Each belongs to later authorized integration evidence.

## Interview tradeoff and pitfalls

Fast mocked tests catch regression in branching, names, policy construction and resource arguments. Real account integration checks catch service behavior and permission errors that mocks cannot simulate faithfully. A sound delivery process uses each at its appropriate boundary. Do not run uninspected tests against production, count mock assertions as deployment verification, weaken a failing assertion to claim success, or infer resource availability from a fixture AMI. Name the observed check, its result and its limit.

## References

Official sources checked on 2026-10-26.

- [validate command](https://developer.hashicorp.com/terraform/cli/commands/validate)
- [Terraform tests](https://developer.hashicorp.com/terraform/language/tests)
- [provider mocking](https://developer.hashicorp.com/terraform/language/tests/mocking)


[Previous lesson](./38-terraform-lifecycle-import-and-refactoring.md) · [Next lesson](./40-aws-release-pipeline-and-oidc.md)

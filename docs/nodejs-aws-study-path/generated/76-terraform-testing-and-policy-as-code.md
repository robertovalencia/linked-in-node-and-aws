---
title: "Terraform testing and policy as code"
topic: "Terraform testing and policy as code"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New credential-free practice extension; Project code comparison
---

# Terraform testing and policy as code

Prerequisite: lesson 75 and the original testing lesson 39. A useful verification system asks several different questions: can Terraform read the files, does the configuration satisfy its declared interface, does it propose an acceptable change, and does the resulting system behave correctly? No single green command answers all of them.

This lesson extends the local exercise with child contracts and failure expectations. It also introduces organization policy as a design option. It does not claim that OPA, Sentinel or a new security scanner is installed in the project.

## Step 1: match each check to a question

`terraform fmt -check` checks canonical formatting. `terraform validate` checks configuration consistency using available module and provider schemas after initialization. A plan evaluates a particular root with selected inputs, state and observations. Terraform tests run scenarios with assertions. Static analysis examines source or plan representations for selected patterns. Integration tests check actual external behavior with authorized resources.

A variable validation is an input contract. A precondition guards an assumption needed for an operation. A postcondition checks a resulting object's properties and can prevent dependent work when it fails. A `check` block evaluates a broader assertion; in ordinary plan/apply operation its failure produces a warning rather than the blocking semantics of a precondition. These are not interchangeable severity settings. The [validation guide](https://developer.hashicorp.com/terraform/language/validate) explains how to choose among them.

When a condition depends on a computed value, Terraform may defer evaluation until that value is known. A successful plan cannot prove an apply-time condition has already passed. The review should identify deferred checks and how their failures affect later operations.

## Step 2: understand test execution authority

`terraform test` can run real provider operations and create real infrastructure. An apply run is not intrinsically credential-free. Inspect the configuration, providers, run commands and overrides before executing an unfamiliar test suite. Test teardown attempts to clean up its resources, but failure can leave objects requiring manual attention. An automatic cleanup intention is not a guarantee that a cloud account will contain nothing afterward.

Mock providers replace provider operation behavior with synthetic results while retaining schema information from the installed plugin. That makes them useful for evaluating configuration branching and constructed values. A mock cannot prove a real account permits an action, a service accepts a combination, a network path works, or an application is ready. [Provider mocking](https://developer.hashicorp.com/terraform/language/tests/mocking) documents its behavior and fixture controls.

The project's [pinned AWS tests](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/tests/security.tftest.hcl) supply a concrete comparison. Read their mock declarations and assertions as configuration evidence. The new advanced lab instead uses the built-in `terraform_data` resource, so its apply tests manage synthetic local state without an AWS plugin or AWS API.

## Step 3: write a meaningful failure expectation

The advanced lab has five runs: default contract, explicit-null optional default, normalized child owner, invalid tier rejection and an observable empty-inventory check. The invalid-tier run names `var.services` in `expect_failures`. That is stronger than merely accepting any error: the intended input rule must reject the value. A syntax error or unrelated provider failure should not be counted as successful validation coverage.

The check-warning test uses `expect_failures = [check.at_least_one_service]`. Terraform's test harness treats expected check outcomes as test evidence. This does not turn the same check into a hard gate in a normal apply. Explain the difference when presenting results.

An initial execution exposed an important fixture mistake: the runner's scenario auto-variable file supplied an extra service to the default test. The test correctly failed. The repair explicitly supplies its intended inventory in that test run. The assertion was preserved. This is the right response to a failing test: establish which input contract the scenario is meant to exercise, fix unintended coupling, then rerun and retain the failure record when it explains the change.

## Step 4: separate linting, security rules and policy

TFLint is a Terraform linter with extensible rules and provider-specific plugins. It can identify selected errors or conventions that language validation misses. It does not provide a complete security proof. A static application security testing tool, or SAST tool, analyzes code or configuration for configured risk patterns; its findings need interpretation and its coverage depends on the enabled rules. A clean scan means those rules found no reported issues in the analyzed input.

Policy as code expresses organizational decisions in an executable policy language. For example, a proposed policy could reject an unapproved public exposure or require ownership metadata. OPA can evaluate Terraform plan JSON with Rego. Sentinel is a separate policy language and ecosystem. HCP Terraform has managed policy enforcement features, but availability depends on the organization's product edition and entitlement. Do not assume installing Terraform CLI includes a managed Sentinel or OPA enforcement service. Check current licensing and feature availability before designing a required gate. [HCP policy documentation](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement) describes the integration.

A policy must handle unknown values explicitly. Plan JSON can distinguish values not yet known from known nulls; interpreting every missing field as safe can silently allow the riskiest changes. Test policies with allowed, denied and unknown fixtures, and define whether uncertain decisions block, require review or defer to another control. The [OPA Terraform guide](https://www.openpolicyagent.org/docs/terraform) discusses plan-time limitations.

## Practice and expected results

Run the advanced lab and read its five test results alongside the runner's eleven assertions. Then write a proposed policy decision in plain language and design three fixtures: pass, fail and unknown. No policy engine installation is necessary for this exercise. Expected evidence is a clear account of what is locally executed and what remains a design specification.

### Recall: Does a mocked apply prove the cloud deployment succeeds?

**Answer:** No. It exercises configuration logic against synthetic provider behavior. Real authorization, service semantics, networking and application health require separate authorized integration evidence.

## References

Official sources checked on 2026-10-27; the local suite passed with Terraform 1.17.0.

- [Validation mechanisms](https://developer.hashicorp.com/terraform/language/validate)
- [Terraform test scenarios](https://developer.hashicorp.com/terraform/language/tests)
- [Provider mocking](https://developer.hashicorp.com/terraform/language/tests/mocking)
- [TFLint project documentation](https://github.com/terraform-linters/tflint)
- [OPA Terraform policy](https://www.openpolicyagent.org/docs/terraform)
- [Managed policy enforcement](https://developer.hashicorp.com/terraform/cloud-docs/policy-enforcement)

[Previous lesson](./75-terraform-import-moves-and-provider-upgrades.md) · [Next lesson](./77-terraform-team-ci-and-approval-workflows.md)

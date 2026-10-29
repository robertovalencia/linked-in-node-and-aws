---
title: "Terraform: plans, apply, drift and review"
topic: "Terraform: plans, apply, drift and review"
last_researched: 2026-10-26
source_labels: Project code; Terraform mechanics; Credential-free practice extension
---

# Terraform: plans, apply, drift and review

Prerequisite: explain where state lives and why it matters. This lesson teaches how to read a proposed change and distinguish a new configuration change from a change that happened outside Terraform. The aim is a reviewable decision rather than a ritual sequence of commands.

## Three views of infrastructure

Terraform reasons about configuration, state and provider observations. Configuration records desired arguments. State records bindings and previous attributes. Refresh reads current remote objects through the provider. A normal plan uses these views to propose actions that bring managed objects toward the configuration.

Drift means a managed object changed outside the recorded Terraform workflow, such as someone changing an instance setting in a console. A new desired setting in Git is a configuration change. Both may produce a plan, but their cause and appropriate response differ. Decide whether to restore the declared design or adopt the external change deliberately; do not automatically accept whichever value happened most recently.

## Read a real replacement trigger

The [project instance definition](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L117-L126) includes:

```hcl
  # CPU-credit options apply only to burstable T instances. Non-T families
  # such as m7i-flex must omit the API field entirely.
  dynamic "credit_specification" {
    for_each = can(regex("^t[0-9]", var.instance_type)) ? [1] : []
    content { cpu_credits = "standard" }
  }
  user_data                   = file("${path.module}/user-data.sh")
  user_data_replace_on_change = true
  tags                        = { Name = local.name }
```

Changing the user-data file changes the expression's value. With this explicit setting, that change requests instance replacement. A reviewer should connect a small script diff to the possible operational effect on the single-host demo. A plan's risk depends on what is being replaced and where application data lives, not only on the number of lines changed.

The project has one EC2 instance and [a 40 GiB encrypted root disk that deletes on termination](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/main.tf#L100-L116). Do not infer production high availability or durable external database storage from a passing Terraform plan. That storage and availability decision belongs in a separate architecture discussion before replacement is approved.

## What a plan tells you

Creation, in-place update, deletion and replacement are different actions. Replacement contains a delete and a create; its ordering may be affected by lifecycle settings. Attributes can be unknown until apply when a provider must allocate or discover them. Unknown is not the same as null, empty or a failed value.

An unsaved plan is a preview. A saved plan captures a proposed operation that can be reviewed and later applied as that artifact. A saved plan can become stale when state changes, and its sensitive contents need protection. An apply can partially complete before failing; Terraform is not a transaction that rolls back every successful API operation automatically. Read diagnostics and generate a fresh understanding before retrying.

For the cloud project, the working agreement requires approval of a concrete saved plan and current cost estimate before cloud provisioning. This lesson does not give a cloud apply command. Local built-in-resource operations are a separate practice exercise with no AWS objects.

## Runnable practice: compare four plans

Run the local lab. First, its initial plan reports `create` and detailed exit code 2. Applying the saved local plan records one resource. Second, the same inputs produce exit code 0, proving idempotency. Third, changing `release` to v2 updates `input` in place. Fourth, changing `generation` to 2 changes `triggers_replace`, producing delete/create actions and a new resource identity.

The runner parses `terraform show -json` and asserts these action lists, so a success message is tied to observed behavior. Exit code 1 is an error, 0 means no differences with `-detailed-exitcode`, and 2 means differences are present. A generic shell script that treats every nonzero code as failure must explicitly handle this documented contract.

The built-in resource has no external API object for another person to edit. Therefore this lab proves change planning and lifecycle transitions, not real AWS drift detection. For a drift exercise without cloud access, explain on paper what a normal plan should compare if a console operator changed a security-group rule. In this project an unexpected inbound rule would conflict with the declared empty ingress and deserves immediate review.

## Checkpoint and answer

### Recall: A plan says one resource will change. Is that enough information to approve it?

**Answer:** No. Read the address, action type, changed arguments, dependencies and data/recovery implications. Replacing the only compute host can be more consequential than creating several independent metadata objects. A no-op plan also does not prove the application is healthy.

## Interview tradeoff and pitfalls

A normal plan evaluates desired convergence. A refresh-only plan is useful when deliberately reviewing how observations should update state, but it does not itself propose configuration convergence. `-refresh=false` skips normal observation and can miss drift; use it only when its reduced evidence is understood. Routine resource targeting can hide dependencies and incomplete changes, so it is a recovery tool rather than a default deployment strategy.

A senior review explains cause, effect, downtime, rollback limits and the evidence needed after apply. Avoid assuming plan means authorization, confusing a provider observation with an input value, publishing saved plans as ordinary text artifacts, or treating a failed apply as if nothing happened. Preserve the diagnostic and examine the next plan carefully.

## References

Official sources checked on 2026-10-26.

- [HashiCorp plan command](https://developer.hashicorp.com/terraform/cli/commands/plan)


[Previous lesson](./36-terraform-state-locking-and-bootstrap.md) · [Next lesson](./38-terraform-lifecycle-import-and-refactoring.md)


## Type the commands and inspect the result

The [local command workbook](../walkthroughs/09-terraform-local-commands.md) walks through a runnable isolated configuration from initialization to cleanup. The separate [AWS command workflow](../walkthroughs/10-terraform-aws-commands.md) explains owner/state/input prerequisites, protected saved plans, approval and later apply; it is not a cloud deployment authorization.

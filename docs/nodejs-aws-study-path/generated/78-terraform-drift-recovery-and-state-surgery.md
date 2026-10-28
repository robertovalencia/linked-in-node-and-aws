---
title: "Terraform drift recovery and state surgery"
topic: "Terraform drift recovery and state surgery"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New recovery tabletop; New credential-free practice extension
---

# Terraform drift recovery and state surgery

Prerequisite: state, migrations and team workflows. Drift means an observed managed object differs from Terraform's recorded or desired view because something changed outside the expected workflow. Recovery means restoring a trustworthy relationship among configuration, state and real objects. “State surgery” is an informal name for exceptional changes to those ownership records; it should be a diagnosis-driven operation with a recovery path.

This lesson does not alter the project's state or cloud resources. The runnable extension demonstrates local snapshot inspection and a no-change refresh-only plan. Its remaining incidents are explicitly proposed tabletop exercises.

## Step 1: determine which view is wrong

Configuration expresses desired behavior. State records Terraform's known bindings and observations. The provider reads the actual service. An incident can involve any of them: an operator changed a firewall, a resource was deleted outside Terraform, a module rename omitted its migration, or a process created an object before failing to save state. Those failures require different repairs.

Start by establishing the intended account, region, root, backend key and workspace. A wrong environment can look like missing resources. Freeze competing writes while investigating. Preserve diagnostics and obtain a protected current snapshot before mutating ownership. Record source and tool versions so a later operator can reproduce the interpretation rather than guessing from a screenshot.

Do not assume a failed apply rolled everything back. Terraform coordinates many provider operations without a global transaction. Some changes may have succeeded. A subsequent plan uses current observations and state to propose the next reconciliation. Read the actual object IDs and failure timing before deciding whether to retry, import, move or correct configuration.

## Step 2: choose whether to revert or accept drift

A normal plan refreshes observations and compares them with configuration. If an unauthorized manual change conflicts with desired settings, applying a reviewed normal plan may restore them. If the manual change was an intentional emergency fix that should persist, update configuration to match the accepted decision and review the resulting plan. Silently accepting every outside change makes infrastructure policy depend on the last person to click a console button.

A refresh-only plan proposes updating state and outputs to reflect observed objects without changing remote objects to match configuration. Applying it accepts those refreshed observations into state; it does not automatically rewrite configuration. Future normal plans can still propose changes when configuration differs. Inspect a refresh-only plan before applying it, particularly when credentials or permissions could make objects appear absent. The [plan command reference](https://developer.hashicorp.com/terraform/cli/commands/plan) explains this mode.

The older standalone refresh command directly updates state and offers a weaker review boundary. Prefer the explicit refresh-only plan workflow when its behavior matches the diagnosis. A no-change refresh-only result in the local lab demonstrates command mechanics, not cloud drift detection coverage. `terraform_data` has no external firewall, disk or service for an operator to change behind Terraform's back.

## Step 3: preserve recovery evidence

A state snapshot includes a lineage identifying its history and a serial identifying its revision progression. These values help detect accidental replacement by a mismatched or older snapshot. A backup is not safe merely because its filename contains a date. Record where it came from, when it was captured, which tool read it and how access is restricted.

State can contain secrets, so protect backups as strongly as the active backend. Do not commit a pulled snapshot or paste it into a public issue. Backend version history is helpful, but restoring an old version requires reconciling everything created, changed or destroyed afterward. An old ownership record can refer to a deleted object or omit a newly created object, causing the next plan to do unexpected work.

`terraform state push` has lineage and serial safety checks; bypassing them with force can overwrite a newer or unrelated state. It is an exceptional tool, not a routine way to make a diagnostic disappear. Preserve the current snapshot first and rehearse the intended operation in a nonproduction context. The [state push reference](https://developer.hashicorp.com/terraform/cli/commands/state/push) documents its protection and override behavior.

## Step 4: use supported ownership tools

Prefer declarative moved and removed blocks for planned migrations because reviewers can see the intent in version control. Use import when an existing object needs a supported binding. State commands such as list and show inspect ownership; mv and rm change it. Removing a binding does not delete the real object, but leaving its configuration can cause Terraform to propose a new object later. Every exceptional operation should state both the address change and the resulting real-world owner.

Avoid hand-editing state JSON as a normal repair technique. Provider-specific schema versions, sensitive metadata, dependencies and deposed instances can make apparently simple edits inconsistent. Use Terraform's supported commands and current provider guidance. The right goal is a trustworthy plan with expected ownership, not a quiet terminal achieved by deleting inconvenient records.

A stale lock has another distinct repair path. Identify its ID and owning run; establish that the process has stopped and no other writer is active. `force-unlock` releases a lock, not the work that process may already have performed. It does not roll back resources or repair state. Never break someone else's active lock to accelerate your own run. The [force-unlock reference](https://developer.hashicorp.com/terraform/cli/commands/force-unlock) and [locking guide](https://developer.hashicorp.com/terraform/language/state/locking) explain the boundary.

## Practice and expected results

Run the advanced local lab. It captures a snapshot, checks positive serial and nonempty lineage, stores it only in the temporary directory with restricted file permissions, and gets a no-change refresh-only plan after the address migration. Final cleanup verifies empty normal state. These are actual local observations, separate from a remote recovery drill.

For the tabletop, analyze three incidents: a manually changed label, an interrupted apply with an untracked existing object, and a resource rename that proposes replacement. For each, identify the authoritative desired result, evidence to collect, likely repair and the plan that would confirm success. Expected choices are configuration reconciliation, supported adoption when appropriate, and a moved declaration. Do not choose force-unlock unless a stale lock is itself the diagnosed problem.

### Recall: Does restoring yesterday's state restore yesterday's infrastructure?

**Answer:** No. A snapshot restores records. It does not reverse real service changes. Reconcile current objects with the restored ownership view before allowing another apply.

## References

Official documentation checked on 2026-10-27.

- [Plan and refresh-only mode](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [State push safety checks](https://developer.hashicorp.com/terraform/cli/commands/state/push)
- [Force unlock](https://developer.hashicorp.com/terraform/cli/commands/force-unlock)
- [State locking](https://developer.hashicorp.com/terraform/language/state/locking)
- [Declarative refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)

[Previous lesson](./77-terraform-team-ci-and-approval-workflows.md) · [Next lesson](./79-cloud-threat-model-and-security-review.md)

---
title: "Terraform sensitive and ephemeral values"
topic: "Terraform sensitive and ephemeral values"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New design exercise; Project code comparison
---

# Terraform sensitive and ephemeral values

Prerequisite: remote-state access control. A secret can pass through source files, input loading, expressions, provider calls, plans, state, logs and artifacts. Protecting one stage does not secure the whole route. Start by drawing where a value originates and where it must be used, then decide which copies are necessary.

This is a new security design exercise. The advanced local lab contains only synthetic owner and tier data. It deliberately does not ask for passwords or demonstrate secret storage by putting a real credential into `terraform_data`.

## Step 1: distinguish hiding from omission

`sensitive = true` marks a variable or output so Terraform ordinarily redacts its value in human-facing output. Sensitivity propagates through many expressions. This helps prevent accidental disclosure during review, but it is not encryption and does not mean the value disappears from state or a saved plan. Machine-readable output and direct artifact access require their own controls.

An ephemeral value has a different purpose: Terraform omits it from persisted plan and state representation where the language permits its use. It is available for the current operation and belongs in an ephemeral-compatible context. Marking a variable both sensitive and ephemeral combines display protection with omission; neither property implies the other. The official [sensitive-data guide](https://developer.hashicorp.com/terraform/language/manage-sensitive-data) distinguishes these mechanisms.

A new illustrative input is:

```hcl
variable "session_token" {
  type      = string
  sensitive = true
  ephemeral = true
}
```

This declaration does not provide a usable destination by itself. Ordinary resource arguments that Terraform must retain cannot generally consume an ephemeral value. Provider configuration, supported ephemeral resources and supported write-only arguments are examples of intended use sites. An ephemeral child-module output can pass a temporary value across a module boundary; a root output cannot be used as an ephemeral export for later consumers.

## Step 2: check both CLI and provider support

Terraform 1.10 introduced ephemeral variables, child-module outputs and ephemeral resource blocks. Managed-resource write-only arguments require Terraform 1.11 or later and support from the particular resource/provider schema. Installing a new Terraform binary does not add an argument to an old provider. Read the documentation for the exact locked provider version before claiming a resource supports a particular temporary input.

Write-only arguments allow an input to be passed to a provider without that argument's value being persisted by Terraform. A resource may expose a companion version field that signals when the provider should act on a new value, because the previous secret is unavailable for an ordinary equality comparison. The field name and rotation semantics are provider-specific. Incrementing an illustrative version is not a universal Terraform password-rotation protocol. [Write-only argument documentation](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only) explains the requirements and limitations.

Inspect the project's [version requirements](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/versions.tf). Its allowed CLI range begins at 1.10. A future change using write-only managed arguments would need to account for the 1.11 minimum as well as the chosen provider schema. This lesson does not modify those requirements or claim that the project already implements ephemeral secret routing.

## Step 3: follow downstream copies

Preventing Terraform from storing an argument does not prove the remote service avoids storing it. A database must retain some representation of its authentication material. A provider might expose another readable attribute, and an application can log a credential after receiving it. Evaluate each downstream system rather than treating one language annotation as an end-to-end guarantee.

There is an especially useful caution in current `terraform_data` documentation: its newer `store` mechanism can accept a write-only input and then copy that content into a stored output. That resource is intended to retain data. Therefore even the term write-only describes an argument boundary, not a promise that no derivative value can ever reach state. Do not generalize from an input flag without inspecting the complete resource's behavior. The [built-in resource reference](https://developer.hashicorp.com/terraform/language/resources/terraform-data) describes that retention explicitly.

For a mental exercise, imagine a temporary deployment token flowing into a provider configuration. Draw separate boxes for the variable, plan, provider, service and logs. Ask which components see the clear value during execution, which persist it and who may inspect their outputs. Ephemeral omission narrows artifact exposure, but runtime process access and provider trust still matter.

## Step 4: make operational habits match the model

Never commit actual secrets in `.tfvars`, scripts, shell history or teaching examples. Environment-supplied inputs can avoid some file copies but still reach persistent Terraform artifacts when used in ordinary retained arguments. An ignored local file is still a copy on disk. Restrict the permissions and lifetime of plans, state, crash output and debugging logs. Redact before sharing a diagnostic; do not assume the CLI redaction shown in one terminal applies to every export path.

Secret rotation should name the owner, source of truth, distribution path, verification and revocation step. Changing an input may update a remote object, trigger replacement or do nothing until a companion version changes. Read the plan and resource contract. Removing a secret from source does not scrub older Git history, backend versions, plan uploads or exported backups. Handle those independently when responding to an actual disclosure.

## Practice and expected results

Create a synthetic routing table with three rows: a public label, a persisted sensitive password argument, and a temporary provider token. Record whether each should be displayed, retained in plan/state, and available to a later run. The expected answer distinguishes sensitive redaction from ephemeral omission and identifies the destination schema as a prerequisite.

Run the advanced local lab to inspect safe metadata persistence. Its owner values appear in output and state by design. Do not replace them with secrets. The lab proves contracts and identity, not the absence of secrets from a real provider's internal logs or a remote service.

### Recall: Is a write-only argument sufficient evidence that no related value appears anywhere in state?

**Answer:** No. It prevents persistence of that argument value at its defined boundary. Inspect the resource's other attributes and behavior; a resource may intentionally produce a stored derivative or output. Provider support and CLI version must also be verified.

## References

Official documentation checked on 2026-10-27. Local exercises used Terraform 1.17.0.

- [Sensitive and ephemeral mechanisms](https://developer.hashicorp.com/terraform/language/manage-sensitive-data)
- [Write-only arguments and requirements](https://developer.hashicorp.com/terraform/language/manage-sensitive-data/write-only)
- [terraform_data storage behavior](https://developer.hashicorp.com/terraform/language/resources/terraform-data)

[Previous lesson](./73-terraform-remote-state-and-access-control.md) · [Next lesson](./75-terraform-import-moves-and-provider-upgrades.md)

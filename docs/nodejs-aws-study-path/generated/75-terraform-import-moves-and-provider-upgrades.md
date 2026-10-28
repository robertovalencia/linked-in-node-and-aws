---
title: "Terraform import, moves and provider upgrades"
topic: "Terraform import, moves and provider upgrades"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New credential-free practice extension; Project code comparison
---

# Terraform import, moves and provider upgrades

Prerequisite: state and module contracts. Terraform associates a configuration address with an existing object through state. Several operations change that relationship, but their intentions differ. Import adopts an unmanaged object. A move preserves ownership while changing an address. Removal can relinquish ownership without destroying the object when explicitly configured. A provider upgrade changes the implementation interpreting resource schemas and operations.

Treat each as a migration with a predicted result. Combining address changes, provider upgrades and behavior changes in one large plan makes an unexpected replacement harder to explain. A small, reviewable sequence creates useful evidence at each boundary.

## Step 1: classify the intended ownership change

Suppose a real object exists and no state owns it. An import can associate it with a configured address if its provider/resource supports import and the supplied identifier is valid. Importing does not guarantee that your written arguments match reality. The following plan may propose updates or replacement to reconcile defaults, missing settings or immutable attributes. Read that plan before treating adoption as complete.

Configuration-driven import blocks, available since Terraform 1.5, make adoption reviewable in a plan. Some workflows can generate candidate configuration, but generated text still needs inspection. A data source reads an object; it does not adopt ownership. An import should not make two states manage the same object. Before adoption, establish the current owner and the handoff process. The official [import overview](https://developer.hashicorp.com/terraform/language/import) explains the supported workflow.

The advanced lab does not fake an import. It uses `terraform_data` for local identity exercises and demonstrates a supported address move. A cloud import would need a real target, provider support and appropriate authorized access. A successful local move is not evidence that a particular AWS resource's import identifier or schema has been tested.

## Step 2: preserve identity through address refactoring

Renaming a resource label without migration metadata normally removes one desired address and adds another. Terraform can then propose destroy/create even if the human intended only a code cleanup. A `moved` block declares an old-to-new address mapping and allows the plan to preserve object identity. Terraform 1.1 and later supports moved blocks for module refactoring. Keep them as migration history for supported consumers.

The new local lab changes an internal child resource from `terraform_data.record` to `terraform_data.entry`. A moved block inside the child maps those relative addresses. The parent still instantiates catalog, identity and search with stable keys. Expected evidence is three changes with no-op resource actions and previous addresses pointing to record, followed by unchanged IDs after applying the move plan.

A map-key rename is also an address change. Moving catalog to product-catalog needs an explicit old-instance to new-instance mapping if it represents the same managed object. Converting count indexes to `for_each` keys requires a deliberate mapping for each instance. Do not rely on matching display names. State identity follows addresses and recorded object IDs, not an intuitive similarity between two strings. [Module refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring) describes these cases.

## Step 3: relinquish ownership intentionally

Removing a resource block without another ownership instruction normally proposes destruction. If a team is transferring management to another system while leaving the object running, an explicit `removed` block with `lifecycle { destroy = false }` expresses that handoff in configuration. Removed blocks were introduced in Terraform 1.7. Read the current block reference and plan carefully: omission of the non-destruction setting is not a safe ownership transfer.

For a paper exercise, write three rows: adopt existing object, rename managed address, stop managing while retaining object. Match them to import, moved and removed-without-destroy. Then state who owns the object afterward. An object retained without an owner creates an operational gap even when the Terraform plan looks quiet. A migration runbook should name the receiving team, recovery authority and next reconciliation mechanism. The [removed block reference](https://developer.hashicorp.com/terraform/language/block/removed) documents the ownership mechanism.

## Step 4: upgrade the provider as a separate change

The project's [provider requirement](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/versions.tf) permits AWS 6.x selections. The lock file records the actual selected provider version and checksums for reproducible installation. `init -upgrade` can select a newer compatible provider; it does not prove that the newer schema preserves all behavior. Read the provider's upgrade guide, initialize deliberately, review lock changes, run configuration tests and inspect a refreshed plan.

Provider state schemas may migrate forward when a new version reads existing state. Returning to an older plugin may not reverse that migration. Preserve recovery snapshots and avoid promising an effortless downgrade. A provider-source-address change is different again: `terraform state replace-provider` changes provider ownership references in state and requires a controlled migration. It does not rename resources or automatically make incompatible schemas equivalent. The [replace-provider reference](https://developer.hashicorp.com/terraform/cli/commands/state/replace-provider) describes that operation.

Provider aliases are configuration instances; provider source addresses identify implementations. If an error reports a missing alias configuration, changing the provider source address is unlikely to be the right repair. Restore the necessary configuration and understand the recorded relationship before altering state.

## Practice and expected results

Run the advanced lab and locate the saved move-plan assertion in its runner. Predict that all three IDs survive the child rename. The assertion checks structured plan actions and previous addresses, then compares IDs after apply; a reassuring text message alone would be weaker evidence. On paper, outline a separate import review and provider-upgrade review with their own expected no-surprise plans.

### Recall: Does an import prove Terraform will leave an object unchanged afterward?

**Answer:** No. Import establishes a binding. Configuration may still differ from the real object, so a subsequent plan can propose changes. Adoption is complete only after ownership and the desired reconciliation behavior are understood.

## References

Official documentation checked on 2026-10-27.

- [Import overview](https://developer.hashicorp.com/terraform/language/import)
- [Moved declarations and module compatibility](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
- [Removed block](https://developer.hashicorp.com/terraform/language/block/removed)
- [Provider-address replacement](https://developer.hashicorp.com/terraform/cli/commands/state/replace-provider)

[Previous lesson](./74-terraform-sensitive-and-ephemeral-values.md) · [Next lesson](./76-terraform-testing-and-policy-as-code.md)

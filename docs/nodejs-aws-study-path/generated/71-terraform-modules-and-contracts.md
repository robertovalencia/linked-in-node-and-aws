---
title: "Terraform modules and contracts"
topic: "Terraform modules and contracts"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New credential-free practice extension; Project code comparison
---

# Terraform modules and contracts

Prerequisite: lesson 70. A module is a directory of Terraform configuration evaluated as a unit. Every configuration has a root module. A child module is called by another module through a `module` block. Reuse is one benefit, but the deeper benefit is an interface that lets callers reason about accepted inputs, exported outputs, ownership and compatibility.

The project's [AWS root](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) provides concrete infrastructure to study. The child module in this lesson is a new teaching extension using synthetic service metadata. It is not a claim that the project already uses a service-module platform.

## Step 1: define the contract before its implementation

Describe a module in ordinary language: “Given a stable service key, owner and tier, produce a normalized inventory contract and an identity.” Required input types explain shape; validation explains semantic limits; outputs explain what callers can depend on. Resource details inside the module remain implementation choices. A caller should not need to navigate into a child's resource internals to obtain a supported value.

In the advanced lab, `modules/service` accepts name, owner and tier. Owner validation rejects an empty or very short owner after trimming. The module outputs `contract` and `id`. The parent collects these into maps. Adding a new internal attribute need not break callers, while renaming `contract` would break expressions that consume it. Output names, types, sensitivity and meanings belong in compatibility review alongside input changes.

An object type alone cannot express every business rule. The owner may be a valid string yet contain only spaces. Validation checks the accepted value at the interface. A precondition guards assumptions needed by a resource or output. A postcondition checks a resulting object using `self` where supported. A `check` block records an assertion about the wider configuration and ordinarily warns on failure rather than blocking normal operations. Do not replace a required safety invariant with a warning. [Lifecycle conditions](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle) explain the resource-level mechanism.

## Step 2: keep identity stable across reuse

A module can be instantiated with `count` or `for_each`. `count` addresses instances numerically: `module.service[0]`. A map-based `for_each` addresses them by key: `module.service["catalog"]`. These are identity decisions. Reordering a list passed to count can assign an old index to a different service. Keyed maps make an intended service boundary visible, but changing a key still changes an address.

Choose durable domain keys such as catalog and identity. Keep display names and changing owner values inside each object. Do not use a secret as a key: addresses appear in output and are operational identifiers. Do not use a future provider-generated ID as the key because Terraform must enumerate instances before apply. For a migration from count to keys, write explicit mappings and verify no unintended replacements in the saved plan.

The lab first has two module instances, then updates one owner and adds a third key. Existing resource IDs must remain the same. Later the child resource is renamed from record to entry using a `moved` block within the child. The same local migration applies inside each module instance. This demonstrates why the location of a moved declaration matters: the child describes its own internal address change while the root retains its public module keys.

## Step 3: choose a source and update strategy

A local source such as `./modules/service` is part of the same reviewed checkout. A registry source identifies a published module and can use the module block's `version` argument. A Git source can select a revision with its source URL. A registry module version and a provider version are separate dependencies. The dependency lock file records provider selections and checksums; it does not lock every remote module source for you.

For a team library, publish an intentional version, read its changes, and test the proposed upgrade in a consuming root. An immutable Git revision can make an experiment reproducible, but it still needs a maintenance policy. Floating branches make a later initialization capable of retrieving changed implementation without an obvious local module edit. Never assume `terraform init -upgrade` means only “repair my cache”; it can change selected dependencies within their constraints.

A contract includes lifecycle behavior as well as syntax. If a new version changes a default that triggers replacement, document that consequence even when the input type remains the same. Keep useful migration blocks long enough for supported consumers to pass through the transition. Removing a historical moved block too early can break callers that skipped a release. [Module refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring) covers this compatibility issue.

## Step 4: teach failure paths explicitly

A module that exposes every provider argument is difficult to reason about; a module with no escape hatch can become an obstacle. Begin with a focused responsibility and meaningful outputs. Compose several modules in a root that owns their relationships. Avoid a single reusable module that creates unrelated infrastructure, backend administration and application delivery because its upgrade and failure boundaries become unnecessarily broad.

Provider configurations normally belong to the root, while each module declares its provider requirements. This makes credentials and environment choices visible to the caller. Modules containing their own provider configurations can impose compatibility limits on use with `count`, `for_each` and `depends_on`; lesson 72 explains aliases and explicit injection. A child module's provider source requirements are still necessary even when it receives a configuration from its parent.

## Practice and expected results

Read the [advanced lab](../labs/terraform-advanced/README.md), then run its Python runner. Locate the input validation, precondition, postcondition and check before execution. Predict which invalid tier test names `var.services` in `expect_failures`. Expected evidence includes two initial instances, a targeted update, one new instance and an address migration preserving all three IDs. A failure must produce a nonzero runner exit; changing an assertion simply to obtain green output defeats the contract exercise.

### Recall: Does a resource's internal name form part of a module's public contract?

**Answer:** Callers should consume declared outputs, but internal addresses still matter to state and upgrades. Renaming an internal resource can require a moved block even when every public output retains its name and type.

## References

Official documentation checked on 2026-10-27.

- [Provider requirements and configuration in modules](https://developer.hashicorp.com/terraform/language/modules/develop/providers)
- [Module refactoring and compatibility](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
- [Lifecycle conditions](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)

[Previous lesson](./70-terraform-expressions-and-type-system.md) · [Next lesson](./72-terraform-provider-aliases-and-environments.md)

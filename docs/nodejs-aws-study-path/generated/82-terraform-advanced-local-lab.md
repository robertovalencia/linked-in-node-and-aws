---
title: "Terraform advanced local lab"
topic: "Terraform advanced local lab"
last_researched: 2026-10-27
source_labels: New credential-free practice extension; Actual local execution; Terraform mechanics
---

# Terraform advanced local lab

Prerequisite: lessons 70–78 and the original Terraform local lab. This new extension gives you an observable exercise in module contracts, stable instance identity and reviewable address migration. You need Python 3 and an already installed Terraform CLI matching `>= 1.10, < 2.0`. The recorded run used Terraform 1.17.0. You do not need an account, credential, provider download or cloud workspace.

The lab operates on synthetic service metadata using only the built-in `terraform_data` resource. It does not simulate AWS networking or deploy the marketplace. Its purpose is to make language and state mechanics concrete enough that you can interpret a more consequential plan later.

## Step 1: inspect isolation before execution

Open the [walkthrough](../labs/terraform-advanced/README.md), [root configuration](../labs/terraform-advanced/main.tf), [child module](../labs/terraform-advanced/modules/service/main.tf) and [runner](../labs/terraform-advanced/run.py). Verify that there is no AWS provider, backend block or provisioner. The child directory is a local source. The runner creates a fresh temporary directory and copies only the teaching files into it.

The runner removes ambient Terraform CLI arguments, workspace selection and relevant credential environment settings. It uses a temporary CLI configuration and disables checkpoint checking. This avoids inheriting a local backend selection or injected Terraform flags from a developer's shell. Isolation is implemented through a specific copy boundary; it is not a claim that running arbitrary Terraform files is harmless.

Run from the repository root:

```sh
python3 docs/nodejs-aws-study-path/labs/terraform-advanced/run.py
```

A nonzero exit means a command or assertion failed. Read the first diagnostic and preserve it when it explains a repair. Do not convert every nonzero result to success: this runner deliberately expects plan exit code two only where `-detailed-exitcode` should report a proposed change.

## Step 2: predict the module contract

The root input contains catalog, identity and disabled preview. Each value has an owner, optional enabled flag and optional tier. The `for` expression filters enabled entries and preserves their keys. The child module stores name, trimmed owner and tier, then exports a contract and an ID. Predict two initial instances: catalog with standard tier and identity with critical tier. Preview has no instance.

The root's validation limits key format and tier values. The child's validation rejects inadequate owner text. A precondition guards name format and a postcondition checks the stored result. A root check observes an empty inventory. Explain which conditions block normal operations and which normally warn before looking at the tests. Terraform can defer conditions whose inputs are not yet known; do not assume every apply-time result was already proved by validation.

The first plan must propose exactly two creates. The runner inspects JSON actions rather than searching for a reassuring sentence. Applying the saved local plan establishes IDs. A second plan must be unchanged. This establishes the baseline against which later migrations are judged.

## Step 3: distinguish content changes from identity changes

The next scenario changes catalog's owner and adds search. Predict three addresses, one updated object and one new object, with identity unchanged. The runner requires those exact resource actions in the saved plan. After applying it, catalog and identity must retain their original IDs.

This proves a specific mechanism: keyed `for_each` preserves the address of an existing instance when another key is added. It does not guarantee preservation when an existing key changes or a provider treats an attribute as replacement-only. Here, `terraform_data.input` can update in place. A real service resource has its own lifecycle rules.

For a paper variation, imagine renaming catalog's key to product-catalog without a move. Predict removal of one address and creation of another. Explain why changing a human-readable name inside the object is different from changing the key outside it. Resource identity is a state concern, not a visual resemblance between two labels.

## Step 4: migrate the child's internal address

The runner modifies only the temporary child copy, renaming `terraform_data.record` to `terraform_data.entry`. It adds a relative moved block inside the child. Because all module instances share that child implementation, the declaration applies to each instance's internal address.

The migration plan must have three previous addresses and no-op resource actions. Applying it updates Terraform's bindings without replacing the objects. The runner compares all three IDs before and after. The checked-in starting files retain the record name, so another execution repeats the same complete experiment in a fresh directory. [Module refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring) documents the declarative migration model.

No import is claimed. Adoption of an externally existing object is a different operation with provider-specific support and identifiers. This lab demonstrates a move of managed local records, which gives a truthful observation without pretending to import a cloud object.

## Step 5: test failure contracts and inspect state

Five Terraform test runs verify the default contract, explicit null using the optional default, owner normalization, invalid tier rejection and an expected empty-inventory check result. The tests supply explicit fixture inputs so the runner's scenario auto-variable file does not accidentally redefine the default test. An initial authoring run exposed that coupling; its assertion was retained and the fixture was repaired.

`expect_failures` names the intended validation or check. A test that fails for an unrelated reason should not count as successful negative coverage. The check expectation belongs to the test harness; the normal root check still has warning behavior. [Terraform test documentation](https://developer.hashicorp.com/terraform/language/tests) explains the scenario model.

The runner also pulls a snapshot without displaying its JSON, verifies serial and lineage, writes a temporary protected backup and performs a no-change refresh-only plan. It then destroys its normal local objects and requires an empty state list. The temporary directory is removed on exit. The actual successful execution reported 24 Terraform commands, 11 Python runner assertions and five passed Terraform test runs.

## Evidence limits and interview application

These observations support claims about local language contracts, optional defaults, filtering, key stability, planned actions and identity-preserving child moves. They do not prove remote locking, backend encryption, OIDC, cloud import, real provider permissions, policy licensing or application health. Keep the lesson's design exercises separate from execution claims.

Use this lab in an interview by predicting one plan, explaining one preserved identity and diagnosing one meaningful failure. A clear explanation of why a test originally failed is better evidence of engineering judgment than hiding the diagnostic or weakening the assertion.

### Recall: Why verify both plan actions and IDs after the move?

**Answer:** The plan shows the intended migration without replacement. Comparing IDs afterward confirms the local execution preserved identity. Together they establish more than a successful command exit alone.

## References

Official documentation checked on 2026-10-27; the lab was actually executed with Terraform 1.17.0.

- [Built-in terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data)
- [Module address migration](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring)
- [Terraform tests](https://developer.hashicorp.com/terraform/language/tests)
- [Validation mechanisms](https://developer.hashicorp.com/terraform/language/validate)
- [Plan modes and exit behavior](https://developer.hashicorp.com/terraform/cli/commands/plan)

[Previous lesson](./81-network-security-local-lab.md) · [Next lesson](./83-professional-cloud-capstone-and-question-bank.md)

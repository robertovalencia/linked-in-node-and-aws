# Advanced Terraform contracts and identity lab

This is a new credential-free teaching extension. It uses only the built-in `terraform_data` resource, a local child module and synthetic metadata. It creates no AWS resources and contains no AWS provider, remote backend, provisioner or cloud workspace. It complements the existing introductory `terraform-local` lab rather than replacing or copying that lab's lifecycle tour.

You need Python 3 and an installed Terraform CLI matching `>= 1.10, < 2.0`. The recorded execution used Terraform 1.17.0. The runner does not install software. Run from the repository root:

```sh
python3 docs/nodejs-aws-study-path/labs/terraform-advanced/run.py
```

The runner copies only this lab's configuration, child module and tests into a new temporary directory. It removes ambient Terraform CLI flags, workspace selection, Terraform credentials and common cloud environment settings, then uses an isolated CLI configuration with checkpoint checking disabled. It neither reads nor copies the project's real infrastructure. The temporary directory is removed when the process exits, including after an assertion fails. Terraform test state and the normal runner state are separate.

## Read the contract first

In [main.tf](./main.tf), the `services` input is a map of objects. Keys are durable identities. Owner is required; enabled defaults to true; tier defaults to standard. The root validates key format and the allowed tier vocabulary. A `for` expression filters enabled entries before `for_each` instantiates the child.

In [modules/service/main.tf](./modules/service/main.tf), the child validates owner text and stores a normalized contract. Its precondition checks the service-name assumption and its postcondition checks the stored result. Its declared outputs are the parent-facing contract. A root check observes whether any service is enabled; that check ordinarily warns rather than blocking a normal apply.

Predict the initial output before running: catalog and identity exist, preview is absent, catalog has a standard tier, and identity has a critical tier. Resource IDs are generated during apply and should not be hardcoded.

## Observe three separate changes

The first saved plan must create exactly two child resources. Applying that local plan establishes their IDs, and an unchanged plan must return exit code zero with no changes. With `-detailed-exitcode`, code two is expected when a plan proposes changes; it is not an error in that situation.

Next, the runner changes catalog's owner and adds search. It reads the structured plan to require an update for catalog, no-op for identity and create for search. Applying this plan must preserve the two existing IDs. This is the practical difference between changing a value inside a map and changing an instance key.

Finally, the runner edits only its temporary child copy: record becomes entry and a child-level moved block maps the addresses. The plan must report all three previous addresses and no-op resource actions. After applying that plan, every ID must remain equal to the pre-move output. The checked-in source remains at the starting resource name so each run repeats the same experiment.

## Tests, snapshot and cleanup

[tests/contracts.tftest.hcl](./tests/contracts.tftest.hcl) contains five runs:

1. `default_contract` applies an explicit default-shaped fixture and checks filtering and optional defaults.
2. `explicit_null_default` confirms a non-null optional default handles an explicit null.
3. `child_normalizes_owner` confirms the child's trimmed output.
4. `reject_invalid_tier` expects the exact root input validation to fail during planning.
5. `check_warning_is_observable` expects the empty-inventory check result in the test harness.

The harness's expected check failure does not convert an ordinary check warning into a production hard gate. These apply tests use only local built-in resources. Uninspected Terraform tests in other repositories can use real providers and create infrastructure.

The runner pulls a state snapshot without printing the JSON, checks serial and lineage, writes a temporary backup with mode `0600`, and performs a no-change refresh-only plan. This demonstrates inspection mechanics. It does not simulate external cloud drift, encryption, remote locking or disaster recovery. Final destroy is limited to the temporary built-in objects; the runner then requires an empty state list.

The recorded successful result is:

```text
PASS: 24 Terraform commands; 11 runner assertions; five Terraform test runs. No cloud provider, backend or credentials.
```

Terraform commands can print internal refresh/read messages; the summary counts top-level CLI invocations. A failed command or failed Python assertion causes a nonzero exit. The initial authoring run caught a default-test fixture inheriting scenario auto-variables; the fixture now supplies its own explicit input, preserving the original assertion.

## Scope of the evidence

This lab proves local module interfaces, optional/null behavior, validation and check expectations, keyed update isolation and a child-address migration. It does not prove imports, cloud permissions, provider aliases, remote-state authorization, OIDC, hosted policies or application readiness. Those topics have separate design exercises in lessons 70–78. Never replace synthetic owners with real secrets: ordinary `terraform_data.input` intentionally persists its input.

Official references: [terraform_data](https://developer.hashicorp.com/terraform/language/resources/terraform-data), [module refactoring](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring), [Terraform tests](https://developer.hashicorp.com/terraform/language/tests), [validation](https://developer.hashicorp.com/terraform/language/validate).

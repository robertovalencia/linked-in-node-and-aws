# 9 · Run Terraform commands step by step, without AWS

[Walkthrough index](README.md) · [Next: the actual AWS command workflow](10-terraform-aws-commands.md)

“Trigger Terraform” means executing its CLI against a specific configuration directory. Terraform is not a server that starts by itself. Begin here: this example uses the project's built-in `terraform_data` teaching resource. It has no AWS provider, remote backend, provisioner or billable cloud object.

## Fast path: the existing complete lab

Run from the project root:

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
terraform version
python3 docs/nodejs-aws-study-path/labs/terraform-local/run.py
```

Expected: the runner completes its lifecycle/assertion checks and three configuration test runs, then cleans up temporary local resources. Python 3 and Terraform `>=1.10,<2.0` must already be installed. The recorded command-workbook verification uses Terraform 1.17.0. The runner does not install software or authenticate to AWS. Its [source and scope](../labs/terraform-local/README.md) explain the isolation.

To learn the individual commands instead of letting the runner sequence them, use the manual path below in the **same terminal**. Do not substitute an `infra/` directory for this lab.

## Step 1. Make an isolated working copy

The following variables identify this lesson only. `mktemp` creates a new unique directory; `cp` copies only the inspected teaching configuration/tests. Neither Terraform source nor operational state in the application roots is changed.

```bash
cd /Users/robertovalencia/Documents/Business/linked-in-node-and-aws
LESSON_TF_REPO="$(pwd -P)"
LESSON_TF_CLI="$(command -v terraform)"
LESSON_TF_DIR="$(mktemp -d "${TMPDIR:-/tmp}/marketplace-tf-commands.XXXXXX")"
cp "$LESSON_TF_REPO/docs/nodejs-aws-study-path/labs/terraform-local/main.tf" "$LESSON_TF_DIR/main.tf"
cp -R "$LESSON_TF_REPO/docs/nodejs-aws-study-path/labs/terraform-local/tests" "$LESSON_TF_DIR/tests"
: > "$LESSON_TF_DIR/terraform.rc"
study_tf() {
  env -i TF_CLI_CONFIG_FILE="$LESSON_TF_DIR/terraform.rc" CHECKPOINT_DISABLE=1 \
    "$LESSON_TF_CLI" -chdir="$LESSON_TF_DIR" "$@"
}
```

`study_tf` is a shell shortcut for the real Terraform binary, with `-chdir` fixing its directory. `env -i` gives that process a clean environment so inherited AWS credentials, `TF_VAR_*`, workspace choices and `TF_CLI_ARGS_*` cannot change the exercise. The empty CLI configuration avoids inheriting remote CLI settings. This teaching copy's normal local state stays in its own directory. Do not paste real secrets into `terraform_data.input`: the resource deliberately stores its input in state.

## Step 2. Check formatting, initialize and validate

```bash
study_tf fmt -check
study_tf init -input=false
study_tf validate
```

- `fmt -check` reports formatting differences without rewriting source.
- `init` prepares this configuration's Terraform working data. The built-in provider needs no external AWS plugin.
- `validate` checks configuration consistency, without creating the resource.

Expected: formatting exits successfully, Terraform reports initialization success, and validation succeeds. An initialization success message is not an apply result. Read the [actual HCL](../labs/terraform-local/main.tf) and confirm the resource type before continuing.

## Step 3. Produce and inspect a saved creation plan

```bash
study_tf plan -input=false -no-color -out=create.tfplan
study_tf show -no-color create.tfplan
```

Expected: **1 to add, 0 to change, 0 to destroy**, for `terraform_data.release`. Its `input` contains `marketplace-local` and release `v1`; its ID/output may be unknown until apply. `-out` saves the exact proposal rather than changing anything. Because `-chdir` selects the lesson root, this relative plan filename is inside the temporary directory.

This first example deliberately omits `-detailed-exitcode`: a valid ordinary plan can exit 0 even when it proposes changes. With that optional flag, 0 means no changes, 1 means error, 2 means changes. Treating 2 as an ordinary failure in `set -e` scripts is a common automation mistake. [Plan reference](https://developer.hashicorp.com/terraform/cli/commands/plan).

## Step 4. Apply that local plan

```bash
study_tf apply -input=false -no-color create.tfplan
study_tf output -json release_summary
study_tf state list
study_tf state show -no-color terraform_data.release
```

Expected output includes name `marketplace-local`, release `v1`, and one managed address: `terraform_data.release`. Applying a saved plan does **not** display another interactive approval prompt. That is acceptable here because the inspected plan contains only the bounded local teaching object. The AWS chapter requires prior approval of the exact cloud artifact. Do not generalize this lab's permission to a different root.

`output` reads declared result values. `state list` reads tracked addresses; it does not enumerate every object in an AWS account. [Apply reference](https://developer.hashicorp.com/terraform/cli/commands/apply).

## Step 5. Observe an unchanged plan

```bash
study_tf plan -input=false -no-color -detailed-exitcode -out=no-change.tfplan
```

Expected: no changes, exit 0. Terraform is comparing this configuration's desired values with the managed local state. The built-in resource has no remote AWS object, so this is not an AWS drift or reachability test.

## Step 6. Change a value, not the identity

```bash
study_tf plan -input=false -no-color -var='release=v2' -out=release-v2.tfplan
study_tf show -no-color release-v2.tfplan
study_tf apply -input=false -no-color release-v2.tfplan
study_tf output -json release_summary
study_tf state show -no-color terraform_data.release
study_tf plan -input=false -no-color -var='release=v2' -detailed-exitcode -out=v2-no-change.tfplan
```

Expected: one in-place update, then release `v2`, followed by a no-change plan. The resource ID stays the same. A CLI `-var` applies to that invocation; state does not permanently redefine the source's desired input. Repeat `release=v2` when checking the changed scenario. Omitting it returns to the source default `v1` and can propose another update.

For stable-key modules, replacement and moved-address practice, run the separate [advanced lab](../labs/terraform-advanced/README.md) after finishing this exercise; do not edit a live root to imitate the demo.

## Step 7. Run the configuration tests

```bash
study_tf test -no-color
```

Expected: three passing runs, including the deliberately invalid slug's expected validation failure. Terraform tests have separate test state; these tests use built-in local resources only. The word “test” does not make an arbitrary cloud provider configuration safe. Always inspect the providers and test definitions first.

## Step 8. Plan local cleanup, then verify it

```bash
study_tf plan -destroy -input=false -no-color -var='release=v2' -out=cleanup.tfplan
study_tf show -no-color cleanup.tfplan
study_tf apply -input=false -no-color cleanup.tfplan
study_tf state list
```

Expected: one destruction of `terraform_data.release`, followed by an empty state list. `apply` executes the actions in its plan—including deletions—not only creation. This is cleanup of the isolated teaching object, not a cloud teardown instruction. Keep the temporary directory if you want to inspect its plans/state; deleting files is not a substitute for destroying real infrastructure.

You have now used `init`, `fmt`, `validate`, `plan`, `show`, `apply`, `output`, `state list` and `test` against a real executable example. For AWS, next study the different state/approval sequence in [chapter 10](10-terraform-aws-commands.md).

## Troubleshoot the first failing step

| Observation | Meaning / next check |
|---|---|
| `terraform: command not found` | Install Terraform through the official distribution, then confirm the supported version before rerunning Step 1 |
| `study_tf: command not found` | You changed terminal sessions; define the Step 1 function again rather than running from an uncertain directory |
| A plan mentions AWS resources | Wrong exercise/configuration; stop before apply and inspect the working directory |
| A proposed change returns exit 2 | Expected only when using `-detailed-exitcode`; inspect the plan instead of treating it as an error |
| Tests fail with unexpected values | Check that only `main.tf` and `tests/` were copied; no unrelated `.auto.tfvars` file should be present |

**Recall:** Which command creates the local object? Why does saved-plan apply not ask for yes? What happens if you omit `-var='release=v2'` after the update?

Official references: [initialization](https://developer.hashicorp.com/terraform/cli/commands/init), [plan](https://developer.hashicorp.com/terraform/cli/commands/plan), [apply](https://developer.hashicorp.com/terraform/cli/commands/apply), [tests](https://developer.hashicorp.com/terraform/language/tests).

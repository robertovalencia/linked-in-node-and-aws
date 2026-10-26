# Terraform without AWS credentials or billing

This teaching extension uses only `terraform_data`, supplied by Terraform's built-in provider. It creates no AWS resources, invokes no AWS CLI, installs no provider plugin, and needs no credentials. It teaches Terraform behavior; the application's actual AWS roots remain separate source examples.

Run from the repository root with Python 3 and an already installed Terraform version `>= 1.10, < 2.0`:

```sh
python3 docs/nodejs-aws-study-path/labs/terraform-local/run.py
```

Optionally retain command results in a JSON file, containing no AWS credentials, real infrastructure state or binary saved plans:

```sh
python3 docs/nodejs-aws-study-path/labs/terraform-local/run.py --evidence work/terraform-local-evidence.json
```

The runner creates a fresh temporary directory and copies only this lab's configuration and tests. It removes inherited AWS settings and Terraform variable/CLI argument overrides, checks the installed Terraform version, and removes the temporary directory on exit. It never works in `infra/aws-dev` or `infra/bootstrap` and never discovers an application backend. Saved plans and state remain inside its temporary directory.

## What to read first

Open [main.tf](./main.tf). The input `project` defaults to `marketplace` and validates its naming contract. The local value derives `marketplace-local`. The resource's `input` records the name and release, while `triggers_replace` holds the generation. The output returns the stored input after apply. This is a small stateful object; it is not a simulated EC2 API.

Then read [the runner](./run.py). The script performs these operations and checks the results instead of printing an unconditional success message:

| Step | Operation | Expected evidence |
|---|---|---|
| 1 | `fmt -check`, `init -backend=false`, `validate` | Configuration accepted; built-in provider available |
| 2 | First saved plan | Exit 2; resource action `create` |
| 3 | Apply the first saved plan | One generated resource identity |
| 4 | Plan unchanged inputs | Exit 0; no change |
| 5 | Set release to v2 and plan | Exit 2; in-place `update` |
| 6 | Apply that saved plan | Output release becomes v2 |
| 7 | Set generation to 2 and plan | Exit 2; `delete`, then `create` |
| 8 | Apply replacement | Identity differs from the initial resource |
| 9 | Rename the copied resource and append a moved block | Resource `no-op`; old address recorded |
| 10 | Apply the move and plan again | Same replacement identity retained; follow-up exit 0 |
| 11 | `terraform test` | Three configuration test runs pass |
| 12 | Destroy local objects, then list state | Empty state; temporary directory removed |

Detailed exit code 2 means changes are present when `-detailed-exitcode` is requested. It is deliberately expected for creation, update, replacement and the address migration. Exit 1 is an error. The moved plan can have exit 2 while its resource action is a no-op because Terraform must record the address change.

The runner's normal apply commands consume saved local plans. Its sole `-auto-approve` cleanup is bounded to built-in teaching objects inside its isolated directory. Do not transfer that cleanup policy to application infrastructure.

## Configuration tests

[contracts.tftest.hcl](./tests/contracts.tftest.hcl) contains three runs:

- `default_contract` applies only the built-in resource and checks the default name and release.
- `custom_input` supplies catalog/v2 and checks that inputs flow through the local value and resource output.
- `invalid_project` plans with an invalid slug and expects the specific variable validation failure.

These tests intentionally use test state separate from the runner's normal state. They contain no external provider and no provisioner. A Terraform test with a real AWS provider can create billable resources; the safety of this lab follows from the configuration you can inspect, not from the word “test.”

## What this lab cannot prove

`terraform_data` has no remote AWS object to refresh, so this lab does not demonstrate AWS drift detection. It cannot prove IAM permissions, network reachability, SSM connectivity, EC2 capacity, free-plan eligibility or application health. Lessons 32–39 connect these mechanics to pinned real project code while retaining that boundary.

On 2026-10-26, the complete runner passed using Terraform 1.17.0 on darwin_arm64: all 27 CLI invocations succeeded with their expected exit codes, all three local configuration runs passed, identity assertions passed, and cleanup produced empty state. Separate project mock checks also passed five aws-dev runs and two bootstrap runs using cached AWS provider 6.69.1 in temporary source copies; the aws-dev S3 backend was removed in those copies. No cloud apply or real AWS integration is claimed.

If a command fails, read its diagnostic. The runner fails immediately rather than continuing to a success banner, removes the temporary directory, and writes completed command evidence when `--evidence` was requested. Correct the configuration or tool issue and start a fresh run. You do not need to repair any cloud resource after this bounded exercise.

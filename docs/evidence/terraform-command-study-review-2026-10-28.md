# Independent Terraform command-study review

Status: repaired candidate independently approved for documentation publication. Cloud execution remains unapproved.

Scope: beginner step-by-step commands for the existing local built-in Terraform lab and later owner-operated AWS Terraform roots. Source inspected at `01c30fc`. This critic will not run AWS authentication, AWS provider plan/apply/destroy, image publication or GitHub dispatch.

Source constraints checked:

- `AGENTS.md` requires concrete saved-plan and current-cost approval before cloud provisioning, actual execution evidence, separate local/cloud state, and independent review.
- The foundation lab contains only built-in `terraform_data.release`; it has default release v1/generation1, three configuration tests and no provisioner, AWS provider or backend.
- `infra/bootstrap` uses local state and defaults its provider to us-east-1 unless the region is supplied. Bucket-only review expects five creates with `create_github_oidc=false`.
- `infra/aws-ecs-dev` declares S3 backend; actual key must be `linked-in-node/ecs-dev/terraform.tfstate`, region us-east-2, encrypt/use_lockfile true.
- The already-issued certificate has separate private local state, which must not be replaced by an empty copy or migrated implicitly.
- Current HTTPS review distinguishes a five-create bootstrap plan from a never-apply 111-create local-backend HTTPS preview. A final S3-backed plan is still pending approved bootstrap.
- The deploy-dev workflow verify job covers ECS checks, but its deploy=true job publishes images and calls the preserved EC2/SSM deploy script. It must not be taught as an ECS deployment command.

Candidate review:

- Chapter09 explains working directory, clean environment, built-in provider, local state, saved-plan behavior, detailed exit codes and cleanup accurately.
- Chapter10 correctly preserves certificate state, explicitly requires Ohio/bootstrap no-OIDC inputs, distinguishes private local preview from final S3-backed plan, uses private artifact paths and umask before redirection, explains saved-plan no-prompt behavior, retains current-cost/source/plan approval, and explicitly identifies deploy=true as the EC2/SSM path.
- Existing source primary-reference links and pending execution claims match the source at01c30fc. All15 local/pinned-source targets in the two pages resolve against the source plus overlay. Root author is checking final packaged index/ZIP separately.

Independent actual execution:

- Executed all eight manual chapter09 Bash blocks in sequence using Terraform1.17.0 and the unmodified built-in lab copied by the documented commands. No AWS provider or registry access was involved.
- Injected invalid inherited AWS_ACCESS_KEY_ID and TF_CLI_ARGS_apply canaries; the documented env-i helper prevented either from affecting Terraform.
- Asserted saved-plan JSON actions were create, in-place update and delete. Observed both no-change checks, all three configuration tests and an empty final state.
- Bash syntax for the initial nine chapter10 blocks and repaired ten chapter10 blocks passes. Read-only Terraform fmt against its three listed source roots exits0.
- Reproduced the initial guard failure with a stub shell function named terraform: a preexisting bootstrap.tfplan still reaches all four Terraform invocations. This probe ran no actual Terraform or AWS process.

No AWS authentication, AWS provider init/plan/apply/destroy, resource mutation or GitHub dispatch was performed.

Binary winner: WIN / APPROVE the repaired two-page command documentation. It meets the beginner execution/explanation bar without claiming cloud execution, bypassing owner approval or confusing legacy delivery with ECS. Final publication packaging remains the parent author’s verification task.

Largest gap: test guards were described as stopping artifact overwrite, but ordinary pasted Bash blocks continue after test returns nonzero. A failed plan could also be followed by show of a stale artifact. This weakens the review-artifact boundary even though actual cloud execution remains explicitly gated.

Repair verified: cloud operational templates now use subshell set-eu, require the initialized root and private paths, refuse both existing binary plans and JSON, set the run directory mode0700, and set umask077 before new private files. The apply template additionally compares the receipt SHA256 and fresh STS account before reaching apply; documentation correctly says an integrity match is not proof of human approval.

Retained failed behavior: the initial Step4 block performed test-not-exists followed by init, validate, plan and show as independent unguarded commands. With a preexisting plan, a shell-only stub probe still observed all4 Terraform calls. No real cloud process was used. This reproduces the largest gap without exposing any private artifact.

Repaired independent shell-only probes:

| Probe | Actual result |
|---|---|
| Bootstrap plan already exists | Exit1; zero Terraform stub calls |
| Bootstrap init fails | Exit1; only the first stub call; validate/plan/show skipped |
| ECS binary plan already exists | Exit1; zero Terraform stub calls |
| ECS JSON already exists | Exit1; zero Terraform stub calls |
| ECS root variable missing | Exit1; zero Terraform stub calls |
| ECS plan fails | Exit1; no JSON file created |
| Approved-artifact hash differs | Exit1; zero Terraform stub calls |
| STS account differs | Exit1; zero Terraform stub calls |
| Stubbed approved context matches | Exit0; exactly one stubbed apply call |
| Stubbed successful ECS plan/show | Exit0; directory0700, plan0600, JSON0600 |

These ten probes exercise shell behavior only. The stubbed success cases establish control flow and file modes, not successful AWS authorization, provisioning or deployment. No check was relaxed to obtain the documentation win.

# 4 · Terraform roots, state and plan review

**29 October update:** the S3 state bootstrap was approved, applied and independently verified. The real S3-backed application plan is prepared; application resources/activation remain pending. Read the [actual execution journal](11-aws-execution-journal.md) for commands and the new 24-hour/delete-demo-data choice. Earlier dated checkpoints below remain historical.

[Previous: identity and costs](03-aws-identity-and-costs.md) · [Index](README.md) · [Next: hostname and certificate](05-hostname-dns-and-certificate.md)

## 1. Start in the safe teaching directory

The default practice uses built-in `terraform_data`, not the AWS provider. Run from the repository root with installed Python 3 and Terraform `>=1.10,<2.0`:

```bash
python3 docs/nodejs-aws-study-path/labs/terraform-local/run.py
python3 docs/nodejs-aws-study-path/labs/terraform-advanced/run.py
```

The runners copy teaching configuration into temporary directories, isolate relevant environment settings and remove temporary files afterward. The foundation runner covers lifecycle; the advanced runner covers child contracts, stable keys and moved addresses. Read their [foundation](../labs/terraform-local/README.md) and [advanced](../labs/terraform-advanced/README.md) explanations first. A generic `terraform test` in an unfamiliar AWS directory can create resources; these particular labs are safe because of their inspected provider/configuration boundaries.

## 2. A root directory defines an infrastructure workspace

| Root | Purpose in this project | Recorded status |
|---|---|---|
| [infra/aws-dev](https://github.com/robertovalencia/linked-in-node-and-aws/tree/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-dev) | Preserved EC2/SSM baseline | Historical architecture reference; do not confuse with ECS |
| [infra/bootstrap](https://github.com/robertovalencia/linked-in-node-and-aws/tree/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/bootstrap) | State bucket and optional OIDC definitions | Five-create bucket-only plan pending approval |
| [infra/aws-ecs-certificate](https://github.com/robertovalencia/linked-in-node-and-aws/tree/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-certificate) | Certificate request without application resources | One certificate applied; separate state preserved |
| [infra/aws-ecs-dev](https://github.com/robertovalencia/linked-in-node-and-aws/tree/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev) | Prepared private ECS/RDS/broker/networking design | HTTPS preview only; not applied |

A root is not just a folder label. Its backend, providers, inputs and state decide which remote objects it can manage. Never run a convenient apply command in the wrong directory.

## 3. Distinguish four Terraform artifacts

**Configuration** is desired resource code. **`.terraform.lock.hcl`** records selected provider versions/checksums; it belongs in source control. **State** records Terraform's managed-object identities and attributes; it is private operational data. A **saved binary plan** captures proposed actions using particular inputs and state; treat it as private too.

`terraform init` prepares the backend/providers; it is not an infrastructure apply, although a configured remote backend can require network access and credentials. `fmt` checks layout; `validate` checks configuration consistency. None proves real network connectivity or that AWS will allow every create.

## 4. Why the state bucket must come first

The ECS root declares an [S3 backend](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/infra/aws-ecs-dev/versions.tf). That backend cannot store state in a bucket that does not exist. The separate bootstrap root prepares a private, encrypted, versioned bucket with public-access blocks and a transport policy. The actual selected bootstrap plan has five creates and no OIDC.

After separately approved bootstrap, the operator would initialize the application root against the actual bucket/key, with encryption and native S3 lockfile configuration. This is pending. The certificate's existing private local state must be preserved or deliberately migrated through its own reviewed operation; creating a state bucket does not migrate every root automatically. See [the S3 backend reference](https://developer.hashicorp.com/terraform/language/backend/s3).

## 5. Preview is not the final apply artifact

The [28 October review](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/aws-https-plan-review-2026-10-28.md) records two plans: five bootstrap creates and 111 HTTPS preview creates. The HTTPS preview used a local backend to inspect proposed resources before bootstrap; it must not be applied as the final application plan.

After bootstrap, the deployment owner needs a new S3-backed saved plan, current identity/cost checks and explicit approval. Review creates, updates, replacements and deletes; bind the plan to source/input hashes and the intended account/Region. Old approval does not authorize a changed topology. See [saved-plan behavior](https://developer.hashicorp.com/terraform/cli/commands/plan).

## 6. Review the relationships, not just resource counts

The offline [plan reviewer](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/scripts/aws-ecs-review-plan.py) compares the saved binary's JSON, embedded source and private context. It checks security-group ownership/peers/ports and the listener → host rule → target group chain. Matching a count of 111 alone would miss a rule attached to the wrong group.

The critic reproduced such unsafe relationships in negative fixtures. The checker was repaired to reject them while still accepting the real valid fixture. [Evidence](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8cb1c13bc3e42f06930ce8c7f1bb6a8aa3c08b61/docs/evidence/aws-https-plan-2026-10-28/README.md) records 23 HTTPS and 11 legacy negative controls. This establishes behavior of the reviewer, not live AWS permission or connectivity.

## 7. Keep private artifacts private

Raw state, saved plans, exact client CIDR, credentials and unredacted context stay in ignored owner-only storage. Git contains summaries and hashes suitable for review. A Terraform `sensitive` annotation hides selected presentation; it does not guarantee absence from state. Never paste `terraform show -json` output into a public issue.

**Understanding check:** Why is a lock file publishable while state is private? Why must the operator make a new plan after state bootstrap? What could a resource-count-only reviewer miss?


## Copyable command workbooks

Follow [09 · local Terraform commands](09-terraform-local-commands.md) for the executable learning sequence, then [10 · the AWS operator command workflow](10-terraform-aws-commands.md). Every step states its directory, purpose, expected result and execution boundary.

> Historical approval packet: approved by the human, executed successfully once, and verified. Current actual state has 112 managed resources; the deadline remains 9:51 PM EDT.

# Complete the remaining RDS and alarms — approval packet

Prepared 2026-10-30T21:31:52.406555+00:00. **New saved plan; preparation only, not applied or approved.** The already approved deadline remains **today, October 30, 2026, 9:51:25 PM EDT** (`2026-10-31T01:51:25.219221Z`). No extension is being requested again.

The approved `754e2d2deb23` repair was executed once and **failed partially**, exit 1. AWS rejected `db.t4g.small` with `FreeTierRestrictionError: This instance size isn’t available with free plan accounts`. The response does not prove one-day backup eligibility. No account upgrade, disabled backups or silent retry occurred. Actual state is preserved: **104 managed resources, serial 7**, same lineage, no tainted resources. The eight missing resources are RDS and all seven alarms; the alarm graph was deferred after RDS failed.

The successful portion is verified: broker/AMI/root disk preserved, actual EBS expiry exactly 01:51:25Z, active replacement ALB, verified TLS, expected correct-host empty-target 503 and wrong-host 403, logging test object **and a real delivered gzip access-log object**, broker registration and actual private DNS A record. Five empty discovery definitions have fresh creation timestamps and threshold 1; AWS returned their former service IDs, so an initial ID-must-change verification assumption was rejected and corrected using actual delete/create receipts. Zero app services/tasks. Original failed evidence is preserved.

## Exact new plan

Private binary: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-rds-micro-residual-2026-10-30-v2/residual.tfplan`

SHA256: `cb438bc065c4d95f32fbe69aac6d94671c03d81e5c331ed2bc81741e21d4478a`

Account `772641336063`, Ohio `us-east-2`; existing encrypted/locked S3 backend, default workspace, Terraform 1.17.0/provider 6.70.0. **8 adds, 0 updates, 0 destroys**, with **104 existing resources no-op**. Adds are one private RDS instance and seven original alarms. No successful repair is repeated.

Only infrastructure source change: `instance_class` from `db.t4g.small` to **`db.t4g.micro`**. All original RDS settings are identical in the actual saved plan, including **one-day backups**, private networking, encryption, managed master credentials, deletion protection and final-snapshot/backup retention protections. Four service-owned databases/roles remain the application contract; no database bootstrap or secret population is in this plan. One-day backup acceptance is still unproved; stop on any new service rejection, with no account upgrade or further weakening.

This changes memory from **2 GiB to 1 GiB**, retaining 2 vCPUs. It is a smaller demo candidate; application connection/memory behavior must be checked before activation. Official AWS [RDS Free plan guidance](https://aws.amazon.com/rds/free/) lists micro sizes; the authenticated Ohio orderable-options API returned four options for this project's PostgreSQL 17.6 and `db.t4g.micro`. Neither documentation nor that listing guarantees complete account-specific create acceptance.

## Updated cost

Fresh Ohio Price List API selects SKU `GGD6FE59WWUNDKDC`, PostgreSQL Single-AZ `USE2-InstanceUsage:db.t4g.micro`: **$0.016/hour** DB compute, versus the prior $0.032/hour small instance. The unused-reservation product was explicitly excluded. Storage, backup allowance, network, logging and all other 31 prior rate selections are unchanged.

For comparison, repaired infrastructure's expected four-hour gross estimate decreases from $1.06 to **$0.99**. That is a comparison window, not a new four-hour clock. As of this packet, hypothetical immediate repaired infrastructure through the existing deadline is about **$1.07**, before credits, taxes, usage variation and billing/deletion tails. Already incurred October zone charges and prior sunk costs are excluded from the incremental view. No new replacement reserve is added to this create-only correction. See [deterministic remaining costs](evidence/aws-approved-repair-apply-2026-10-30/remaining-costs.json); these are not caps.

## Checks actually run

- Real backend-bound Terraform fmt 0, validate 0, fresh plan 2 (changes), exact show 0. Full embedded source comparison permits only the class change; provider lock/template/backend/inputs remain bound.
- One focused backend-disabled mocked Terraform run passed, preserving micro class, backup/encryption/private/recovery protections and zero app tasks. The first formatting failure is retained; no cloud apply occurred in mocks.
- Exact RDS plan structure matches the prior approved database except class; all 104 existing resources are no-op. Seven alarms retain their settings with dimensions bound to the actual broker, replacement ALB, target group and database name. Eight negative controls reject a larger DB, zero backups, public access, broker updates, wrong dimensions/thresholds, deadline reset and activation. Prior independent infrastructure critique is reused; no new reviewers were spawned and this focused check is not misrepresented as a new independent review.
- Local amd64 image preparation was attempted and stopped after Docker Hub base metadata retrieval stalled. No new successful build/scan or ECR publication is claimed. Hosted Verify still lacks a fresh green run; SonarCloud external configuration remains absent. All application release gates remain required.

## Execution boundary and command

The original approved repair is consumed; do not retry it. After approval of this **new exact hash**, recheck account/Free plan/backend/workspace/source/lock/template/binary, actual state serial/lineage and live drift. Apply this new saved artifact once; stop and preserve real state on a service rejection. Do not substitute a newly generated plan.

Working directory: `/Users/robertovalencia/Documents/Business/linked-in-node-and-aws/infra/aws-ecs-dev`. Reference only; not run:

```bash
shasum -a 256 /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-rds-micro-residual-2026-10-30-v2/residual.tfplan
# After exact human approval and immediate guards, in the existing cleaned profile environment:
terraform apply -json -input=false -lock-timeout=60s /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/work/aws-rds-micro-residual-2026-10-30-v2/residual.tfplan
```

This plan does not activate apps, publish images, populate secrets, change public DNS/client exposure, upgrade the account, perform cleanup or extend the deadline. Begin operator-assisted cleanup preparation by **7:51 PM EDT** for **9:51 PM EDT**; actual current teardown artifacts need their own approval. No automatic controller/reminder was installed.

Reply **“Approve the micro RDS completion plan cb438bc065c4.”** The prior approval does not cover a different database class/artifact. Repository `AGENTS.md` requires approval of the concrete saved plan and current costs.

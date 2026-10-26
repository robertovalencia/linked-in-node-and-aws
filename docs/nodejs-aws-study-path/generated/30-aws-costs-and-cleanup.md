---
title: "AWS costs, budgets, retention and complete cleanup"
topic: "AWS costs, budgets, retention and complete cleanup"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 30 · AWS costs, budgets, retention and complete cleanup

**Prerequisites:** 25–29; resource lifetime and state ownership.

[Previous: 29](29-aws-observability-and-incidents.md) · [Next: 31](31-aws-production-design-tradeoffs.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Turn the architecture into a cost inventory

List compute hours, EBS capacity, public IPv4, registry storage/scanning, S3 requests/versions, Secrets Manager and transfer. Add optional services before recommending them: NAT gateways, load balancers and managed databases/brokers change the baseline. A Free plan or credits affect billing eligibility, not whether a resource consumes usage.

## 2. Date every estimate

The repository's 24-hour estimate is historical preparation, not a live quote or current balance. Recheck region, account eligibility, runtime, credits and current prices before an actual plan review. This lesson intentionally gives no new price promise. AWS Budgets can monitor cost/usage and configured actions, but an alert is not an instantaneous universal spending cap.

## 3. Separate stop, destroy and retention

Stopping EC2 does not delete its EBS storage or every related charged resource. Destroying the dev root removes its managed resources according to configuration; it does not destroy the separately managed bootstrap bucket. ECR `force_delete`, S3 `force_destroy` and root disk deletion discard demonstration artifacts/data only when the corresponding destroy actually happens. Tags do not schedule expiration.

## 4. Plan the data decision before cleanup

Export evidence and required data before approving deletion. A versioned S3 bucket can retain old object versions/delete markers. The secret uses a recovery window. The bootstrap state bucket has `prevent_destroy` and requires a separately reviewed retention/removal decision. Do not erase the state that tells Terraform which resources it owns before finishing resource accounting.

## 5. Make cleanup observable

Record the intended account/region, source/state context, resource inventory, saved destroy plan, reviewer and post-cleanup checks. Inspect remaining volumes, addresses, repositories, secrets and bucket versions; check billing after its reporting delay. The current runbook states that no teardown is scheduled. A study guide does not create one automatically.

## Walk the real project

[docs/short-run.md · lines 16–16](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/docs/short-run.md#L16-L16)

```text
At the deadline, save required test/release evidence and export any database contents worth retaining. Check the account again. Create a fresh **saved destroy plan** from `infra/aws-dev`, review its exact resource list, then apply that same plan. The dev ECR repositories use `force_delete=true` and the versioned release bucket uses `force_destroy=true` so images and release objects are removed with the dev stack. The instance root disk has `delete_on_termination=true`. The secret enters its seven-day recovery window; [AWS says a secret marked for deletion has no charge](https://docs.aws.amazon.com/secretsmanager/latest/userguide/manage_delete-secret.html). These settings intentionally discard demo data and release images during final cleanup. They do not run until an approved destroy is executed.
```

[infra/bootstrap/main.tf · lines 10–10](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/bootstrap/main.tf#L10-L10)

```hcl
  lifecycle { prevent_destroy = true }
```

Open `docs/costs.md` and label its observation date and assumptions. Then compare resource destruction flags in dev with bootstrap protection. The difference is intentional: temporary runtime artifacts and the infrastructure ownership record have different retention responsibilities.

## Practice step by step

1. Build a cost worksheet with resource, unit, quantity, pricing source/date, estimate and uncertainty.
2. Fill quantities from source: one host, one root disk, two ECR app repositories, distinct state/release buckets, one runtime secret.
3. Write a source-only cleanup checklist; do not execute deletion commands for this lesson.
4. Explain what remains after dev destruction and how you would verify a genuinely empty footprint.

**Expected evidence:** A dated worksheet and complete cleanup/retention checklist identifying both Terraform roots.

## Check your understanding

### Does `prevent_destroy` mean AWS can never lose/delete that bucket?

No. It guards applicable Terraform plans while configured; it is not an AWS deletion lock or protection against every actor.

### Does a 24-hour tag terminate EC2 automatically?

No. An actual authorized automation or operator action is required, and its execution must be verified.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html)
- [S3 versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
- [EBS volumes](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volumes.html)

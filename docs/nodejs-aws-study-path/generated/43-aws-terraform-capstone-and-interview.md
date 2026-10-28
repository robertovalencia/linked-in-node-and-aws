---
title: "Capstone: explain, review and defend the AWS/Terraform design"
topic: "Capstone: explain, review and defend the AWS/Terraform design"
last_researched: 2026-10-26
source_commit: 9bb88515f14067feb23611c6851c03ca8fbc89b6
---

# 43 · Capstone: explain, review and defend the AWS/Terraform design

**Prerequisites:** All cloud lessons 20–42; complete the local lab first.

[Previous: 42](42-aws-terraform-troubleshooting-workbook.md) · [AWS/Terraform roadmap](20-cloud-roadmap-and-lab.md)

## 1. Build an evidence-backed architecture explanation

Start with one user journey: React calls nginx, authenticated requests reach the owning Node capability, PostgreSQL commits state/outbox, and Kafka eventually delivers a deduplicated notification. Then explain the AWS envelope: one EC2 host, Docker network, public subnet for outbound connectivity, zero SG ingress and an SSM tunnel to loopback 80. Finish with identities, artifacts, secrets, state and recovery boundaries.

## 2. Present Terraform as a lifecycle tool

Describe HCL inputs/references, provider selection, initialization, state/backend locking, plan review, saved apply and later drift. Use the local `terraform_data` lab to demonstrate what actually happened. Use mocked tests to demonstrate selected real configuration invariants. State that neither activity provisions or verifies a live AWS deployment.

## 3. Assemble a reviewer packet

Include a source commit, architecture diagram, identity matrix, traffic trace, Terraform dependency sketch, version/lockfile explanation, cost worksheet, release diagram, rollback plan and local test evidence. For proposed cloud work, include a concrete reviewed resource/change list rather than an invented passing plan. Record uncertain or unexecuted checks explicitly.

## 4. Rehearse a five-minute narrative

| Minute | Explain | Point to |
|---|---|---|
|1 |Business flow and capability ownership |Backend services and architecture diagram |
|2 |AWS network/access/identity |VPC, security group, instance profile, SSM |
|3 |Terraform lifecycle and state |Two roots, S3 backend, native locking and local lab |
|4 |Exact-source release and rollback |CI gate, image digests, manifest, SSM acceptance |
|5 |Tradeoffs and next evidence |Single-host limits, data recovery, managed-service proposal |

A useful rehearsal is concrete: name the line, predict a failure and show the check. Tool names without mechanism are insufficient. Avoid claiming hands-on deployment merely because the repository contains a deployment workflow.

## 5. Grade the work before moving on

Score 0 for a missing answer,1 for a definition, 2 for a project-specific explanation and 3 for a demonstrated result plus its limits. Grade identity, networking, data lifetime, Terraform state, plan/replacement, testing, release identity, rollback, cost and production tradeoffs. Repeat any item below 2. A production-extension proposal needs a validation plan even when implementation is outside the learning scope.

## Walk the real project

[infra/aws-dev/tests/security.tftest.hcl · lines 16–26](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/infra/aws-dev/tests/security.tftest.hcl#L16-L26)

```hcl
run "private_management" {
  command = plan
  assert {
    condition     = length(aws_security_group.dev.ingress) == 0
    error_message = "Dev must have no inbound access, including SSH and HTTP."
  }
  assert {
    condition     = aws_instance.dev.metadata_options[0].http_tokens == "required" && aws_instance.dev.root_block_device[0].encrypted
    error_message = "Require IMDSv2 and encrypted disk."
  }
  assert {
```

[scripts/aws-release-local.mjs · lines 27–29](https://github.com/robertovalencia/linked-in-node-and-aws/blob/9bb88515f14067feb23611c6851c03ca8fbc89b6/scripts/aws-release-local.mjs#L27-L29)

```javascript
function validateAcceptance(report) {
  requireThat(report.expected === 48 && report.passed === 48 && report.failed === 0 && report.results?.length === 48 && report.results.every(result => result.status === 'PASS'), 'CI acceptance evidence must contain exactly 48 PASS results and zero failures');
}
```

The mock assertions and exact acceptance gate are two different quality bars. Explain what each catches and what it cannot observe. Trace one proposed IAM/network edit to its expected mock assertion, saved-plan review question and future runtime check.

## Practice step by step

1. Finish the reviewer packet and record actual local lab output.
2. Rehearse the five-minute narrative without opening the README; then verify every factual claim against source.
3. Answer the questions below aloud and record the biggest remaining gap.
4. Ask a reviewer to challenge account selection, state recovery, public-subnet wording, lost-response retries and destructive rollback assumptions.

**Expected evidence:** A complete packet, a five-minute rehearsal, a scored checklist and an honest remaining-gap statement.

## Check your understanding

### Why a public subnet with no ingress instead of a private subnet?

The temporary dev design uses outbound internet access without NAT baseline cost and authenticated SSM browser access. Production alternatives need explicit requirements and connectivity/cost decisions.

### What is the most dangerous plan change here?

One strong answer is host replacement or destruction that deletes the root disk holding database/broker volumes. Explain the exact trigger and required retention/recovery decision.

### What would you improve first for production?

Tie the answer to a stated requirement: recovery/availability, public TLS entry, identity separation, centralized telemetry or managed data. Distinguish your proposal from currently implemented resources.

Do not mark this lesson complete until you can show the evidence and explain the result without reading the answer. Record your attempt and remaining question in your personal study notes; generated lessons are not personal progress records.

## References

Code excerpts are pinned to the inspected project revision `9bb8851`. They describe source, not proof that AWS resources were deployed. Official documentation was checked on 2026-10-26; verify account policies and selected tool versions before a real deployment.

- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [Terraform S3 backend](https://developer.hashicorp.com/terraform/language/backend/s3)
- [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
- [GitHub OIDC with AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)


## Next: professional core concepts beyond this baseline

Continue to [44 · complete AWS/Terraform syllabus](44-cloud-complete-syllabus-and-mastery-map.md). This foundation capstone is not the end of the cloud path. Complete the professional modules and local labs before the final [83 · architecture defense](83-professional-cloud-capstone-and-question-bank.md).

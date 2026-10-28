# 6 · Deployment, network security and recovery

[Previous: certificate](05-hostname-dns-and-certificate.md) · [Index](README.md) · [Next: building the study path](07-building-and-reviewing-the-study-path.md)

This is the **pending deployment sequence**, explained from prepared source and the owner's dated plan. It is not a report that these steps have run. The deployment owner must review costs/permissions and obtain the required concrete-plan approvals. The [selected ECS guide](../../../docs/aws-ecs-dev.md) is the detailed operator runbook.

## 1. Give every traffic path a reason

The preserved EC2/SSM design has no inbound application rules; its authenticated tunnel is the access path. The proposed HTTPS design needs an explicit public entry point. Adding an ingress rule grants permission, so “more security rules” is not automatically safer.

| Proposed connection | Why it exists | Boundary to verify later |
|---|---|---|
| Approved client `/32` → ALB 443 | Restrict demo HTTPS access to one IPv4 address | Other clients denied |
| ALB → private frontend 8180 | Forward approved host traffic | Backend not directly public |
| Frontend → capability APIs | Same-origin UI calls | Correct destinations/ports only |
| Application → private RDS 5432 | Service-owned PostgreSQL data | Owned credentials and verified TLS |
| Inquiries/Notifications → broker 9093 | Publish/consume domain events | Separate SCRAM identities and ACLs |
| Private workloads → approved egress | Images, logs and required AWS APIs | Routes, NAT/endpoints, IAM and DNS |

The actual client address stays private. A `/32` selects one IPv4 address; a security-group peer reference selects allowed network peers, not an application user. Source-group trust is not transitive. User authentication and ownership checks remain in application code.

## 2. Separate network permission from application availability

An SG rule permitting traffic does not create a route, listener, healthy target or authorized user session. The [14-case local reasoning model](../labs/network-security/README.md) demonstrates allowed/denied permissions with explicit simplifications. It does not query real ENIs or prove AWS reachability.

In the preview, the selected host routes to an empty frontend target group; zero application tasks are defined. Later, TLS with a 503 can be an expected infrastructure-only observation. A fixed 403 for an unknown host proves that rule's response, not that a complete marketplace works. These observations themselves remain pending live tests.

## 3. Follow the deployment gates in order

1. Approve/apply the separately reviewed state bootstrap.
2. Generate a fresh final S3-backed infrastructure plan; recheck identity, costs, scope and expiry/start proposal; obtain its approval.
3. Apply only the exact approved artifact and inspect actual outputs/resources.
4. Separately authorize exact-source image publication, runtime secret population, database bootstrap and application activation.
5. Verify target health, HTTPS, permitted/forbidden traffic and complete browser/API behavior.
6. Exercise recovery/rollback, then complete the selected teardown and residual-resource review.

This chapter supplies no cloud apply command. The [dated review](../../../docs/aws-https-plan-review-2026-10-28.md) defines the current pending decision: five-create bootstrap, then final infrastructure review. Do not apply the local-backend HTTPS preview merely because Terraform can read it.

## 4. Bind an image to reviewed source

A tag is a human-friendly image label; a digest identifies image content. The [ECS publisher](../../../scripts/aws-ecs-publish-local.mjs) is prepared to verify a successful source run and publish/scans manifests/digests. Its name contains “local” because it runs on the operator's machine; it can call AWS and publish images. It is not a credential-free study lab.

The current `Deploy AWS dev` workflow's optional deployment path is the preserved EC2/SSM route. An existing workflow name is not evidence of ECS deployment support. Read [toolchain](../../../docs/toolchain.md) and [.github/workflows/deploy-dev.yml](../../../.github/workflows/deploy-dev.yml) before selecting it. No infrastructure apply path is supplied by these workflows.

## 5. Keep secret values out of Terraform input history

Prepared secret resources are metadata, not proof that usable passwords/keys are populated. Runtime secret setup, TLS trust and service-owned database roles are distinct steps in the [ECS runbook](../../../docs/aws-ecs-dev.md). A task that starts with an empty secret is not ready to serve traffic.

The plan reviewer also keeps generated operator IAM policy drafts separate from attached permissions. The published draft has wildcard warnings and was not attached. A generated policy is a proposal to review, not an authority to grant itself broad rights.

## 6. Distinguish collection, alarms and response

CloudWatch log groups/configuration do not establish that a running task or host emits data. A host agent and a container log driver have different roles. An alarm definition does not establish that a real signal changes its state or that a human receives a notification. Future verification must observe emission, dimensions, retention and alarm behavior/delivery where configured.

The selected single-AZ database/broker and one zonal NAT are cost/recovery compromises. They do not form end-to-end high availability. Study [observability](../generated/65-cloudwatch-agent-logs-metrics-and-alarms.md) and [recovery](../generated/68-disaster-recovery-and-resilience-testing.md) before describing the architecture as production resilient.

## 7. Recovery and teardown are part of delivery

Image rollback can restore a binary; it does not reverse a database migration or recover lost events. The owner plans isolated database restore, replay and bad-release drills with measured RPO/RTO. A first deployment has no prior successful release to restore automatically. Read the [recovery boundaries](../../../docs/aws-ecs-dev.md) before running any operator script.

Stopping tasks does not remove a NAT, ALB, database, secrets, image storage or retained state. An expiry tag is metadata, not a deletion timer. Agree on the demo start/teardown mechanism before billable provisioning; no such clock has started in the recorded status. Retain or remove certificate/state artifacts only through their separately reviewed lifecycle.

**Understanding check:** Why can TLS work while the application returns 503? Why does a healthy target not prove inquiry delivery? Name a cost or data artifact that can outlive application tasks.

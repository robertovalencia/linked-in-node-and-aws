---
title: "Threat modeling and architecture security review"
topic: "Threat modeling and architecture security review"
last_researched: 2026-10-27
source_labels: Professional core curriculum; Official documentation; Explicit illustrative examples
---

# 79 · Threat modeling and architecture security review

**Prerequisites:** Identity, networking, managed services, encryption and telemetry lessons.

[Previous lesson](78-terraform-drift-recovery-and-state-surgery.md) · [Next lesson](80-staged-modernization-and-traceability.md) · [Full syllabus](44-cloud-complete-syllabus-and-mastery-map.md)

## 1. Start with assets, actors and entry points

Threat modeling asks what must be protected, who can act, how data flows and where trust changes. Assets include business data, identity/signing material, deployment authority, images, state and recovery keys. Actors include anonymous visitors, authenticated clients/providers, application roles, operators, CI and compromised dependencies. An architecture diagram without identities and data sensitivity misses important boundaries.

The current marketplace makes several boundaries concrete: clients and providers have different roles, ownership is checked in services, internal provider lookup has its own credential, and inquiry/outbox writes share a database transaction. These are real application controls. A proposed ALB, ECS or RDS architecture must preserve them rather than assuming managed infrastructure replaces them.

## 2. Build a data-flow and trust-boundary model

Trace browser → entry point → API → database/event stream → consumer. Then separately trace developer → GitHub verification → deployment identity → image/bundle → runtime role → secret. Add the Terraform state path and its readers/writers. Distinguish control-plane permissions from data-plane credentials and from application end-user claims.

For each crossing, ask how the caller is authenticated, which operation is authorized, what is encrypted, where errors go, what is logged and what happens after timeout or retry. A timeout can leave an uncertain successful remote write; blindly issuing a new operation identity can duplicate work.

## 3. Evaluate changes as new paths, not security brand names

A no-ingress SSM dev host and an internet-facing HTTPS ALB solve different access requirements. Adding ALB ingress is justified only by an intended reachable path with appropriate safeguards. Database ingress should reference the application security group where the selected design supports it, not an internet CIDR or every host in a broad private network. A security-group reference does not automatically trust every group reachable through it.

Adding a NAT gateway, RDS, MSK or ECS does not itself prove least privilege, encryption or correct recovery. Define the concrete invariant: for example, only the task’s runtime identity may read its needed secret, or only approved app peers may establish the database connection.

## 4. Test both required and forbidden behavior

A security acceptance plan needs allowed journeys and denied journeys. Test a valid client’s inquiry as well as another provider’s attempted modification; approved ALB-to-app access as well as direct client-to-database access; correct role use as well as an unintended repository assuming deployment authority. Positive connectivity alone is incomplete.

## 5. Review operational and recovery authority

Someone who can change a CI workflow, assume a deployment role, edit Terraform state or retrieve a host secret may influence production behavior without logging into the UI. Record those powers and recovery mechanisms. Break-glass access needs an owner, limited scope, audit and a way to end it. Do not store its secret in a study document.

## 6. Make conclusions proportional to evidence

Record a finding’s condition, relevant source/test, consequence, uncertainty and proposed repair. A paper architecture review, mock test, local simulator and live network test establish different facts. The curriculum supplies the first three; actual AWS acceptance belongs to the cost-first deployment owner.

## Example and current-project boundary

**Illustrative review matrix:**

| Asset/path | Invariant | Required/forbidden example |
|---|---|---|
| Database connection | Only intended app peers and credentials | App role connects; internet peer cannot |
| Release identity | Exact reviewed source and artifact | Approved SHA/digest accepted; unrelated run denied |
| State | Restricted environment-specific writers | Authorized pipeline writes; fork PR has no write credential |

Compare with the real [application architecture](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/docs/architecture.md). This is a teaching review, not an account-wide security assessment.

## Practice with observable evidence

1. Draw both the application path and delivery/state path with identities.
2. Pick five assets and list an allowed operation, denied operation and an abuse hypothesis for each.
3. Map each invariant to a local test, mock assertion or future AWS check.
4. Add evidence limits and an owner for any unresolved item. Feed deployment-affecting choices to the other chat instead of editing infrastructure here.

**Expected evidence:** a boundary diagram and ten positive/negative tests, with honest separation between local and live assertions.

## Recall and interview defense

### Why is ingress permission not automatically a security feature?

It grants reachability. Its safety depends on the required path, scope, destination, identity and remaining protections.

### Why review Terraform state access as part of application security?

State can reveal sensitive values and authoritative resource mappings; its writers can influence infrastructure management. Protecting only the UI misses that control path.

## Mastery gate

Explain the mechanism without reading, show the stated evidence, identify a failure case and say which facts were tested locally versus merely proposed for AWS. Keep personal notes in your existing protected progress area. Learning a service does not require deploying it in the portfolio.

## References

Official sources checked on 2026-10-27. These teach mechanisms; any account-specific cost comparison, service selection or provisioning belongs to the deployment chat and requires its own current evidence.

- [AWS security pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [Security group rules](https://docs.aws.amazon.com/vpc/latest/userguide/security-group-rules.html)

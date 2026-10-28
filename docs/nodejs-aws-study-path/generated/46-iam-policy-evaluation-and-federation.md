---
title: "IAM policy evaluation, federation, and temporary access"
topic: "IAM policy evaluation, federation, and temporary access"
last_researched: 2026-10-27
source_commit: 8b2c3e087014d76f9025dc47f5ede7837d73bfe6
---

# 46 · IAM policy evaluation, federation, and temporary access

**Prerequisites:** 45 and the existing project IAM/SSM lessons.

[Previous: 45](45-aws-account-governance-and-landing-zones.md) · [Next: 47](47-vpc-cidr-ipv6-and-subnet-design.md) · [Study path](../README.md)

**Implementation boundary:** The project declares an EC2 host role and an optional GitHub OIDC deployment role. Organization guardrails, workforce federation, and per-task application roles in this lesson are broader design topics.

A principal is the identity making an AWS request; an action is the API operation; a resource is the target; conditions constrain the request context. Authentication establishes who is calling. Authorization decides whether that caller may perform this operation now. Federation exchanges an external identity assertion for AWS access, commonly using temporary role credentials. Distinguish a role trust policy, which governs assumption, from its permissions policies, which govern subsequent actions.

## 1. Write the complete request before evaluating policy

Describe principal ARN, action, resource ARN, account, session, and relevant conditions. For example, reading a release object requires object-level S3 permission on the intended prefix. Listing a bucket is a different action and resource shape. This prevents the common mistake of treating an ARN-shaped string as proof of correct scoping. Use the service authorization reference when an action lacks resource-level support; a necessary wildcard still needs justified action and condition limits.

## 2. Trace the applicable policy layers

Identity policies and resource policies can both influence access. Permissions boundaries and session policies can constrain role permissions; organization policies may constrain them further. An applicable explicit deny overrides an allow. The simplified slogan “all policies intersect” is inaccurate because same-account resource grants differ according to the principal type being granted access. Use the official evaluation logic for role ARN versus role-session ARN cases, and label any hand-worked model as a simplification.

## 3. Treat trust as a separate review surface

An assumption must satisfy the role trust policy and any caller-side authorization required for that flow. For OIDC, constrain issuer/provider, audience, and subject to the intended repository or environment. A broad subject wildcard can turn another workflow into a deployment identity. Temporary credentials limit credential lifetime, but they do not make excessive permissions safe. Review session duration, revocation expectations, and what happens when the source workflow or identity provider is compromised.

## 4. Assign human and workload access deliberately

Humans need auditable, time-bounded sessions, preferably through centrally managed federation. EC2, ECS tasks, and Lambda use workload-specific role mechanisms. Do not distribute an operator’s access key into application containers. The project host role reads its runtime secret and release prefix and pulls ECR images; an application moved into ECS would need a separate task-role decision. Sharing code or a Docker image does not imply every capability needs the same AWS permissions.

## 5. Diagnose denied actions using evidence

First confirm the actual principal and request parameters from a redacted error or audit record. Check trust failures separately from API failures after assumption. Then inspect explicit denies, applicable grants, resource policy, boundaries, organization policy, and service-specific conditions such as KMS policy or endpoint policy. A local policy simulator or truth table can teach mechanics but cannot fully reproduce every resource-policy, organization, or runtime context. Never repair uncertainty by blindly attaching administrator access.

## Source or illustrative example

**Actual source anchor:** [host and deployment role policies](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/infra/aws-dev/main.tf) show scoped release-object access and an OIDC trust condition tied to the `dev` environment. The optional role exists only when its feature input enables it. **New illustrative request:** an ECS catalog task reads one media prefix using its own role; this role and workload are not implemented by that source.

## Safe exercise

Run a local simplified authorization exercise:

```sh
node --input-type=module <<'JS'
const decision = ({allow, boundary, deny}) => !deny && allow && boundary;
for (const row of [
  {allow:true,boundary:true,deny:false},
  {allow:true,boundary:false,deny:false},
  {allow:true,boundary:true,deny:true},
]) console.log(decision(row) ? 'ALLOW' : 'DENY');
JS
```

Expected outcome: `ALLOW`, `DENY`, `DENY`. This models only an identity allow constrained by a boundary and explicit deny. Add a note explaining why it is not a complete AWS authorization simulator, especially for resource-policy session grants.

## Failure diagnosis

If `AssumeRoleWithWebIdentity` fails, inspect token issuer, audience, subject, provider, and trust policy before reviewing S3 permissions. If assumption succeeds but object access fails, inspect the object ARN/prefix, resource policy, encryption key access, and any endpoint controls. If a role works in development but not production, compare the full account governance and session context. Avoid recording bearer tokens, access keys, or unredacted secret values in the troubleshooting packet.

## Recall and answers

### Can a boundary grant access that an identity policy lacks?

No. A boundary limits permissions; it is not an independent grant.

### Does short-lived access remove the need for subject constraints?

No. A short session issued to the wrong workflow is still unauthorized access.

## Mastery check

Explain two failures: an identity cannot assume a role, and an assumed role cannot read an encrypted object. Name the distinct policy surfaces and evidence needed. Review the actual OIDC subject condition and state its scope without claiming the workflow has run.

## References

Primary official documentation was checked on 2026-10-27. Source links are pinned to `8b2c3e087014d76f9025dc47f5ede7837d73bfe6` and describe repository declarations, not verified AWS resources. Exercises are local or read-only; no resource creation, saved infrastructure plan, or cost estimate is part of this lesson.

- [IAM policy evaluation](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [ECS task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html)

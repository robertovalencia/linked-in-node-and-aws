---
title: "Terraform team CI and approval workflows"
topic: "Terraform team CI and approval workflows"
last_researched: 2026-10-27
source_labels: Terraform mechanics; New workflow design exercise; Project code comparison
---

# Terraform team CI and approval workflows

Prerequisite: testing and policy. Continuous integration means running repeatable checks when a change enters the shared workflow. Infrastructure delivery adds another requirement: a checked change must be tied to a particular state, identity, reviewed plan and authorized execution. A source-code approval alone does not identify everything an apply will do.

The workflow described here is a new design exercise. The project's existing [deployment workflow](https://github.com/robertovalencia/linked-in-node-and-aws/blob/8b2c3e087014d76f9025dc47f5ede7837d73bfe6/.github/workflows/deploy-dev.yml) provides real examples of manual invocation, verification, an environment and scoped permissions. It is an application release workflow; do not describe it as an already implemented saved-plan Terraform approval pipeline.

## Step 1: define the trust boundary of each event

A pull request can contain untrusted executable content: scripts, provider selections, test code and workflow edits. Running Terraform against those files may execute plugins or other configured operations. Even a command called plan can access credentials, read remote state and invoke data sources. Classify what an event may execute before deciding which credentials it receives.

Fork pull requests should normally receive checks that need no privileged backend access or cloud identity. Formatting, source review and an isolated credential-free lab are examples. A privileged workflow that checks out attacker-controlled code can expose its tokens and state. Do not combine a privileged `pull_request_target` context with arbitrary pull-request checkout. Treat artifacts arriving from less-trusted jobs as untrusted input, too. GitHub's [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use) describes these risks.

Distinguish a maintainer's approval of an external contributor from approval of a particular revision. A later push can change the code. Re-evaluate checks and review when the relevant revision changes. Similarly, repository ownership does not make every dependency immutable: a third-party action, module source or plugin must have an intentional update and integrity strategy.

## Step 2: bind the plan to its inputs

A saved Terraform plan is an executable decision artifact. Record its source revision, root directory, Terraform version, provider lock selection, input provenance, backend state identity and creation time. A human-readable summary helps review; the binary plan preserves the actual decisions to apply. Applying source code by generating a fresh plan after approval can produce different actions from those a reviewer saw.

A proposed workflow therefore produces a saved plan in a trusted context, checks it, stores it in restricted artifact storage and makes that exact artifact available to the authorized apply job. Record a cryptographic digest and verify the artifact identity at use. This is a design pattern, not a claim that the current repository already implements it. The [plan reference](https://developer.hashicorp.com/terraform/cli/commands/plan) explains saved plans and their sensitive contents.

Plans can contain secrets even when terminal output displays redaction. Do not attach binary plans or unredacted plan JSON to public pull-request comments. Limit artifact readership, retention and download authority. A plan summary may itself expose resource identifiers or sensitive strings, so review its content before publication. Plan security is part of backend security rather than a separate cosmetic concern.

An old plan may become stale after another state change, and external drift may occur after it was created. Set an intentional validity window and re-plan when relevant context changes. Avoid pretending a digest proves freshness; it proves identity of bytes. Requiring a new plan after expiration or state change also requires renewed review of that new artifact.

## Step 3: separate concurrency from authorization

A backend lock protects a particular state's cooperating writers. A CI concurrency group prevents conflicting jobs according to the workflow configuration. Both are useful, but neither grants approval. A waiting run can become obsolete while another apply completes. Canceling a running apply indiscriminately can interrupt it after some changes succeeded, so understand the runner's termination and recovery behavior.

Assign a specific state owner and approval authority. A proposed production change should have a reviewer capable of interpreting replacements, deletions, IAM effects and dependency changes. A generic approval button without a readable plan does not create informed review. Emergency bypass should name who can use it and how the resulting actions are audited. These are workflow design choices; this lesson does not change repository branch protection or external environments.

After execution, preserve the plan identity, command result and resource-change evidence. A zero exit status is useful but does not establish application health. Infrastructure checks and application verification must be tied to their own observable results. If an apply fails halfway, capture the diagnostic and obtain a new plan rather than blindly rerunning an obsolete artifact.

## Step 4: scope temporary identity

OIDC lets a workflow exchange a signed identity token for short-lived cloud credentials. It reduces dependence on long-lived stored access keys, but the role's trust and permissions still determine what the job can do. Restrict expected audience and subject claims to the intended repository and branch or protected environment. Environment-based subjects have different shapes from branch-based subjects; the trust must match the actual token context. [GitHub's AWS OIDC guide](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws) documents this boundary.

Grant token-request permission only to jobs that need it. A plan identity and apply identity can have different authority, but remember that refreshing a plan often needs broad read access. Backend access is another permission surface. A short-lived credential used by untrusted code can still be abused during its lifetime. Pair runtime identity with trusted source selection and runner isolation.

## Practice and expected results

Draw a proposed sequence from fork checks through trusted plan, restricted artifact, review, exact-plan apply and post-apply verification. Label every arrow with the source revision or artifact digest it carries. Introduce two faults: a contributor pushes another commit after approval, and another run changes state. Expected behavior is a new reviewable plan, with privileged execution withheld until the workflow's current conditions are satisfied.

Run the advanced local lab as a credential-free check that could belong in the first stage. Its success demonstrates local Terraform contracts and lifecycle assertions. It provides no evidence that OIDC trust, branch protection or protected-environment reviewers have been configured.

### Recall: Does applying the same Git commit guarantee the same actions a reviewer saw yesterday?

**Answer:** No. Inputs, state, external objects and dependency selections may differ. Tie approval to a specific plan and context, enforce freshness, and review again when those inputs change.

## References

Official documentation checked on 2026-10-27.

- [Saved plans and sensitive data](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [Workflow security and untrusted checkout](https://docs.github.com/en/actions/reference/security/secure-use)
- [AWS OIDC trust from GitHub Actions](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)

[Previous lesson](./76-terraform-testing-and-policy-as-code.md) · [Next lesson](./78-terraform-drift-recovery-and-state-surgery.md)

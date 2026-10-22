---
title: "Delivery tools: specifications, CI, quality gates and traceability"
topic: "Delivery tools: specifications, CI, quality gates and traceability"
last_researched: 2026-10-22
source_labels: Project code; Library mechanics; Practice extensions explicitly labeled
---

# Delivery tools: specifications, CI, quality gates and traceability

Prerequisites: lesson 13. The role expects human direction and verification of generated code.

Study one concept at a time: explain it, open the linked code, then answer the recall question. Code blocks are source excerpts unless the practice section explicitly says to run them.

## A specification is an executable-review target

**What:** An agent task needs a bounded requirement, constraints and observable acceptance criteria.

**How:** The project’s contract defines behavior and its acceptance suite exercises it. Ask an AI tool for a small reviewable change, then inspect the actual diff and failure cases.

**Real code:** [CONTRACT.md · lines 1–6](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/CONTRACT.md#L1-L6).

```text
# Marketplace API and event contract

This document defines the local application boundaries and the API behavior that the frontend and services rely on. The schemas below define the public migration contract; the executable reference is `scripts/acceptance.mjs`.

**Stack:** Node.js 22, NestJS, strict TypeScript, React/Vite, PostgreSQL and Kafka. Local and AWS dev have independent configuration, secrets and data.

```

**Watch for:** The employer’s approximately 95% generated-code target is not a measured achievement for this project.

### What should a useful agent instruction contain?

The behavior, source context, boundaries, acceptance cases and evidence required to finish.

## GitHub Actions jobs and dependency order

**What:** A workflow describes automated jobs. Each job’s commands provide different evidence from type checks to real integration behavior.

**How:** Verify runs source checks, integration and Terraform validation. Deployment is a separate manual workflow; a workflow file existing is not proof of a successful run.

**Real code:** [.github/workflows/verify.yml · lines 12–19](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/workflows/verify.yml#L12-L19).

```yaml
jobs:
  source:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
```

**Watch for:** A green build does not prove that cloud deployment occurred.

### Why separate unit and integration jobs?

They have different dependencies, costs and failure meanings.

## SonarLint versus a server quality gate

**What:** Editor analysis gives local feedback. SonarQube analysis and its configured gate evaluate submitted project evidence.

**How:** The deployment workflow requires configuration and waits for the Sonar gate. Coverage scope, exclusions and actual findings must be reviewed rather than treated as universal quality scores.

**Real code:** [.github/workflows/deploy-dev.yml · lines 41–42](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/workflows/deploy-dev.yml#L41-L42).

```yaml
-Dsonar.qualitygate.wait=true
-Dsonar.qualitygate.timeout=300
```

**Watch for:** Do not claim a hosted integration is verified merely because variables or plugins are listed.

### Does a passing gate prove ownership checks are correct?

No. Meaningful security tests and code review are still required.

## Dependabot and dependency-change review

**What:** Dependabot proposes dependency updates. Lockfiles record the exact resolved graph used by installation.

**How:** This repository config covers npm, actions, Terraform and Docker. A version PR still needs compatibility, release-note, security and test review; an automatic proposal is not an automatic approval.

**Real code:** [.github/dependabot.yml · lines 2–9](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/dependabot.yml#L2-L9).

```yaml
updates:
  - package-ecosystem: npm
    directory: /
    schedule: {interval: weekly}
  - package-ecosystem: npm
    directory: /backend
    schedule: {interval: weekly}
  - package-ecosystem: npm
```

**Watch for:** A transitive override such as js-yaml is a reviewed dependency policy, not an application YAML API.

### Why inspect a lockfile change?

It can modify transitive runtime or build dependencies beyond the package name in the PR title.

## OIDC, release manifests and serialization

**What:** A release manifest associates source identity with exact image content. A host lock prevents overlapping deployment scripts.

**How:** The remote script obtains a filesystem lock before applying a release. App rollback and data/schema recovery remain different operations.

**Real code:** [scripts/aws-remote-deploy.sh · lines 7–11](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/scripts/aws-remote-deploy.sh#L7-L11).

```bash
exec 9>/opt/marketplace/deploy.lock
flock -n 9 || { echo 'Another deployment is running'; exit 1; }
secret_arn=$(jq -er .secret_arn manifest.json)
region=$(jq -er .region manifest.json)
registry=$(jq -er .backend manifest.json | cut -d/ -f1)
```

**Watch for:** An image rollback cannot undo a destructive migration or restore missing rows.

### Why link the source commit to image digests?

It lets a reviewer trace exactly which built content was released from which source.

## Jira, VS Code and architect collaboration

**What:** Tickets track requirements; the editor supports source navigation and debugging; an architecture decision explains constraints and alternatives.

**How:** The project’s traceability document connects requirement records to tests and release evidence. Draft a ticket and ADR locally before claiming any external ticket or approval exists.

**Real code:** [docs/traceability.md · lines 1–6](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/docs/traceability.md#L1-L6).

```text
# Requirements through release

The stable identifiers below map the interview specification to source, tests and operational evidence. They are local requirement IDs; Jira issue keys become real only after import into the chosen Jira project. Do not invent issue URLs or claim an import ran.

| Requirement | Implementation | Verification | Deployment/release link |
|---|---|---|---|
```

**Watch for:** A role requirement or study exercise is not personal production experience.

### What makes traceability useful?

A real requirement can be followed through specification, diff/test, artifact and observed release result.

## Practice and mastery

Draft an agent task for the proposed minRate filter. Include default compatibility, invalid bounds, affected files and expected tests.

- Review an intentionally missing-owner-check change in a practice copy; explain why it is wrong before repairing it.
- Record one chain: requirement → code change → behavioral test → artifact → release result. Mark stages that have not run as planned.
- Give the architect one recommendation, one alternative and one unresolved assumption.
- Use Claude Code as the role’s requested tool; distinguish that expectation from which agent created this project. Do not fabricate generation percentages or completed integrations.

## References

Code links are pinned to the inspected source commit. The repository lockfiles define the study baseline; library documentation may cover newer versions.

- [GitHub Actions workflows](https://docs.github.com/en/actions/writing-workflows/about-workflows)
- [GitHub OIDC](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [Project example: A specification is an executable-review target](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/CONTRACT.md#L1-L6)
- [Project example: GitHub Actions jobs and dependency order](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/workflows/verify.yml#L12-L19)
- [Project example: SonarLint versus a server quality gate](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/workflows/deploy-dev.yml#L41-L42)
- [Project example: Dependabot and dependency-change review](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/.github/dependabot.yml#L2-L9)
- [Project example: OIDC, release manifests and serialization](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/scripts/aws-remote-deploy.sh#L7-L11)
- [Project example: Jira, VS Code and architect collaboration](https://github.com/robertovalencia/linked-in-node-and-aws/blob/fbf61d81f9d240e2d974f1bcf21789ac6f2b21fa/docs/traceability.md#L1-L6)

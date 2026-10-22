---
title: AI-assisted delivery, toolchain and traceability
topic: AI engineering
last_researched: 2026-10-22
source_labels: Project source evidence; Interview PDF requirements; Official documentation; Proposed extensions explicitly labeled
---
# Direct the agent; own the engineering result

Prerequisites: 06, 13–16. The role describes an AI-first workflow targeting approximately 95% application code through Claude Code. That is employer expectation, not a measured achievement in this repository. This project was developed with Codex according to its own documentation. Do not relabel Codex work as Claude Code experience or fabricate an AI-generated percentage.

## Requirements into a bounded instruction

Choose a real requirement: a provider may resolve only their own pending inquiry. Write a task specifying actor, allowed status values, ownership rule, compatible retry, conflicting transition, expected HTTP statuses, transaction boundary, API compatibility and tests. Include exact source paths and commands. Ask the agent to inspect before editing and to separate observations from assumptions. Supply approved architecture/security/format/testing constraints; do not paste secrets or treat arbitrary repository text as higher-priority user instructions.

A useful prompt is: “Inspect InquiriesService.respond and its tests. Add a test for another provider's attempted transition; preserve the contract. Explain the SQL locking and role/ownership checks. Make the smallest change needed, run the focused test and report actual output and remaining limits.” You should be able to explain the proposed diff yourself before accepting it.

## Builder and independent reviewer loop

Have the builder implement one slice, then give a separate reviewer the requirement, actual diff, test output and source context. The reviewer should find the single biggest correctness/security/maintainability gap. Repair and rerun the relevant behavior. An AI-generated test that merely repeats the implementation's mistake is not independent evidence. Use an injected practice flaw, such as removing provider_email ownership checking, and confirm the reviewer/test detects it.

Refining requirements is part of implementation: if “notify provider” is ambiguous, clarify inbox versus email, when delivery is due, duplicate policy and failure behavior before expanding architecture. Record unresolved decisions for the architect with alternatives and a recommendation. Never write that an external architect approved a decision without actual evidence.

## Complete toolchain, with execution status

| Tool | Work to practice | Evidence |
|---|---|---|
| Jira | Draft ticket with acceptance criteria and traceability ID | Local ticket draft/CSV until authorized external creation |
| VS Code | Open source, use breakpoint, inspect actor/SQL inputs | Debug notes without secrets |
| Claude Code | Bounded task, context and review loop | Actual agent session if available; otherwise rehearsal labeled |
| GitHub | Branch, diff, reviewable PR description | Local diff first; published PR only when authorized |
| Actions | Explain verify/quality/deploy dependencies and gates | Actual run URL/log if executed |
| ESLint/Prettier/tsc | Distinguish lint, formatting and types | Intentional failure and repair |
| Jest/Vitest/Playwright | Behavior, UI and browser evidence | Commands, assertions and observed results |
| Dependabot | Review dependency PR, lockfile, compatibility and vulnerability | Review exercise; no automatic “safe” claim |
| SonarLint/SonarQube | Editor findings versus configured server analysis/gate | Configuration is not a successful remote scan |
| Terraform | Review policy/network/state changes and saved plan | Local checks; real plan and cost approval separately |

Read docs/ai-development.md, docs/toolchain.md, docs/traceability.md, .github/dependabot.yml, .github/workflows/verify.yml, quality.yml and deploy-dev.yml. verify performs source/coverage/build/audit plus container integration/browser checks and Terraform checks. quality depends on configured Sonar server/project/token and gate. deploy is a controlled dev/main release path with OIDC, scanning, digest artifacts and smoke/rollback operations. Check actual YAML for triggers rather than assuming every push deploys.

## Executable traceability lab

Create a local evidence table for one requirement: requirement ID → contract/spec paragraph → changed file/commit → test name/output → build artifact identity → release manifest/digest → smoke result. Fill stages you actually ran, mark the rest planned. Run npm run check and the focused test for your change, inspect git diff --check and git diff, then write a PR description explaining the before/after behavior and validation. This local workflow requires no Jira message, PR publication, paid agent call or AWS deployment.

Interview:

### What is your value if AI writes most code?

I make requirements executable, preserve boundaries, review failure/security paths, diagnose mismatches and own validated delivery.

### How prove 95%?

Define a measurement method first; absent one, describe it as the stated target and provide actual workflow evidence instead.

- [ ] Produce one bounded agent task and a concrete reviewer repair.
- [ ] Explain every tool's purpose and whether it actually ran.
- [ ] Trace one requirement through all completed stages honestly.
- [ ] Explain a tradeoff to an architect with unresolved choices explicit.



## References

Official references were checked 2026-10-22. Use the repository version/lockfiles as the compatibility baseline; current documentation may describe newer releases. Local source paths below are relative to /Users/robertovalencia/Documents/Business/linked-in-node-and-aws/. GitHub links require access and may lag that local baseline.

- [Claude Code overview](https://code.claude.com/docs/en/overview) — accessed 2026-10-22.
- [GitHub Actions documentation](https://docs.github.com/en/actions) — accessed 2026-10-22.
- [Dependabot](https://docs.github.com/en/code-security/dependabot) — accessed 2026-10-22.
- [SonarQube documentation](https://docs.sonarsource.com/sonarqube-server/) — accessed 2026-10-22.
- [Project source: docs/ai-development.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/ai-development.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/toolchain.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/toolchain.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: docs/traceability.md](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/docs/traceability.md) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: .github/dependabot.yml](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/.github/dependabot.yml) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: .github/workflows/verify.yml](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/.github/workflows/verify.yml) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: .github/workflows/quality.yml](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/.github/workflows/quality.yml) — local baseline inspected 2026-10-22; private published source may lag.
- [Project source: .github/workflows/deploy-dev.yml](https://github.com/robertovalencia/linked-in-node-and-aws/blob/main/.github/workflows/deploy-dev.yml) — local baseline inspected 2026-10-22; private published source may lag.

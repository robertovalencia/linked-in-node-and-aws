# Requirements through release

The stable identifiers below map the interview specification to source, tests and operational evidence. They are local requirement IDs; Jira issue keys become real only after import into the chosen Jira project. Do not invent issue URLs or claim an import ran.

| Requirement | Implementation | Verification | Deployment/release link |
|---|---|---|---|
| R01 discovery | backend/src/catalog, frontend/services and hooks | acceptance search/filter/sort/paging; frontend discovery tests | Same catalog image/source commit as release |
| R02 profile/compare | frontend/src/components and routes | comparison/profile component tests; browser smoke | Frontend image digest |
| R03 identity/security | backend/src/common/auth.ts, identity | JWT/role/owner Jest tests; acceptance negative cases | Identity runtime of backend digest |
| R04 owned edits | catalog service + profile editor | acceptance cross-owner/invalid-price/persistent read; frontend workspace tests | Catalog runtime; migration version |
| R05 inquiry/idempotency | backend/src/inquiries | original concurrent duplicate checks + transaction tests | Inquiries runtime; DB migration |
| R06 lifecycle | inquiries service, workspace | accepted/declined/ownership API checks | Inquiries runtime |
| R07 notifications | outbox publisher + notifications consumer | Kafka acceptance; failure-drill replay/outage | Kafka topic + notifications runtime |
| R08 React separation | frontend/src/{components,services,routes,types,contexts,hooks} | lint/types; Vitest stale-request and error tests | Frontend digest |
| R09 local setup | compose.yaml, scripts/local.sh, scripts/dev.mjs | full Compose acceptance; hot-reload readiness | Local project linked-in-node-local |
| R10 AWS dev | infra/aws-ecs-dev, infra/aws-ecs-certificate; owned TLS connections/bootstrap/replay; scripts/aws-ecs-* | [Fresh local preparation evidence](evidence/ecs-preparation/verification-manifest.json), 10+2 mock runs, PG30/Kafka9/DNS5, saved-plan negative controls and independent critic | [Selected ECS guide](aws-ecs-dev.md); local-backend 108-create preview only; final S3 plan, exact-source CI and all cloud gates tracked separately |
| R11 toolchain | .github, .vscode, sonar-project.properties, compose.ci-quality.yaml, scripts/sonar-ci.mjs | Prior local/Verify gates pass; fresh exact-SHA verification with isolated CI Sonar 80% gate required; hosted Cloud remains pending | Successful verification-only run ID checked by local release helper; optional protected GitHub deploy mode retained |
| R12 learning/AI | AGENTS.md, docs/specs, docs/prompts, guides | independent critic; docs link check; interview rehearsal | docs/releases/current.json |

For a new change use branch/commit naming such as `R05: preserve idempotency across retries`, then add the actual commit SHA and pull-request/workflow links to its review entry. A release records source SHA, migration versions, test-report identity and immutable image digests. The prepared AWS deploy script retains deployed digests for rollback; it is not proof of a deployment until executed.

[Jira CSV](jira-import.csv) has importable Summary, Description, Issue Type and Labels columns. In Jira map those fields in CSV import, choose your existing project, inspect the preview and import. Add returned issue keys to this table and link pull requests manually or through your configured integration. CSV creation did not access Jira.


## Cloud study extension evidence

R12 → `docs/nodejs-aws-study-path/generated/20–43` → `scripts/check-cloud-study.py` → `labs/terraform-local/run.py` and `evidence/` → independent curriculum review. These are teaching/local verification results, not AWS deployment evidence. The app imports managed guides with profile-scoped IDs and preserves personal notes/expansions/comments.


## Production dependency advisory repair

R11 → `backend/package.json` scoped override and `backend/package-lock.json` patched parser/upload dependencies → production audits, valid dependency tree, existing unit suites and unchanged real API contract → `docs/evidence/ci-security-repair/` → independent review. Hosted SonarCloud configuration/status is tracked separately in `docs/sonarqube-cloud.md`; its gate remains required when that workflow runs.


## Cost-first deployment redesign

R10 → [phased ADR and cost review](aws-cost-review-2026-10-27/README.md) → `model.py` / `rates.json` / exact scenario ledger → independent `critic_audit.py` (42 platform + six streaming cases) / `critic.md` → sanitized October 27 account and baseline-preview summaries. Cost/topology selection, hardened infrastructure, final S3-backed plan approval, cloud recovery/security/48-check execution and teardown are pending. No Jira import or new release is implied by these local requirement links.

## Selected ECS scope

R10 selection supersedes the earlier proposed SSM recommendation for preparation only. [Requirements](specs/requirements.md) → [runtime/Terraform source](../infra/aws-ecs-dev/README.md) → [local execution manifest](evidence/ecs-preparation/verification-manifest.json) → [sanitized actual plan/costs](evidence/ecs-preparation/staging-plan-cost-review.json) → [critic record](reviews.md). The new publisher validates exact-SHA GitHub/Sonar/48-API evidence and isolated ECS state before ECR writes; no AWS publication or deployment occurred. Jira import and actual deployment/release identities remain pending.

## Historical R10 free-hostname preparation checkpoint, 27 October 2026

[Free hostname guide](aws-free-test-hostname.md) → dynv6 primary CNAME/CAA/underscore documentation and public/authoritative DNS checks → owner account/zone reservation → reviewed certificate-only plan and actual ACM ISSUED → new final S3-backed infrastructure plan. The candidate is not claimed reserved. No AWS or provider records were created, no application/Terraform source changed and no free-DNS feature removes the cloud approval or security gates.

Historical checkpoint before certificate approval: R10 registered-zone checkpoint → owner-account/public DNS evidence → `infra/aws-ecs-certificate` (unchanged source) → two passing mock tests → [one-create saved certificate plan receipt](evidence/certificate-request/plan-review.json) → user approval pending → actual CNAME/ISSUED → fresh reviewed infrastructure plan. The old hostname-free preview is not an activation approval.

R10 approved certificate execution → exact reviewed plan/source/account guards → Terraform one-resource apply → actual provider CNAME → three-resolver DNS proof → live ACM ISSUED/DNS SUCCESS → no-change post-issuance plan → [execution evidence](evidence/certificate-request/issuance.json) / [independent critic](evidence/certificate-request/issuance-critic.md). Client CIDRs/final infrastructure plan and all application deployment gates remain pending.
